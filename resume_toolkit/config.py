"""
配置模块：基础分类体系 + 用户自定义扩展
"""

from typing import Dict, List
from pathlib import Path
import os
import json

# 默认简历库路径（可通过环境变量覆盖）
DEFAULT_BASE_DIR = str(Path.home() / "简历库")


class Config:
    """全局配置"""

    def __init__(self, base_dir: str = None):
        self.base_dir = base_dir or os.getenv("RESUME_BASE_DIR", DEFAULT_BASE_DIR)
        self.user_config_file = Path.home() / ".resume-toolkit" / "user_config.json"
        self._user_rules = self._load_user_rules()

    def _load_user_rules(self) -> Dict:
        """加载用户自定义规则"""
        if not self.user_config_file.exists():
            return {"custom_categories": {}, "custom_keywords": {}}
        try:
            with open(self.user_config_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"custom_categories": {}, "custom_keywords": {}}

    def save_user_rules(self):
        """保存用户自定义规则"""
        self.user_config_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.user_config_file, "w", encoding="utf-8") as f:
            json.dump(self._user_rules, f, ensure_ascii=False, indent=2)

    def get_custom_categories(self) -> Dict[str, List[str]]:
        """获取用户自定义分类"""
        return self._user_rules.get("custom_categories", {})

    def add_custom_category(self, category: str, keywords: List[str]):
        """添加自定义分类"""
        if "custom_categories" not in self._user_rules:
            self._user_rules["custom_categories"] = {}
        self._user_rules["custom_categories"][category] = keywords
        self.save_user_rules()

    def add_custom_keywords(self, category: str, keywords: List[str]):
        """向现有分类添加自定义关键词"""
        if "custom_keywords" not in self._user_rules:
            self._user_rules["custom_keywords"] = {}
        if category not in self._user_rules["custom_keywords"]:
            self._user_rules["custom_keywords"][category] = []
        self._user_rules["custom_keywords"][category].extend(keywords)
        self.save_user_rules()


# 基础分类体系（半固定：用户可扩展，不可删除基础）
CATEGORY_SYSTEM: Dict[str, List[str]] = {
    "技术研发": [
        "软件工程师", "开发工程师", "前端", "后端", "全栈", "Java", "Python", "Go", "C++",
        "Android", "iOS", "移动端", "测试工程师", "QA", "SDET", "运维", "DevOps",
        "架构师", "技术总监", "CTO", "算法工程师", "数据开发", "大数据", "区块链",
    ],
    "产品经理": [
        "产品经理", "产品总监", "CPO", "需求分析", "产品规划", "产品运营",
    ],
    "设计创意": [
        "UI设计师", "UX设计师", "交互设计", "视觉设计", "平面设计", "插画",
        "动效设计", "设计总监", "用户体验",
    ],
    "运营": [
        "新媒体运营", "内容运营", "社群运营", "用户运营", "活动运营", "产品运营",
        "运营总监", "COO",
    ],
    "市场营销": [
        "市场营销", "品牌策划", "市场推广", "销售", "销售总监", "BD", "商务拓展",
        "公关", "媒介", "SEO", "SEM",
    ],
    "数据分析": [
        "数据分析师", "数据科学家", "商业分析", "BI", "数据产品经理",
    ],
    "人力资源": [
        "HR", "人力资源", "招聘", "HRBP", "薪酬福利", "培训", "组织发展",
    ],
    "财务法务": [
        "财务", "会计", "出纳", "审计", "法务", "合规", "投资", "融资",
    ],
    "行政": [
        "行政", "前台", "总助", "办公室",
    ],
    "供应链": [
        "供应链", "采购", "物流", "仓储", "跨境电商", "电商运营",
    ],
}

# 支持的文件扩展名
SUPPORTED_EXTENSIONS = {".pdf", ".doc", ".docx", ".jpg", ".jpeg", ".png", ".bmp", ".html", ".htm"}

# 扫描时排除的文件夹
EXCLUDE_DIRS = {".git", "__pycache__", "node_modules", ".venv", "venv", "venv2"}

# 文件名格式：职位-姓名-学历-年龄-城市
FILENAME_FORMAT = "{job_title}_{name}_{education}_{age}_{city}"
