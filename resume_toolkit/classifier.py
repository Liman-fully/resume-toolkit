"""
分类模块：半固定分类体系 + 用户自定义扩展
"""

from typing import Optional, Dict, List
from .config import Config, CATEGORY_SYSTEM


def get_all_categories(config: Config = None) -> Dict[str, List[str]]:
    """
    获取所有分类规则（基础分类 + 用户自定义）

    Args:
        config: 配置对象

    Returns:
        分类字典 {分类名: [关键词列表]}
    """
    if config is None:
        config = Config()

    # 合并基础分类和用户自定义分类
    categories = CATEGORY_SYSTEM.copy()
    user_categories = config.get_custom_categories()

    for category, keywords in user_categories.items():
        if category in categories:
            # 扩展现有分类
            categories[category].extend(keywords)
        else:
            # 新增分类
            categories[category] = keywords

    return categories


def classify_by_job_title(job_title: str, config: Config = None) -> str:
    """
    根据职位名称归类

    Args:
        job_title: 职位名称（如"产品经理"、"Java开发工程师"）
        config: 配置对象

    Returns:
        分类名称，如果无法匹配则返回 "待人工归类"
    """
    if not job_title:
        return "待人工归类"

    categories = get_all_categories(config)

    # 遍历所有分类，查找匹配的关键词
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword.lower() in job_title.lower():
                return category

    # 动态分类：如果职位名本身比较明确，直接作为分类
    if len(job_title) >= 2 and not any(char in job_title for char in [" ", "-", "_"]):
        # 简化职位名，去掉常见的后缀
        simplified = job_title.replace("工程师", "").replace("经理", "").replace("总监", "")
        if simplified:
            return simplified

    return "待人工归类"
