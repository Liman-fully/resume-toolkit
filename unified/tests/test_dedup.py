#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dedup 模块单元测试
"""

import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from resume_dedup.dedup import run_dedup, audit_special_folder


def make_pdf(folder, name, content=b"pdf"):
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, name)
    with open(path, "wb") as f:
        f.write(content)
    return path


# ── run_dedup ─────────────────────────────────────────────────

class TestRunDedup:
    def test_dry_run_does_not_delete(self, tmp_path):
        """dry_run=True 时文件不应被删除"""
        d = tmp_path / "00_测试分类"
        d.mkdir()
        make_pdf(str(d), "cv1.pdf", b"same")
        make_pdf(str(d), "cv2.pdf", b"same")

        result = run_dedup(base_dir=str(tmp_path), dry_run=True)
        # 文件仍然存在
        assert (d / "cv1.pdf").exists()
        assert (d / "cv2.pdf").exists()
        assert result.dry_run is True
        assert result.deleted_count == 1

    def test_execute_deletes_duplicate(self, tmp_path):
        """dry_run=False 时重复文件应被删除"""
        d = tmp_path / "01_测试"
        d.mkdir()
        make_pdf(str(d), "工程师-张三.pdf", b"dup content")
        make_pdf(str(d), "工程师-张三_1.pdf", b"dup content")

        result = run_dedup(base_dir=str(tmp_path), dry_run=False)
        # 只保留一个
        remaining = list((d).iterdir())
        assert len(remaining) == 1
        assert result.deleted_count == 1
        assert result.dry_run is False

    def test_keeps_best_filename(self, tmp_path):
        """应保留评分更高的文件名（无 _数字 后缀的）"""
        d = tmp_path / "02_测试"
        d.mkdir()
        make_pdf(str(d), "产品经理-李四.pdf", b"same content")
        make_pdf(str(d), "产品经理-李四_1.pdf", b"same content")

        result = run_dedup(base_dir=str(tmp_path), dry_run=False)
        remaining = [f.name for f in d.iterdir()]
        assert "产品经理-李四.pdf" in remaining
        assert "产品经理-李四_1.pdf" not in remaining

    def test_no_duplicates_returns_zero(self, tmp_path):
        d = tmp_path / "03_测试"
        d.mkdir()
        make_pdf(str(d), "a.pdf", b"content a")
        make_pdf(str(d), "b.pdf", b"content b")

        result = run_dedup(base_dir=str(tmp_path), dry_run=True)
        assert result.deleted_count == 0
        assert result.dup_groups == 0

    def test_error_file_recorded_not_crash(self, tmp_path):
        """单文件权限问题不应导致整体崩溃"""
        d = tmp_path / "04_测试"
        d.mkdir()
        p = make_pdf(str(d), "locked.pdf", b"content")
        os.chmod(p, 0o000)  # 无权限

        try:
            result = run_dedup(base_dir=str(tmp_path), dry_run=True)
            assert any("locked.pdf" in e for e in result.errors)
        finally:
            os.chmod(p, 0o644)  # 恢复权限，让 pytest 可以清理

    def test_cross_folder_duplicate_detected(self, tmp_path):
        """跨文件夹重复应被检测"""
        d1 = tmp_path / "05_A"
        d2 = tmp_path / "06_B"
        d1.mkdir(); d2.mkdir()
        make_pdf(str(d1), "cv_original.pdf", b"cross dup")
        make_pdf(str(d2), "cv_copy.pdf", b"cross dup")

        result = run_dedup(base_dir=str(tmp_path), dry_run=True)
        assert result.dup_groups == 1
        assert result.deleted_count == 1


# ── audit_special_folder ──────────────────────────────────────

class TestAuditSpecialFolder:
    def test_pure_backup_detected(self, tmp_path):
        """所有文件已在分类文件夹中时，判定为 pure_backup"""
        classified = tmp_path / "01_分类"
        backup = tmp_path / "_备份"
        classified.mkdir(); backup.mkdir()

        make_pdf(str(classified), "cv.pdf", b"content")
        make_pdf(str(backup), "cv_backup.pdf", b"content")  # 同内容不同名

        result = audit_special_folder("_备份", base_dir=str(tmp_path), dry_run=True)
        assert result.verdict == "pure_backup"
        assert result.unique_only_here == 0

    def test_has_unique_detected(self, tmp_path):
        """有独有文件时，判定为 has_unique"""
        classified = tmp_path / "01_分类"
        special = tmp_path / "_特殊"
        classified.mkdir(); special.mkdir()

        make_pdf(str(classified), "cv1.pdf", b"classified content")
        make_pdf(str(special), "cv_unique.pdf", b"unique content")

        result = audit_special_folder("_特殊", base_dir=str(tmp_path), dry_run=True)
        assert result.verdict == "has_unique"
        assert result.unique_only_here == 1
        assert "cv_unique.pdf" in result.unique_filenames

    def test_execute_pure_backup_deletes_folder(self, tmp_path):
        """dry_run=False 时，纯备份文件夹应被删除"""
        classified = tmp_path / "01_分类"
        backup = tmp_path / "_备份"
        classified.mkdir(); backup.mkdir()

        make_pdf(str(classified), "cv.pdf", b"same")
        make_pdf(str(backup), "cv_bk.pdf", b"same")

        result = audit_special_folder("_备份", base_dir=str(tmp_path), dry_run=False)
        assert result.deleted_folder is True
        assert not backup.exists()

    def test_not_found_folder(self, tmp_path):
        result = audit_special_folder("_不存在", base_dir=str(tmp_path), dry_run=True)
        assert result.verdict == "not_found"
