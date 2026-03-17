from .config import BASE_DIR, CATEGORY_RULES, FALLBACK_CATEGORY
from .utils import file_hash, score_filename, pick_best, collect_hashes, list_classified_folders
from .dedup import run_dedup, audit_special_folder, DedupResult, FolderAuditResult
from .classify import guess_category, classify_folder, classify_files, ClassifyResult

__all__ = [
    "BASE_DIR", "CATEGORY_RULES", "FALLBACK_CATEGORY",
    "file_hash", "score_filename", "pick_best", "collect_hashes", "list_classified_folders",
    "run_dedup", "audit_special_folder", "DedupResult", "FolderAuditResult",
    "guess_category", "classify_folder", "classify_files", "ClassifyResult",
]
