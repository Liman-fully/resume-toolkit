"""
简历整理工具包 v2.0
支持扫描、解析、去重、归类、重命名、Web UI
"""

__version__ = "2.0.0"
__author__ = "Liman"

from .config import Config, CATEGORY_SYSTEM
from .scanner import scan_resumes, ScanResult
from .parser import parse_resume, ParseResult
from .dedup import deduplicate_files, DedupResult
from .classifier import classify_by_job_title, get_all_categories
from .renamer import rename_resume
from .organizer import organize_resumes, OrganizeResult

__all__ = [
    "Config",
    "CATEGORY_SYSTEM",
    "scan_resumes",
    "ScanResult",
    "parse_resume",
    "ParseResult",
    "deduplicate_files",
    "DedupResult",
    "classify_by_job_title",
    "get_all_categories",
    "rename_resume",
    "organize_resumes",
    "OrganizeResult",
]
