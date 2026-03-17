# 简历整理工具 - 详细使用指南

## 目录

1. [安装指南](#安装指南)
2. [快速开始](#快速开始)
3. [功能详解](#功能详解)
4. [配置文件](#配置文件)
5. [常见问题](#常见问题)
6. [故障排除](#故障排除)
7. [高级用法](#高级用法)

---

## 安装指南

### Windows

1. 前往 [GitHub Releases](https://github.com/Liman-fully/resume-toolkit/releases)
2. 下载 `简历整理工具-1.0.0-setup.exe`
3. 双击运行安装程序
4. 按照提示完成安装
5. 桌面会出现快捷方式

### macOS

1. 前往 [GitHub Releases](https://github.com/Liman-fully/resume-toolkit/releases)
2. 下载 `简历整理工具-1.0.0.dmg`
3. 双击打开 DMG 镜像
4. 将应用拖拽到 Applications 文件夹
5. 在 Launchpad 中打开应用

**注意**：如果提示"无法打开，因为无法验证开发者"：
- 右键点击应用 → 选择"打开" → 确认打开

### Linux

1. 前往 [GitHub Releases](https://github.com/Liman-fully/resume-toolkit/releases)
2. 下载 `简历整理工具-1.0.0.AppImage`
3. 添加执行权限：`chmod +x 简历整理工具-1.0.0.AppImage`
4. 双击运行，或命令行执行：`./简历整理工具-1.0.0.AppImage`

---

## 快速开始

### 第一次使用

1. **启动应用**：双击桌面图标
2. **选择源目录**：点击"选择"按钮，选择包含简历的文件夹
   - 可以是根目录（如 `~/Downloads`）
   - 支持递归扫描所有子目录
3. **选择目标目录**：选择整理后的简历存放位置
4. **预览模式**：默认开启，点击"预览"查看效果
5. **确认执行**：
   - 如果预览结果满意，取消"预览模式"
   - 点击"执行"开始整理

### 界面说明

```
┌─────────────────────────────────────┐
│  📄 简历整理工具           🔄 检查更新  │
├─────────────────────────────────────┤
│  📂 设置路径                        │
│  ┌───────────────────────────────┐ │
│  │ 源目录：[ /path/to/source ]    │ │
│  │        [    选择    ]           │ │
│  ├───────────────────────────────┤ │
│  │ 目标目录：[ /path/to/target ]  │ │
│  │          [    选择    ]         │ │
│  └───────────────────────────────┘ │
│                                     │
│  ⚡ 操作                           │
│  ☑ 预览模式（不实际移动文件）       │
│  ┌──────┐  ┌──────┐              │
│  │ 👀   │  │ ⚡   │              │
│  │ 预览 │  │ 执行 │              │
│  └──────┘  └──────┘              │
│                                     │
│  📊 进度                           │
│  ████████████░░░░░░ 60%           │
│  正在处理：张三-产品经理-本科...    │
│                                     │
│  ✅ 结果                           │
│  扫描文件数：100                    │
│  去重复数：8                        │
│  移动数：92                         │
│  重命名数：92                       │
│  待人工审核：5                      │
│  错误数：0                          │
└─────────────────────────────────────┘
```

---

## 功能详解

### 1. 深度扫描

**功能说明**：
- 递归扫描源目录及其所有子目录
- 自动识别简历文件（PDF、Word、图片、网页）
- 跳过隐藏目录和系统目录（如 `.git`、`node_modules`）

**支持格式**：
- PDF：`.pdf`
- Word：`.doc`, `.docx`
- 图片：`.jpg`, `.jpeg`, `.png`
- 网页：`.html`, `.htm`

**扫描示例**：
```
源目录：/Users/Downloads
├── 2024/
│   ├── 01/
│   │   ├── 张三.pdf
│   │   └── 李四.docx
│   └── 02/
│       └── 王五.jpg
└── backup/
    └── 赵六.html

扫描结果：4 个文件
```

### 2. 智能解析

**提取字段**：
- 姓名：从简历标题或正文中提取
- 职位：从职位描述或工作经历中提取
- 学历：从教育背景中提取（本科/硕士/博士）
- 年龄：从个人信息中提取
- 城市：从联系方式或期望地点中提取

**解析准确性**：
- PDF（可复制文字）：90%+
- PDF（扫描件）：70%+（依赖 OCR）
- Word：90%+
- 图片：70%+（依赖 OCR）
- 网页：85%+

**示例**：
```
原文件名：简历_20240317.pdf
解析结果：
  姓名：张三
  职位：产品经理
  学历：本科
  年龄：28
  城市：北京

新文件名：产品经理-张三-本科-28-北京.pdf
```

### 3. 自动去重

**去重逻辑**：
1. 计算每个文件的 MD5 哈希
2. 找出哈希相同的文件（内容完全相同）
3. 保留文件名更规范的那一份
4. 其余标记为重复，放入"待人工审核"文件夹

**示例**：
```
找到重复文件：
  /Downloads/张三.pdf (保留)
  /Downloads/backup/张三.pdf (删除)
  /Downloads/old/张三-copy.pdf (删除)
```

### 4. 智能归类

**分类体系**：

| 分类 | 包含职位 |
|------|---------|
| 技术 | 前端、后端、全栈、架构师、测试工程师 |
| 产品 | 产品经理、产品总监、产品助理 |
| 运营 | 运营专员、市场经理、销售代表 |
| 设计 | UI设计师、UX设计师、平面设计师 |
| 市场 | 市场专员、品牌经理、公关 |
| 其他 | 所有未匹配的职位 |

**自定义分类**：

在用户配置文件中添加：
```json
{
  "categories": {
    "AI": ["算法工程师", "机器学习", "深度学习"],
    "数据": ["数据分析师", "数据科学家", "大数据"]
  }
}
```

### 5. 统一重命名

**默认格式**：
```
职位-姓名-学历-年龄-城市.pdf
```

**示例**：
```
原始文件名：
  - 简历_张三_20240317.pdf
  - 李四_产品经理_最新版.docx
  - resume-wangwu.jpg

重命名后：
  - 产品经理-张三-本科-28-北京.pdf
  - 运营专员-李四-硕士-26-上海.pdf
  - 前端工程师-王五-本科-25-深圳.pdf
```

**缺失字段处理**：
- 姓名缺失：跳过重命名，放入"待人工审核"
- 其他字段缺失：用"未知"占位，如 `产品经理-张三-未知-?-北京.pdf`

---

## 配置文件

### 配置文件位置

| 平台 | 配置文件路径 |
|------|-------------|
| Windows | `%APPDATA%/resume-toolkit/config.json` |
| macOS | `~/Library/Application Support/resume-toolkit/config.json` |
| Linux | `~/.config/resume-toolkit/config.json` |

### 配置文件示例

```json
{
  "sourceDir": "/Users/Downloads",
  "targetDir": "/Users/Documents/已整理简历",
  "dryRun": false,
  "renameFormat": "职位-姓名-学历-年龄-城市",
  "categories": {
    "技术": ["前端", "后端", "全栈", "架构师", "测试工程师"],
    "产品": ["产品经理", "产品总监", "产品助理"],
    "运营": ["运营", "市场", "销售"],
    "设计": ["UI设计师", "UX设计师", "平面设计师"],
    "市场": ["市场专员", "品牌经理", "公关"],
    "其他": []
  },
  "extensions": [".pdf", ".doc", ".docx", ".jpg", ".jpeg", ".png", ".html"],
  "excludeDirs": [".git", "node_modules", "__pycache__", "venv"],
  "dedupStrategy": "keep_best_filename",
  "manualReview": true
}
```

### 配置项说明

| 配置项 | 类型 | 说明 | 默认值 |
|--------|------|------|--------|
| `sourceDir` | string | 源目录路径 | "" |
| `targetDir` | string | 目标目录路径 | "" |
| `dryRun` | boolean | 预览模式 | true |
| `renameFormat` | string | 重命名格式 | "职位-姓名-学历-年龄-城市" |
| `categories` | object | 分类规则 | 见默认分类 |
| `extensions` | array | 支持的文件扩展名 | 见默认值 |
| `excludeDirs` | array | 排除的目录名 | 见默认值 |
| `dedupStrategy` | string | 去重策略 | "keep_best_filename" |
| `manualReview` | boolean | 是否创建待审核文件夹 | true |

---

## 常见问题

### Q1：扫描不到我的简历文件？

**可能原因**：
1. 文件格式不支持（目前只支持 PDF/Word/图片/网页）
2. 文件在排除目录中（如 `.git`、`node_modules`）
3. 文件权限问题

**解决方案**：
1. 检查文件扩展名是否在支持的列表中
2. 检查配置文件中的 `excludeDirs` 设置
3. 确保文件可读（检查文件权限）

### Q2：解析不准确怎么办？

**可能原因**：
1. 简历格式不规范
2. 扫描件质量差
3. OCR 识别错误

**解决方案**：
1. 手动重命名文件（支持标准格式：`姓名-职位-学历-年龄-城市`）
2. 将扫描件转为可复制文字的 PDF
3. 在"待人工审核"文件夹中手动修正

### Q3：重命名后文件名太长？

**解决方案**：
修改配置文件中的 `renameFormat`：
```json
{
  "renameFormat": "职位-姓名"
}
```

### Q4：不想自动归类，全部放到一个文件夹？

**解决方案**：
在配置文件中只保留一个分类：
```json
{
  "categories": {
    "全部": []
  }
}
```

### Q5：误操作了，能撤销吗？

**解决方案**：
1. 默认预览模式，不会实际移动文件
2. 如果已执行，检查原目录（文件可能还在）
3. 下次建议先备份源目录

### Q6：Windows 提示"无法验证开发者"？

**解决方案**：
1. 右键点击安装包 → 属性
2. 勾选"解除锁定"
3. 再次双击运行

### Q7：macOS 提示"无法打开"？

**解决方案**：
1. 右键点击应用
2. 选择"打开"
3. 点击确认

### Q8：Linux 下无法运行 AppImage？

**解决方案**：
1. 添加执行权限：`chmod +x 简历整理工具-1.0.0.AppImage`
2. 安装依赖：`sudo apt install libfuse2`
3. 或使用命令行运行：`./简历整理工具-1.0.0.AppImage`

---

## 故障排除

### 1. 应用无法启动

**检查步骤**：
1. 确认操作系统版本（Windows 10+、macOS 10.13+、Linux Ubuntu 18.04+）
2. 检查是否有杀毒软件阻止
3. 查看错误日志：
   - Windows：`%APPDATA%/resume-toolkit/logs/`
   - macOS：`~/Library/Logs/resume-toolkit/`
   - Linux：`~/.local/share/resume-toolkit/logs/`

### 2. 扫描速度慢

**可能原因**：
1. 文件数量过多（>10000）
2. 目录层级过深（>10层）
3. OCR 识别耗时

**优化方案**：
1. 减少扫描范围（只扫描必要的目录）
2. 关闭 OCR（在配置文件中设置 `enableOCR: false`）
3. 使用 SSD 硬盘

### 3. 解析失败

**检查步骤**：
1. 确认文件格式正确
2. 尝试用其他软件打开文件，确认文件未损坏
3. 检查文件编码（推荐 UTF-8）

### 4. 内存占用过高

**可能原因**：
1. 同时处理大量文件
2. OCR 识别占用内存

**解决方案**：
1. 分批处理（每次处理 500 个文件）
2. 减少并发数量
3. 关闭其他占用内存的程序

---

## 高级用法

### 1. 命令行调用

Windows:
```cmd
"C:\Program Files\简历整理工具\简历整理工具.exe" --source "C:\Downloads" --target "C:\整理后简历"
```

macOS/Linux:
```bash
/Applications/简历整理工具.app/Contents/MacOS/简历整理工具 --source ~/Downloads --target ~/Documents/已整理简历
```

### 2. 定时任务

**Windows 任务计划程序**：
1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（如每天凌晨 2 点）
4. 设置操作：启动程序
5. 程序路径：`简历整理工具.exe`
6. 参数：`--source "C:\Downloads" --target "C:\整理后简历"`

**macOS/Linux Cron**：
```bash
# 编辑 crontab
crontab -e

# 添加定时任务（每天凌晨 2 点执行）
0 2 * * * "/Applications/简历整理工具.app/Contents/MacOS/简历整理工具" --source ~/Downloads --target ~/Documents/已整理简历
```

### 3. 批量处理

**处理多个源目录**：
```bash
# Windows
for /d %i in (C:\Downloads\*) do "简历整理工具.exe" --source "%i" --target "C:\整理后简历"

# macOS/Linux
for dir in ~/Downloads/*/; do
  "/Applications/简历整理工具.app/Contents/MacOS/简历整理工具" --source "$dir" --target ~/Documents/已整理简历
done
```

### 4. 自定义解析规则

修改核心解析器（需要重新编译）：
```javascript
// src/main/core/parser.js
class ResumeParser {
  extractName(text) {
    // 自定义姓名提取规则
    const namePattern = /姓名[：:]\s*([^\n]+)/;
    // ...
  }
}
```

### 5. 导出处理报告

每次执行后会生成 `report.json`：
```json
{
  "timestamp": "2024-03-17T12:00:00Z",
  "summary": {
    "scanCount": 100,
    "dedupCount": 8,
    "moveCount": 92,
    "renameCount": 92,
    "manualReviewCount": 5,
    "errorCount": 0
  },
  "files": [
    {
      "source": "/Downloads/张三.pdf",
      "target": "/Documents/已整理简历/技术/产品经理-张三-本科-28-北京.pdf",
      "status": "success"
    }
  ]
}
```

---

## 技术支持

如果以上方案都无法解决问题：

1. **查看日志**：
   - Windows：`%APPDATA%/resume-toolkit/logs/`
   - macOS：`~/Library/Logs/resume-toolkit/`
   - Linux：`~/.local/share/resume-toolkit/logs/`

2. **提交 Issue**：
   - 访问：https://github.com/Liman-fully/resume-toolkit/issues
   - 描述问题步骤
   - 附上错误日志

3. **联系作者**：
   - 邮箱：liman@example.com

---

**祝你使用愉快！** 🎉
