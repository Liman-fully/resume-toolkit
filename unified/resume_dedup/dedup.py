#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
去重核心逻辑模块。
- 支持 dry_run 模式（默认），不传 dry_run=False 不会修改任何文件。
- 所有文件操作包裹 try/except，单文件失败不中断全局流程。
- 返回结构化结果，方便日志、测试、CLI 各层独立消费。
"""

import os
import shutil
from dataclasses import dataclass, field
from typing import Optional

from .config import BASE_DIR, FALLBACK_CATEGORY
from .utils import collect_hashes, list_classified_folders, pick_best


# ── 数据结构 ──────────────────────────────────────────────────

@dataclass
class DedupResult:
    """去重操作结果，dry_run=True 时所有 deleted/moved 为预期值，不代表已执行。"""
    dry_run: bool
    scanned: int = 0
    dup_groups: int = 0
    deleted: list[str] = field(default_factory=list)   # "folder/filename"
    kept: list[str] = field(default_factory=list)      # "folder/filename"
    errors: list[str] = field(default_factory=list)    # 错误信息

    @property
    def deleted_count(self) -> int:
        return len(self.deleted)

    def summary(self) -> str:
        mode = "[DRY-RUN 预览]" if self.dry_run else "[已执行]"
        lines = [
            f"{mode} 全库去重扫描结果",
            f"  扫描文件：{self.scanned}",
            f"  重复组数：{self.dup_groups}",
            f"  可删除副本：{self.deleted_count}",
        ]
        if self.errors:
            lines.append(f"  ⚠ 出错文件：{len(self.errors)}")
        return "\n".join(lines)


# ── 核心去重函数 ──────────────────────────────────────────────

def run_dedup(
    base_dir: str = BASE_DIR,
    *,
    dry_run: bool = True,
    extra_folders: Optional[list[str]] = None,
) -> DedupResult:
    """
    扫描 base_dir 下所有已分类文件夹，找出内容重复的文件组。
    每组保留评分最高的一份，删除其余副本。

    Args:
        base_dir:       简历库根目录
        dry_run:        True = 仅预览，不修改文件（默认）
        extra_folders:  额外扫描的文件夹名列表（如 ["_重复简历"]）

    Returns:
        DedupResult 对象
    """
    result = DedupResult(dry_run=dry_run)

    folders = list_classified_folders(base_dir)
    if extra_folders:
        folders += [f for f in extra_folders if f not in folders]

    hash_map = collect_hashes(base_dir, folders)

    # 提取扫描错误
    errors_raw = hash_map.pop("__errors__", [])
    for folder, fname, err in errors_raw:  # type: ignore[misc]
        result.errors.append(f"读取失败 {folder}/{fname}: {err}")

    result.scanned = sum(len(v) for v in hash_map.values())

    # 找出重复组
    dup_groups = {h: v for h, v in hash_map.items() if len(v) > 1}
    result.dup_groups = len(dup_groups)

    for h, copies in dup_groups.items():
        # 挑出保留文件
        best_fname = pick_best([fname for _, fname in copies])
        best_entry = next((folder, fname) for folder, fname in copies if fname == best_fname)

        result.kept.append(f"{best_entry[0]}/{best_entry[1]}")

        for folder, fname in copies:
            if (folder, fname) == best_entry:
                continue
            fpath = os.path.join(base_dir, folder, fname)
            result.deleted.append(f"{folder}/{fname}")

            if not dry_run:
                try:
                    os.remove(fpath)
                except OSError as e:
                    result.errors.append(f"删除失败 {folder}/{fname}: {e}")

    return result


# ── 特殊文件夹处理 ────────────────────────────────────────────

@dataclass
class FolderAuditResult:
    """对某个特殊文件夹（如 _备份_重复简历）的审计结果。"""
    folder: str
    total: int = 0
    overlap_with_classified: int = 0
    unique_only_here: int = 0
    unique_filenames: list[str] = field(default_factory=list)
    verdict: str = ""           # "pure_backup" | "has_unique" | "not_found"
    dry_run: bool = True
    deleted_folder: bool = False
    moved_files: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    def summary(self) -> str:
        mode = "[DRY-RUN]" if self.dry_run else "[已执行]"
        if self.verdict == "not_found":
            return f"{mode} {self.folder} 不存在，跳过"
        lines = [
            f"{mode} 审计 {self.folder}",
            f"  文件总数：{self.total}",
            f"  与已分类重复：{self.overlap_with_classified}",
            f"  仅此处独有：{self.unique_only_here}",
            f"  结论：{'纯备份，可安全删除' if self.verdict == 'pure_backup' else '有独有文件，已移至 ' + FALLBACK_CATEGORY}",
        ]
        return "\n".join(lines)


def audit_special_folder(
    folder_name: str,
    base_dir: str = BASE_DIR,
    *,
    dry_run: bool = True,
) -> FolderAuditResult:
    """
    审计一个特殊文件夹（如 _备份_重复简历 / _重复简历）：
    - 与已分类文件夹做哈希比对
    - 若全部重复 → 标记为 pure_backup，dry_run=False 时删除整个文件夹
    - 若有独有文件 → 标记为 has_unique，dry_run=False 时将独有文件移入 FALLBACK_CATEGORY

    Args:
        folder_name:  要审计的文件夹名（相对 base_dir）
        base_dir:     简历库根目录
        dry_run:      True = 仅预览

    Returns:
        FolderAuditResult
    """
    res = FolderAuditResult(folder=folder_name, dry_run=dry_run)
    folder_path = os.path.join(base_dir, folder_name)

    if not os.path.isdir(folder_path):
        res.verdict = "not_found"
        return res

    # 收集特殊文件夹的哈希
    special_map = collect_hashes(base_dir, [folder_name])
    special_map.pop("__errors__", None)
    # hash -> first filename in special folder
    special_hashes: dict[str, str] = {
        h: entries[0][1] for h, entries in special_map.items()
    }
    res.total = len(special_hashes)

    # 收集已分类文件夹的哈希（不含当前特殊文件夹）
    classified_folders = list_classified_folders(base_dir)
    classified_map = collect_hashes(base_dir, classified_folders)
    classified_map.pop("__errors__", None)
    classified_hashes: set[str] = set(classified_map.keys())

    overlap = set(special_hashes.keys()) & classified_hashes
    unique = set(special_hashes.keys()) - classified_hashes

    res.overlap_with_classified = len(overlap)
    res.unique_only_here = len(unique)
    res.unique_filenames = [special_hashes[h] for h in unique]

    if unique:
        res.verdict = "has_unique"
        if not dry_run:
            fallback_dir = os.path.join(base_dir, FALLBACK_CATEGORY)
            os.makedirs(fallback_dir, exist_ok=True)
            for h in unique:
                fname = special_hashes[h]
                src = os.path.join(folder_path, fname)
                dst = os.path.join(fallback_dir, fname)
                # 目标冲突时追加 _rescued 后缀
                if os.path.exists(dst):
                    name, ext = os.path.splitext(fname)
                    dst = os.path.join(fallback_dir, f"{name}_rescued{ext}")
                try:
                    shutil.move(src, dst)
                    res.moved_files.append(fname)
                except OSError as e:
                    res.errors.append(f"移动失败 {fname}: {e}")
            # 删除已重复的文件
            for h in overlap:
                fpath = os.path.join(folder_path, special_hashes[h])
                try:
                    if os.path.exists(fpath):
                        os.remove(fpath)
                except OSError as e:
                    res.errors.append(f"删除失败 {special_hashes[h]}: {e}")
            # 清理空文件夹
            remaining = [f for f in os.listdir(folder_path)
                         if any(f.lower().endswith(ext) for ext in (".pdf",))]
            if not remaining:
                try:
                    shutil.rmtree(folder_path)
                    res.deleted_folder = True
                except OSError as e:
                    res.errors.append(f"删除文件夹失败：{e}")
    else:
        res.verdict = "pure_backup"
        if not dry_run:
            try:
                shutil.rmtree(folder_path)
                res.deleted_folder = True
            except OSError as e:
                res.errors.append(f"删除文件夹失败：{e}")

    return res
