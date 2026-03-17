"""
简历解析子模块
"""

from ._pdf import parse_pdf
from ._word import parse_word
from ._image import parse_image
from ._html import parse_html

__all__ = ["parse_pdf", "parse_word", "parse_image", "parse_html"]
