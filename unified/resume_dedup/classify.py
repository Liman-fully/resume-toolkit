#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动归类模块。
- 按文件名关键词将简历归入对应分类文件夹
- 支持 dry_run 预览
- 归类结果结构化返回，方便测试验证
"""

import os
import shutil
from dataclasses import dataclass, field
from typing import Optional

from .config import BASE_DIR, CATEGORY_RULES, FALLBACK_CATEGORY


# ── 归类核心 ──────────────────────────────────────────────────

def guess_category(filename: str) -> str:
    """
    根据文件名关键词推断所属分类。
    匹配逻辑：大小写不敏感，按 CATEGORY_RULES 顺序，首个命中即返回。
    未命中时返回 FALLBACK_CATEGORY。

    设计说明：
    - 调整关键词优先级 → 修改 config.py 中 CATEGORY_RULES 的顺序
    - 新增关键词 → 在对应类别列表追加字符串
    """
    name_lower = filename.lower()
    for category, keywords in CATEGORY_RULES:
        for kw in keywords:
            if kw.lower() in name_lower:
                return category
    return FALLBACK_CATEGORY


# ── 结果数据结构 ──────────────────────────────────────────────

@dataclass
class ClassifyResult:
    dry_run: bool
    moved: list[tuple[str, str, str]] = field(default_factory=list)
    # (source_folder, filename, target_category)
    skipped: list[tuple[str, str, str]] = field(default_factory=list)
    # (source_folder, filename, reason)
    errors: list[str] = field(default_factory=list)

    @property
    def moved_count(self) -> int:
        return len(self.moved)

    def category_stats(self) -> dict[str, int]:
        """按目标分类统计数量。"""
        stats: dict[str, int] = {}
        for _, _, cat in self.moved:
            stats[cat] = stats.get(cat, 0) + 1
        return stats

    def summary(self) -> str:
        mode = "[DRY-RUN 预览]" if self.dry_run else "[已执行]"
        lines = [
            f"{mode} 自动归类结果",
            f"  已归类：{self.moved_count}",
            f"  跳过：{len(self.skipped)}",
        ]
        if self.errors:
            lines.append(f"  ⚠ 出错：{len(self.errors)}")
        lines.append("\n  各分类数量：")
        for cat, cnt in sorted(self.category_stats().items()):
            lines.append(f"    {cat}: {cnt}")
        return "\n".join(lines)


# ── 执行函数 ──────────────────────────────────────────────────

def classify_folder(
    source_folder: str,
    base_dir: str = BASE_DIR,
    *,
    dry_run: bool = True,
    overwrite: bool = False,
) -> ClassifyResult:
    """
    将 source_folder 内的简历按关键词归类到 base_dir 下对应的分类文件夹。

    Args:
        source_folder:  相对 base_dir 的源文件夹名（如 "_待分类" 或 "_重复简历"）
        base_dir:       简历库根目录
        dry_run:        True = 仅预览，不移动文件（默认）
        overwrite:      目标文件已存在时是否覆盖（默认不覆盖，追加 _dup 后缀）

    Returns:
        ClassifyResult
    """
    result = ClassifyResult(dry_run=dry_run)
    source_path = os.path.join(base_dir, source_folder)

    if not os.path.isdir(source_path):
        result.errors.append(f"源文件夹不存在：{source_path}")
        return result

    for fname in sorted(os.listdir(source_path)):
        if not any(fname.lower().endswith(ext) for ext in (".pdf",)):
            continue

        category = guess_category(fname)
        target_dir = os.path.join(base_dir, category)
        src = os.path.join(source_path, fname)
        dst = os.path.join(target_dir, fname)

        # 解决目标冲突
        if os.path.exists(dst) and not overwrite:
            name, ext = os.path.splitext(fname)
            # 尝试最多 99 个后缀
            for i in range(1, 100):
                candidate = os.path.join(target_dir, f"{name}_dup{i}{ext}")
                if not os.path.exists(candidate):
                    dst = candidate
                    break
            else:
                result.skipped.append((source_folder, fname, "目标冲突且无可用后缀"))
                continue

        result.moved.append((source_folder, fname, category))

        if not dry_run:
            os.makedirs(target_dir, exist_ok=True)
            try:
                shutil.move(src, dst)
            except OSError as e:
                result.errors.append(f"移动失败 {fname}: {e}")
                result.moved.pop()  # 回退记录

    return result


def classify_files(
    filenames: list[str],
    source_folder: str,
    base_dir: str = BASE_DIR,
    *,
    dry_run: bool = True,
    overwrite: bool = False,
) -> ClassifyResult:
    """
    对指定文件名列表进行归类（可与去重结果联动）。
    等价于 classify_folder，但只处理 filenames 中的文件。
    """
    result = ClassifyResult(dry_run=dry_run)
    source_path = os.path.join(base_dir, source_folder)

    for fname in filenames:
        category = guess_category(fname)
        target_dir = os.path.join(base_dir, category)
        src = os.path.join(source_path, fname)
        dst = os.path.join(target_dir, fname)

        if not os.path.exists(src):
            result.skipped.append((source_folder, fname, "源文件不存在"))
            continue

        if os.path.exists(dst) and not overwrite:
            name, ext = os.path.splitext(fname)
            for i in range(1, 100):
                candidate = os.path.join(target_dir, f"{name}_dup{i}{ext}")
                if not os.path.exists(candidate):
                    dst = candidate
                    break
            else:
                result.skipped.append((source_folder, fname, "目标冲突"))
                continue

        result.moved.append((source_folder, fname, category))

        if not dry_run:
            os.makedirs(target_dir, exist_ok=True)
            try:
                shutil.move(src, dst)
            except OSError as e:
                result.errors.append(f"移动失败 {fname}: {e}")
                result.moved.pop()

    return result
