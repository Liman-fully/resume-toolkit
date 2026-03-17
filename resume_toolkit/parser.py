"""
简历解析模块：从简历文件中提取结构化信息
支持格式：PDF, Word, 图片, 网页
"""

from dataclasses import dataclass, field
from typing import Optional, List
from pathlib import Path
import re


@dataclass
class ParseResult:
    """解析结果"""

    name: Optional[str] = None  # 姓名
    job_title: Optional[str] = None  # 职位
    education: Optional[str] = None  # 学历
    age: Optional[str] = None  # 年龄
    city: Optional[str] = None  # 城市
    raw_text: str = ""  # 原始文本（用于调试）

    def is_complete(self) -> bool:
        """检查是否解析完整（所有字段都有值）"""
        return all([self.name, self.job_title, self.education, self.age, self.city])

    def missing_fields(self) -> List[str]:
        """返回缺失的字段列表"""
        fields = []
        if not self.name:
            fields.append("姓名")
        if not self.job_title:
            fields.append("职位")
        if not self.education:
            fields.append("学历")
        if not self.age:
            fields.append("年龄")
        if not self.city:
            fields.append("城市")
        return fields


def parse_resume(file_path: Path) -> ParseResult:
    """
    解析简历文件，提取结构化信息

    Args:
        file_path: 简历文件路径

    Returns:
        ParseResult 对象
    """
    # 根据文件扩展名选择解析器
    suffix = file_path.suffix.lower()

    if suffix == ".pdf":
        from .parser._pdf import parse_pdf
        raw_text = parse_pdf(str(file_path))
    elif suffix in {".doc", ".docx"}:
        from .parser._word import parse_word
        raw_text = parse_word(str(file_path))
    elif suffix in {".jpg", ".jpeg", ".png", ".bmp"}:
        from .parser._image import parse_image
        raw_text = parse_image(str(file_path))
    elif suffix in {".html", ".htm"}:
        from .parser._html import parse_html
        raw_text = parse_html(str(file_path))
    else:
        return ParseResult(raw_text=f"不支持的文件格式: {suffix}")

    # 从文本中提取结构化信息
    result = extract_info_from_text(raw_text)
    result.raw_text = raw_text
    return result


def extract_info_from_text(text: str) -> ParseResult:
    """
    从文本中提取简历信息（正则匹配）

    Args:
        text: 简历文本内容

    Returns:
        ParseResult 对象
    """
    result = ParseResult()

    # 姓名提取（常见模式：姓名：xxx, 姓名：xxx, xxx, xxx ）
    name_patterns = [
        r"姓名[：:]\s*([^\s\n]{2,4})",
        r"个人简介[：:]\s*([^\s\n]{2,4})",
        r"求职意向[：:]\s*([^\s\n]{2,4})",
    ]
    for pattern in name_patterns:
        match = re.search(pattern, text)
        if match:
            result.name = match.group(1)
            break

    # 职位提取
    job_patterns = [
        r"求职意向[：:].*职位[：:]\s*([^\s\n]+)",
        r"应聘职位[：:]\s*([^\s\n]+)",
        r"期望职位[：:]\s*([^\s\n]+)",
    ]
    for pattern in job_patterns:
        match = re.search(pattern, text)
        if match:
            result.job_title = match.group(1)
            break

    # 学历提取
    edu_patterns = [
        r"(博士|硕士|研究生|本科|大专|专科|高中|初中)",
        r"学历[：:]\s*([^\s\n]+)",
    ]
    for pattern in edu_patterns:
        match = re.search(pattern, text)
        if match:
            result.education = match.group(1)
            break

    # 年龄提取
    age_patterns = [
        r"(\d{2})\s*[岁岁]",
        r"年龄[：:]\s*(\d{2})",
        r"(\d{1,2})岁",
    ]
    for pattern in age_patterns:
        match = re.search(pattern, text)
        if match:
            result.age = match.group(1)
            break

    # 城市提取
    city_patterns = [
        r"(北京|上海|广州|深圳|杭州|南京|苏州|成都|重庆|武汉|西安|天津|青岛|大连)",
        r"城市[：:]\s*([^\s\n]+)",
        r"工作地点[：:]\s*([^\s\n]+)",
    ]
    for pattern in city_patterns:
        match = re.search(pattern, text)
        if match:
            result.city = match.group(1)
            break

    return result
