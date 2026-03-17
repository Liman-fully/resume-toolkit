"""
深度扫描模块：递归扫描目录，找到所有简历文件
"""

from typing import List, Set
from pathlib import Path
from .config import SUPPORTED_EXTENSIONS, EXCLUDE_DIRS


class ScanResult:
    """扫描结果"""

    def __init__(self):
        self.total_files: int = 0
        self.files: List[Path] = []
        self.errors: List[str] = []

    def add_file(self, path: Path):
        self.total_files += 1
        self.files.append(path)

    def add_error(self, error: str):
        self.errors.append(error)


def scan_resumes(
    root_dir: str,
    exclude_dirs: Set[str] = None,
    extensions: Set[str] = None,
) -> ScanResult:
    """
    递归扫描目录，找到所有简历文件

    Args:
        root_dir: 根目录路径
        exclude_dirs: 要排除的文件夹名称集合
        extensions: 要包含的文件扩展名集合

    Returns:
        ScanResult 对象，包含所有简历文件路径和错误信息
    """
    if exclude_dirs is None:
        exclude_dirs = EXCLUDE_DIRS
    if extensions is None:
        extensions = SUPPORTED_EXTENSIONS

    result = ScanResult()
    root_path = Path(root_dir)

    if not root_path.exists():
        result.add_error(f"根目录不存在: {root_dir}")
        return result

    if not root_path.is_dir():
        result.add_error(f"路径不是目录: {root_dir}")
        return result

    def _scan_recursive(directory: Path):
        """递归扫描子目录"""
        try:
            for item in directory.iterdir():
                if item.is_file() and item.suffix.lower() in extensions:
                    result.add_file(item)
                elif item.is_dir() and item.name not in exclude_dirs:
                    _scan_recursive(item)
        except PermissionError as e:
            result.add_error(f"无权限访问: {directory} - {e}")
        except Exception as e:
            result.add_error(f"扫描异常: {directory} - {e}")

    _scan_recursive(root_path)
    return result
