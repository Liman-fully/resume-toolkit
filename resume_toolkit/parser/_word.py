"""
Word 解析器：支持 .doc 和 .docx
"""

try:
    import docx
except ImportError:
    docx = None


def parse_word(file_path: str) -> str:
    """
    解析 Word 文件，提取文本内容

    Args:
        file_path: Word 文件路径

    Returns:
        提取的文本内容
    """
    if docx is None:
        return "错误：未安装 python-docx，请运行: pip install python-docx"

    try:
        doc = docx.Document(file_path)
        text_parts = []
        for para in doc.paragraphs:
            text_parts.append(para.text)
        return "\n".join(text_parts)
    except Exception as e:
        return f"Word 解析错误: {e}"
