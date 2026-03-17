# 简历整理工具 v2.0

一个通用的简历整理工具，支持扫描、解析、去重、归类、重命名和 Web UI 操作。

## 特性

- 📂 **深度扫描**：递归扫描指定目录，找到所有简历文件（支持 PDF、Word、图片、网页）
- 🔍 **智能解析**：从简历中提取姓名、职位、学历、年龄、城市等信息
- 🗑️ **去重**：基于 MD5 哈希识别重复文件，自动删除多余副本
- 📁 **归类**：半固定分类体系 + 用户自定义扩展，智能归类
- ✏️ **重命名**：统一文件名格式：`职位-姓名-学历-年龄-城市.pdf`
- 🌐 **Web UI**：浏览器操作界面，非技术用户友好
- ⚡ **高性能**：分块读取文件，避免内存溢出

## 项目结构

```
resume-toolkit/
├── resume_toolkit/
│   ├── __init__.py
│   ├── config.py              # 配置（基础分类体系 + 用户自定义扩展）
│   ├── scanner.py             # 深度扫描模块
│   ├── parser.py              # 简历解析主模块
│   ├── parser/
│   │   ├── _pdf.py            # PDF 解析器
│   │   ├── _word.py           # Word 解析器
│   │   ├── _image.py          # 图片 OCR 解析器
│   │   └── _html.py           # 网页解析器
│   ├── dedup.py               # 去重模块
│   ├── classifier.py          # 分类模块
│   ├── renamer.py             # 重命名模块
│   └── organizer.py           # 整合模块（完整流程）
├── web/
│   ├── app.py                 # Flask Web UI 后端
│   ├── templates/index.html   # Web UI 前端
│   └── static/style.css       # Web UI 样式
├── main.py                    # CLI 入口
├── requirements.txt           # 依赖
└── README.md                  # 说明文档
```

## 安装

```bash
git clone https://github.com/Liman-fully/resume-toolkit.git
cd resume-toolkit
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## 使用方式

### 1. Web UI（推荐）

启动 Web UI：

```bash
python main.py web
```

浏览器访问 `http://localhost:5000`，在界面中：
1. 填写源目录和目标目录
2. 选择预览模式（默认）或执行模式
3. 点击「预览」查看结果，确认后点击「执行」
4. 可以在「分类管理」中添加自定义分类

### 2. 命令行

#### 整理简历（预览模式）

```bash
python main.py organize --source /path/to/source --target /path/to/target
```

#### 整理简历（执行模式）

```bash
python main.py organize --source /path/to/source --target /path/to/target --execute
```

#### 查看分类规则

```bash
python main.py categories
```

#### 启动 Web UI（自定义端口）

```bash
python main.py web --port 8080
```

## 支持的文件格式

- PDF（包括可复制文字和扫描件）
- Word（.doc, .docx）
- 图片（.jpg, .jpeg, .png, .bmp）需要 OCR
- 网页（.html, .htm）

## 分类体系

工具内置了一套基础分类体系（技术研发、产品经理、设计创意等），用户可以通过 Web UI 或配置文件添加自定义分类和关键词。

自定义分类规则保存在 `~/.resume-toolkit/user_config.json`。

## 文件名格式

整理后的文件名格式为：`职位-姓名-学历-年龄-城市.pdf`

示例：`软件工程师_张三_本科_28_北京.pdf`

如果解析不完整，文件会放入 `待人工审核` 文件夹，保留原文件名。

## 注意事项

1. **OCR 依赖**：图片解析需要安装 Tesseract OCR，并确保 `tesseract` 命令在 PATH 中。
2. **默认预览模式**：命令行操作默认为预览模式，不会实际移动/删除文件，需添加 `--execute` 参数才真正执行。
3. **备份建议**：首次使用前，建议先备份简历文件。

## 迭代指南

### 添加新的文件格式支持

1. 在 `resume_toolkit/parser/` 目录下创建新的解析器（如 `_epub.py`）
2. 在 `parser.py` 的 `parse_resume()` 函数中添加对应的格式判断
3. 在 `config.py` 的 `SUPPORTED_EXTENSIONS` 中添加文件扩展名

### 修改分类规则

方法一：通过 Web UI 添加自定义分类

方法二：编辑配置文件 `~/.resume-toolkit/user_config.json`

```json
{
  "custom_categories": {
    "新分类": ["关键词1", "关键词2"]
  },
  "custom_keywords": {
    "技术研发": ["新关键词1", "新关键词2"]
  }
}
```

### 改进解析准确性

修改 `parser.py` 中的 `extract_info_from_text()` 函数，优化正则表达式。

## 测试

```bash
pytest tests/ -v
```

## License

MIT
