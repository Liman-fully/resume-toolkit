#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
classify 模块单元测试
"""

import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from resume_dedup.classify import guess_category, classify_folder, classify_files


def make_pdf(folder, name, content=b"pdf"):
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, name)
    with open(path, "wb") as f:
        f.write(content)
    return path


# ── guess_category ────────────────────────────────────────────

class TestGuessCategory:
    """验证关键词匹配的准确性"""

    @pytest.mark.parametrize("filename,expected_category", [
        # 留学生
        ("留子优先新媒体运营-张三.pdf", "00_留学生"),
        ("海归产品经理-李四-上海.pdf", "00_留学生"),
        # 新媒体运营
        ("新媒体运营-王五-3年-广州.pdf", "01_新媒体与内容运营"),
        ("公众号编辑-陈六.pdf", "01_新媒体与内容运营"),
        ("抖音运营专员-赵七.pdf", "01_新媒体与内容运营"),
        # 内容创作
        ("文案策划-周八-北京.pdf", "02_内容创作与传媒"),
        ("编辑记者-吴九.pdf", "02_内容创作与传媒"),
        # 社群运营
        ("社群运营-郑十-上海.pdf", "03_社群与产品运营"),
        ("私域运营专家-钱某.pdf", "03_社群与产品运营"),
        # HR
        ("人力资源总监-HRBP-孙某.pdf", "04_人事HR"),
        ("招聘经理-韩某.pdf", "04_人事HR"),
        # 项目管理
        ("项目经理-PMO-赵某-PMP.pdf", "05_项目管理"),
        ("敏捷教练-北京.pdf", "05_项目管理"),
        # 培训教育
        ("课程研发-讲师-上海.pdf", "06_培训教育"),
        # 技术研发
        ("Java开发工程师-李某-5年.pdf", "07_技术研发"),
        ("测试工程师-QA-深圳.pdf", "07_技术研发"),
        ("自动驾驶算法工程师.pdf", "07_技术研发"),
        # AI与产品
        ("产品经理-AI方向-北京.pdf", "08_AI与产品"),
        ("AI产品总监-张某.pdf", "08_AI与产品"),
        # 市场营销
        ("市场总监-品牌-广州.pdf", "09_市场营销"),
        ("BD经理-商务拓展-深圳.pdf", "09_市场营销"),
        # 数据分析
        ("数据分析师-BI-3年.pdf", "10_数据分析"),
        # 设计
        ("UI设计师-交互设计-上海.pdf", "11_设计创意"),
        # 供应链
        ("供应链经理-采购-杭州.pdf", "12_供应链与电商"),
        # 行政财务法务
        ("财务总监-CFO-深圳.pdf", "13_行政财务法务"),
        ("法务合规-律师-北京.pdf", "13_行政财务法务"),
        # 兜底
        ("未知_5.pdf", "14_待人工归类"),
        ("resume_001.pdf", "14_待人工归类"),
    ])
    def test_category_mapping(self, filename, expected_category):
        result = guess_category(filename)
        assert result == expected_category, (
            f"文件 '{filename}' 期望分类 '{expected_category}'，实际得到 '{result}'"
        )

    def test_case_insensitive(self):
        assert guess_category("java开发.pdf") == guess_category("JAVA开发.pdf")

    def test_留学生_takes_priority_over_新媒体(self):
        """留学生标签应优先于职能标签"""
        result = guess_category("留子优先新媒体运营.pdf")
        assert result == "00_留学生"


# ── classify_folder ───────────────────────────────────────────

class TestClassifyFolder:
    def test_dry_run_no_move(self, tmp_path):
        source = tmp_path / "_待分类"
        source.mkdir()
        make_pdf(str(source), "产品经理-张三.pdf")

        result = classify_folder("_待分类", base_dir=str(tmp_path), dry_run=True)
        assert result.moved_count == 1
        # 文件未实际移动
        assert (source / "产品经理-张三.pdf").exists()

    def test_execute_moves_file(self, tmp_path):
        source = tmp_path / "_待分类"
        source.mkdir()
        make_pdf(str(source), "Java开发工程师-李四.pdf")

        result = classify_folder("_待分类", base_dir=str(tmp_path), dry_run=False)
        assert result.moved_count == 1
        assert not (source / "Java开发工程师-李四.pdf").exists()
        assert (tmp_path / "07_技术研发" / "Java开发工程师-李四.pdf").exists()

    def test_conflict_resolution(self, tmp_path):
        """目标文件夹已有同名文件时，应追加 _dup1 后缀而非覆盖"""
        source = tmp_path / "_待分类"
        target = tmp_path / "14_待人工归类"  # 兜底分类
        source.mkdir(); target.mkdir()
        # 使用无法匹配任何关键词的文件名，确保归入 14_待人工归类
        make_pdf(str(source), "未知候选人.pdf", b"new")
        make_pdf(str(target), "未知候选人.pdf", b"existing")

        result = classify_folder("_待分类", base_dir=str(tmp_path), dry_run=False)
        assert result.moved_count == 1
        # 原文件未被覆盖
        assert (target / "未知候选人.pdf").read_bytes() == b"existing"
        # 新文件以 _dup1 后缀保存
        assert (target / "未知候选人_dup1.pdf").exists()

    def test_source_not_found(self, tmp_path):
        result = classify_folder("_不存在", base_dir=str(tmp_path), dry_run=True)
        assert result.moved_count == 0
        assert len(result.errors) > 0

    def test_fallback_category(self, tmp_path):
        source = tmp_path / "_待分类"
        source.mkdir()
        make_pdf(str(source), "未知_99.pdf")

        result = classify_folder("_待分类", base_dir=str(tmp_path), dry_run=False)
        assert result.moved_count == 1
        assert (tmp_path / "14_待人工归类" / "未知_99.pdf").exists()

    def test_non_pdf_ignored(self, tmp_path):
        source = tmp_path / "_待分类"
        source.mkdir()
        (source / "doc.docx").write_bytes(b"word")
        make_pdf(str(source), "resume.pdf")

        result = classify_folder("_待分类", base_dir=str(tmp_path), dry_run=True)
        assert result.moved_count == 1  # 只处理 pdf


# ── classify_files ────────────────────────────────────────────

class TestClassifyFiles:
    def test_only_specified_files_moved(self, tmp_path):
        source = tmp_path / "_源"
        source.mkdir()
        make_pdf(str(source), "产品经理.pdf")
        make_pdf(str(source), "Java工程师.pdf")

        # 只归类 "产品经理.pdf"
        from resume_dedup.classify import classify_files
        result = classify_files(["产品经理.pdf"], "_源", base_dir=str(tmp_path), dry_run=False)
        assert result.moved_count == 1
        assert (source / "Java工程师.pdf").exists()  # 未被移动

    def test_missing_source_file_skipped(self, tmp_path):
        source = tmp_path / "_源"
        source.mkdir()
        from resume_dedup.classify import classify_files
        result = classify_files(["不存在.pdf"], "_源", base_dir=str(tmp_path), dry_run=True)
        assert result.moved_count == 0
        assert len(result.skipped) == 1
