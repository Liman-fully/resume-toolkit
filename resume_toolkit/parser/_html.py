"""
HTML 解析器：从网页简历提取文字
"""

from bs4 import BeautifulSoup


def parse_html(file_path: str) -> str:
    """
    解析 HTML 文件，提取文本内容

    Args:
        file_path: HTML 文件路径

    Returns:
        提取的文本内容
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            html = f.read()
        soup = BeautifulSoup(html, "html.parser")
        return soup.get_text(separator="\n", strip=True)
    except Exception as e:
        return f"HTML 解析错误: {e}"
