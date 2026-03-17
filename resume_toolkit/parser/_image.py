"""
图片解析器：OCR 识别
"""

try:
    from PIL import Image
    import pytesseract
except ImportError:
    Image = None
    pytesseract = None


def parse_image(file_path: str) -> str:
    """
    解析图片文件，使用 OCR 提取文字

    Args:
        file_path: 图片文件路径

    Returns:
        识别的文本内容
    """
    if Image is None or pytesseract is None:
        return "错误：未安装 Pillow 和 pytesseract，请运行: pip install Pillow pytesseract"

    try:
        img = Image.open(file_path)
        text = pytesseract.image_to_string(img, lang="chi_sim")
        return text
    except Exception as e:
        return f"图片 OCR 错误: {e}"
