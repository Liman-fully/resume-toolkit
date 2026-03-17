#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
公共工具模块：文件哈希、文件名评分、文件扫描。
所有函数均为纯函数或无副作用工具，方便单元测试。
"""

import hashlib
import os
import re
from collections import defaultdict
from typing import Iterator

from .config import INTERNAL_FOLDERS, RESUME_EXTENSIONS


# ── 文件哈希 ──────────────────────────────────────────────────

CHUNK_SIZE = 65536  # 64 KB，平衡内存与 I/O 效率


def file_hash(path: str) -> str:
    """
    计算文件 MD5 哈希（分块读取，不占用大内存）。
    对损坏 / 无权限文件抛出 OSError，由调用方决定如何处理。
    """
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(CHUNK_SIZE), b""):
            h.update(chunk)
    return h.hexdigest()


# ── 文件名评分（保留策略）────────────────────────────────────

# 带 _数字 后缀的文件名（如 xxx_1.pdf）通常是系统自动重命名的副本
_SUFFIX_PATTERN = re.compile(r"_\d+\.[^.]+$")
# 纯 "未知" 类文件名，信息量极低
_UNKNOWN_PATTERN = re.compile(r"^未知[_\d]*\.", re.IGNORECASE)


def score_filename(filename: str) -> int:
    """
    对文件名打分，分越高表示保留价值越高。
    评分规则（可独立迭代，不影响其他模块）：

    +20  有明确中文姓名或职位（中文字符数 >= 4）
    +5   含任意中文字符
    -10  带 _数字 后缀（系统重命名副本）
    -15  纯"未知"文件名
    +len 文件名长度奖励（上限 40，鼓励信息丰富）
    """
    score = 0
    name_without_ext = os.path.splitext(filename)[0]

    # 中文字符数
    zh_count = sum(1 for c in filename if "\u4e00" <= c <= "\u9fff")
    if zh_count >= 4:
        score += 20
    elif zh_count > 0:
        score += 5

    # 副本后缀扣分
    if _SUFFIX_PATTERN.search(filename):
        score -= 10

    # 纯"未知"扣分
    if _UNKNOWN_PATTERN.match(filename):
        score -= 15

    # 文件名长度（去掉扩展名后）
    score += min(len(name_without_ext), 40)

    return score


def pick_best(filenames: list[str]) -> str:
    """从一组重复文件名中挑选得分最高的保留。"""
    return max(filenames, key=score_filename)


# ── 文件扫描 ──────────────────────────────────────────────────

def iter_resume_files(folder: str) -> Iterator[str]:
    """
    遍历 folder 下（非递归）所有简历文件，返回文件名。
    只包含 RESUME_EXTENSIONS 中定义的扩展名。
    """
    try:
        entries = os.listdir(folder)
    except PermissionError as e:
        raise PermissionError(f"无权限读取文件夹：{folder}") from e

    for name in sorted(entries):
        if any(name.lower().endswith(ext) for ext in RESUME_EXTENSIONS):
            yield name


def collect_hashes(base_dir: str, folders: list[str]) -> dict[str, list[tuple[str, str]]]:
    """
    扫描指定文件夹列表，返回 hash -> [(folder, filename), ...] 映射。

    Args:
        base_dir:  简历库根目录
        folders:   要扫描的文件夹名列表

    Returns:
        字典，key 为 MD5 哈希，value 为 (文件夹名, 文件名) 元组列表。
        value 长度 > 1 表示该内容有多份副本。

    Raises:
        不会因单个文件失败而中断；失败文件记录在返回的 errors 列表。
    """
    hash_map: dict[str, list[tuple[str, str]]] = defaultdict(list)
    errors: list[tuple[str, str, str]] = []  # (folder, filename, error_msg)

    for folder in folders:
        folder_path = os.path.join(base_dir, folder)
        if not os.path.isdir(folder_path):
            continue
        for fname in iter_resume_files(folder_path):
            fpath = os.path.join(folder_path, fname)
            try:
                h = file_hash(fpath)
                hash_map[h].append((folder, fname))
            except OSError as e:
                errors.append((folder, fname, str(e)))

    if errors:
        # 将错误挂在返回值上，调用方可选择记录或报警
        hash_map["__errors__"] = errors  # type: ignore[assignment]

    return dict(hash_map)


def list_classified_folders(base_dir: str) -> list[str]:
    """返回 base_dir 下所有「已分类」文件夹名（排除内部特殊文件夹和隐藏目录）。"""
    result = []
    try:
        entries = os.listdir(base_dir)
    except OSError:
        return result

    for name in sorted(entries):
        if name.startswith("_") or name.startswith("."):
            continue
        if name in INTERNAL_FOLDERS:
            continue
        full = os.path.join(base_dir, name)
        if os.path.isdir(full):
            result.append(name)
    return result
