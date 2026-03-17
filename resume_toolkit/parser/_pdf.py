"""
PDF 解析器：支持文字提取和 OCR
"""

try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None


def parse_pdf(file_path: str) -> str:
    """
    解析 PDF 文件，提取文本内容

    Args:
        file_path: PDF 文件路径

    Returns:
        提取的文本内容
    """
    if fitz is None:
        return "错误：未安装 PyMuPDF，请运行: pip install PyMuPDF"

    try:
        doc = fitz.open(file_path)
        text_parts = []
        for page in doc:
            text_parts.append(page.get_text())
        doc.close()
        return "\n".join(text_parts)
    except Exception as e:
        return f"PDF 解析错误: {e}"
