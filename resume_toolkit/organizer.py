"""
整合模块：完整的简历整理流程
扫描 → 解析 → 去重 → 归类 → 重命名 → 移动
"""

from pathlib import Path
from typing import List, Dict
from .scanner import scan_resumes, ScanResult
from .parser import parse_resume, ParseResult
from .dedup import deduplicate_files, DedupResult
from .classifier import classify_by_job_title
from .renamer import rename_resume
from .config import Config


class OrganizeResult:
    """整理结果"""

    def __init__(self):
        self.scan_result: ScanResult = None
        self.dedup_result: DedupResult = None
        self.moved_count: int = 0
        self.renamed_count: int = 0
        self.manual_review_count: int = 0
        self.errors: List[str] = []

    def summary(self) -> str:
        """生成结果摘要"""
        lines = [
            "=== 简历整理结果 ===",
            f"扫描文件数: {self.scan_result.total_files if self.scan_result else 0}",
            f"去重复文件数: {self.dedup_result.duplicates_to_delete if self.dedup_result else 0}",
            f"整理移动数: {self.moved_count}",
            f"重命名数: {self.renamed_count}",
            f"待人工审核: {self.manual_review_count}",
            f"错误数: {len(self.errors)}",
        ]
        return "\n".join(lines)


def organize_resumes(
    source_dir: str,
    target_dir: str,
    dry_run: bool = True,
    config: Config = None,
) -> OrganizeResult:
    """
    完整的简历整理流程

    Args:
        source_dir: 源目录（扫描所有简历）
        target_dir: 目标目录（按分类存放）
        dry_run: 是否干运行
        config: 配置对象

    Returns:
        OrganizeResult 整理结果
    """
    result = OrganizeResult()

    if config is None:
        config = Config()

    target_path = Path(target_dir)
    target_path.mkdir(parents=True, exist_ok=True)

    # 1. 扫描所有简历
    print("📂 扫描简历文件...")
    scan_result = scan_resumes(source_dir)
    result.scan_result = scan_result

    if scan_result.errors:
        result.errors.extend(scan_result.errors)

    print(f"  找到 {scan_result.total_files} 个简历文件")

    if not scan_result.files:
        print("  未找到简历文件，退出")
        return result

    # 2. 去重
    print("🔍 去重处理...")
    dedup_result, hash_to_files = deduplicate_files(scan_result.files, dry_run=dry_run)
    result.dedup_result = dedup_result

    print(f"  发现 {dedup_result.duplicate_groups} 组重复，删除 {dedup_result.duplicates_to_delete} 个文件")
    print(f"  保留 {dedup_result.unique_files} 个唯一文件")

    # 3. 解析、归类、重命名、移动
    print("📝 解析并整理...")
    manual_review_dir = target_path / "待人工审核"
    if not dry_run:
        manual_review_dir.mkdir(exist_ok=True)

    for file_path in scan_result.files:
        try:
            # 跳过已删除的重复文件
            if not file_path.exists():
                continue

            # 解析简历
            parse_result = parse_resume(file_path)

            # 如果解析不完整，放入待人工审核
            if not parse_result.is_complete():
                target_file = manual_review_dir / file_path.name
                if not dry_run:
                    file_path.rename(target_file)
                result.manual_review_count += 1
                continue

            # 归类
            category = classify_by_job_title(parse_result.job_title, config)
            category_dir = target_path / category
            if not dry_run:
                category_dir.mkdir(exist_ok=True)

            # 重命名
            new_name_path = rename_resume(file_path, parse_result, dry_run=dry_run)

            # 移动
            target_file = category_dir / (new_name_path.name if new_name_path else file_path.name)
            if not dry_run:
                if new_name_path:
                    new_name_path.rename(target_file)
                else:
                    file_path.rename(target_file)

            result.moved_count += 1
            if new_name_path:
                result.renamed_count += 1

        except Exception as e:
            result.errors.append(f"处理失败: {file_path} - {e}")

    print(f"  移动 {result.moved_count} 个文件")
    print(f"  重命名 {result.renamed_count} 个文件")
    print(f"  待人工审核: {result.manual_review_count} 个")

    return result
