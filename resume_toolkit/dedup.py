"""
去重模块：基于 MD5 哈希的文件去重
"""

from typing import List, Dict, Tuple
from pathlib import Path
import hashlib


def _file_hash(file_path: Path, chunk_size: int = 65536) -> str:
    """
    计算文件的 MD5 哈希（分块读取，避免大文件内存溢出）

    Args:
        file_path: 文件路径
        chunk_size: 每次读取的块大小（默认 64KB）

    Returns:
        MD5 哈希字符串
    """
    md5 = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(chunk_size), b""):
                md5.update(chunk)
        return md5.hexdigest()
    except Exception:
        return ""


class DedupResult:
    """去重结果"""

    def __init__(self):
        self.total_files: int = 0
        self.duplicate_groups: int = 0
        self.duplicates_to_delete: int = 0
        self.unique_files: int = 0
        self.errors: List[str] = []


def deduplicate_files(
    files: List[Path],
    dry_run: bool = True,
) -> Tuple[DedupResult, Dict[str, List[Path]]]:
    """
    去重：识别重复文件，保留最优文件名的一份

    Args:
        files: 文件路径列表
        dry_run: 是否干运行（True=不删除，只报告；False=实际删除）

    Returns:
        (DedupResult, hash_to_files) 去重结果和哈希到文件的映射
    """
    result = DedupResult()
    result.total_files = len(files)
    hash_to_files: Dict[str, List[Path]] = {}

    # 计算所有文件的哈希
    for file_path in files:
        try:
            file_hash = _file_hash(file_path)
            if file_hash:
                if file_hash not in hash_to_files:
                    hash_to_files[file_hash] = []
                hash_to_files[file_hash].append(file_path)
        except Exception as e:
            result.errors.append(f"哈希计算失败: {file_path} - {e}")

    # 找出重复组
    duplicate_groups = {h: files for h, files in hash_to_files.items() if len(files) > 1}
    result.duplicate_groups = len(duplicate_groups)

    # 统计唯一文件
    result.unique_files = len(hash_to_files)

    # 决定删除哪些重复文件（保留最优文件名的那份）
    to_delete: List[Path] = []
    for file_hash, file_list in duplicate_groups.items():
        # 保留文件名最短的（通常是最原始的文件名）
        sorted_files = sorted(file_list, key=lambda p: len(p.name))
        keep_file = sorted_files[0]
        for f in sorted_files[1:]:
            to_delete.append(f)

    result.duplicates_to_delete = len(to_delete)

    # 执行删除（如果不是干运行）
    if not dry_run and to_delete:
        for file_path in to_delete:
            try:
                file_path.unlink()
            except Exception as e:
                result.errors.append(f"删除失败: {file_path} - {e}")

    return result, hash_to_files
