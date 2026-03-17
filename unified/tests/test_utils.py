#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
utils 模块单元测试
运行：pytest tests/ -v
"""

import os
import tempfile
import pytest

# 让测试可以在任意机器上运行，不依赖实际简历库路径
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from resume_dedup.utils import file_hash, score_filename, pick_best, collect_hashes


# ── file_hash ─────────────────────────────────────────────────

class TestFileHash:
    def test_same_content_same_hash(self, tmp_path):
        f1 = tmp_path / "a.pdf"
        f2 = tmp_path / "b.pdf"
        f1.write_bytes(b"hello resume")
        f2.write_bytes(b"hello resume")
        assert file_hash(str(f1)) == file_hash(str(f2))

    def test_different_content_different_hash(self, tmp_path):
        f1 = tmp_path / "a.pdf"
        f2 = tmp_path / "b.pdf"
        f1.write_bytes(b"resume A")
        f2.write_bytes(b"resume B")
        assert file_hash(str(f1)) != file_hash(str(f2))

    def test_empty_file_has_stable_hash(self, tmp_path):
        f = tmp_path / "empty.pdf"
        f.write_bytes(b"")
        h = file_hash(str(f))
        assert isinstance(h, str) and len(h) == 32  # MD5 hex length

    def test_missing_file_raises_oserror(self, tmp_path):
        with pytest.raises(OSError):
            file_hash(str(tmp_path / "nonexistent.pdf"))

    def test_large_file_chunked(self, tmp_path):
        """超过 CHUNK_SIZE 的文件应正确计算哈希（分块读取）"""
        f = tmp_path / "large.pdf"
        data = b"x" * (1024 * 1024)  # 1 MB
        f.write_bytes(data)
        h = file_hash(str(f))
        assert len(h) == 32


# ── score_filename ────────────────────────────────────────────

class TestScoreFilename:
    def test_chinese_name_scores_higher_than_unknown(self):
        rich = score_filename("产品经理-张三-28岁-北京.pdf")
        poor = score_filename("未知_1.pdf")
        assert rich > poor

    def test_suffix_number_penalized(self):
        original = score_filename("产品经理-李四.pdf")
        copy = score_filename("产品经理-李四_1.pdf")
        assert original > copy

    def test_unknown_pattern_penalized(self):
        unknown = score_filename("未知_5.pdf")
        normal = score_filename("运营专员.pdf")
        assert normal > unknown

    def test_longer_informative_name_scores_higher(self):
        short = score_filename("简历.pdf")
        long_ = score_filename("新媒体运营-王晓明-3年经验-上海.pdf")
        assert long_ > short

    def test_pure_ascii_no_zh_bonus(self):
        ascii_name = score_filename("resume_engineer.pdf")
        zh_name = score_filename("工程师-陈晓.pdf")
        # 中文名有中文加分，应比纯英文得分高（在名字长度相近时）
        assert zh_name > ascii_name


# ── pick_best ─────────────────────────────────────────────────

class TestPickBest:
    def test_picks_original_over_copy(self):
        names = ["项目经理-张伟_1.pdf", "项目经理-张伟.pdf", "项目经理-张伟_2.pdf"]
        assert pick_best(names) == "项目经理-张伟.pdf"

    def test_picks_chinese_over_unknown(self):
        names = ["未知_3.pdf", "数据分析师-李明-北京.pdf"]
        assert pick_best(names) == "数据分析师-李明-北京.pdf"

    def test_single_item_returns_itself(self):
        assert pick_best(["only.pdf"]) == "only.pdf"


# ── collect_hashes ────────────────────────────────────────────

class TestCollectHashes:
    def _make_pdf(self, folder, name, content=b"pdf content"):
        path = os.path.join(folder, name)
        with open(path, "wb") as f:
            f.write(content)

    def test_finds_duplicate_across_folders(self, tmp_path):
        dir_a = tmp_path / "folderA"
        dir_b = tmp_path / "folderB"
        dir_a.mkdir()
        dir_b.mkdir()

        self._make_pdf(str(dir_a), "cv1.pdf", b"same content")
        self._make_pdf(str(dir_b), "cv2.pdf", b"same content")

        result = collect_hashes(str(tmp_path), ["folderA", "folderB"])
        result.pop("__errors__", None)

        dup_groups = {h: v for h, v in result.items() if len(v) > 1}
        assert len(dup_groups) == 1
        files_in_group = {fname for _, fname in list(dup_groups.values())[0]}
        assert files_in_group == {"cv1.pdf", "cv2.pdf"}

    def test_no_duplicate_unique_files(self, tmp_path):
        dir_a = tmp_path / "folderA"
        dir_a.mkdir()
        self._make_pdf(str(dir_a), "cv1.pdf", b"content A")
        self._make_pdf(str(dir_a), "cv2.pdf", b"content B")

        result = collect_hashes(str(tmp_path), ["folderA"])
        result.pop("__errors__", None)
        assert all(len(v) == 1 for v in result.values())

    def test_missing_folder_skipped_silently(self, tmp_path):
        result = collect_hashes(str(tmp_path), ["nonexistent_folder"])
        result.pop("__errors__", None)
        assert result == {}

    def test_non_pdf_files_ignored(self, tmp_path):
        d = tmp_path / "folder"
        d.mkdir()
        (d / "doc.docx").write_bytes(b"word file")
        (d / "resume.pdf").write_bytes(b"pdf file")

        result = collect_hashes(str(tmp_path), ["folder"])
        result.pop("__errors__", None)
        # 只有 pdf 文件被收集
        all_files = [fname for entries in result.values() for _, fname in entries]
        assert "doc.docx" not in all_files
        assert "resume.pdf" in all_files
