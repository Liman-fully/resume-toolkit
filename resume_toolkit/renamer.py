"""
重命名模块：统一文件名格式为 职位-姓名-学历-年龄-城市
"""

from pathlib import Path
from typing import Optional
from .parser import ParseResult
from .config import FILENAME_FORMAT


def rename_resume(
    file_path: Path,
    parse_result: ParseResult,
    dry_run: bool = True,
) -> Optional[Path]:
    """
    重命名简历文件为标准格式：职位-姓名-学历-年龄-城市.pdf

    Args:
        file_path: 原文件路径
        parse_result: 解析结果
        dry_run: 是否干运行

    Returns:
        新文件路径（如果需要重命名），否则返回 None
    """
    # 如果解析不完整，不重命名
    if not parse_result.is_complete():
        return None

    # 生成新文件名
    job_title = parse_result.job_title or "未知职位"
    name = parse_result.name or "未知姓名"
    education = parse_result.education or "未知学历"
    age = parse_result.age or "未知年龄"
    city = parse_result.city or "未知城市"

    # 清理文件名中的非法字符
    illegal_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for char in illegal_chars:
        job_title = job_title.replace(char, "_")
        name = name.replace(char, "_")
        education = education.replace(char, "_")
        city = city.replace(char, "_")

    new_name = f"{job_title}_{name}_{education}_{age}_{city}{file_path.suffix}"
    new_path = file_path.parent / new_name

    # 如果文件名没变，不需要重命名
    if new_name == file_path.name:
        return None

    # 检查目标文件是否已存在
    if new_path.exists():
        # 追加序号
        counter = 1
        while True:
            base_name = new_path.stem
            new_name_with_counter = f"{base_name}_{counter}{file_path.suffix}"
            new_path = file_path.parent / new_name_with_counter
            if not new_path.exists():
                break
            counter += 1

    # 执行重命名（如果不是干运行）
    if not dry_run:
        try:
            file_path.rename(new_path)
        except Exception as e:
            return None

    return new_path
