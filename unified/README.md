<div align="center">

# 📄 简历整理工具

**Universal Resume Organizer - Desktop App**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![GitHub Release](https://img.shields.io/github/v/release/Liman-fully/resume-toolkit)](https://github.com/Liman-fully/resume-toolkit/releases)
[![Downloads](https://img.shields.io/github/downloads/Liman-fully/resume-toolkit/total)](https://github.com/Liman-fully/resume-toolkit/releases)

**一键整理你的简历库，智能解析、自动归类、统一命名**

</div>

---

## 🎯 产品介绍

简历整理工具是一款**通用的简历管理软件**，帮助你快速整理散落在电脑各处的简历文件，支持 PDF、Word、图片、网页等多种格式。

### 核心功能

| 功能 | 说明 |
|------|------|
| 📂 **深度扫描** | 递归扫描指定目录，简历藏得再深也能找到 |
| 🧠 **智能解析** | 从简历内容提取姓名、职位、学历、年龄、城市 |
| 🔄 **自动去重** | MD5 哈希识别重复文件，保留最优版本 |
| 📁 **智能归类** | 半固定分类体系 + 用户自定义扩展 |
| ✏️ **统一重命名** | 自动重命名为 `职位-姓名-学历-年龄-城市.pdf` |
| 🎨 **友好界面** | 现代化 UI，实时显示处理进度 |

### 适用场景

- **HR 招聘**：整理候选人的简历，快速分类查找
- **猎头顾问**：管理大量候选人简历，提高工作效率
- **求职者**：整理自己不同版本的简历，方便投递
- **企业档案**：历史员工简历归档，建立人才库

---

## ✨ 产品特性

### 1. 通用化设计

不是针对特定文件夹的死规则，而是真正通用的工具：
- ✅ 任意目录深度扫描
- ✅ 多种文件格式支持
- ✅ 用户可自定义分类规则
- ✅ 灵活的命名策略

### 2. 智能化解析

基于先进的文本分析技术：
- ✅ PDF（包括扫描件 OCR）
- ✅ Word (.docx)
- ✅ 图片（OCR 识别）
- ✅ 网页（HTML）

### 3. 安全性保障

多层保护，确保数据安全：
- ✅ **代码混淆**：核心算法打包混淆，防止逆向
- ✅ **本地运行**：所有操作在本地完成，不上传云端
- ✅ **预览模式**：默认预览，确认后再执行
- ✅ **可撤销**：保留原文件结构，随时恢复

### 4. 跨平台支持

一套代码，三个平台：
- ✅ **Windows**：.exe 安装包
- ✅ **macOS**：.dmg 镜像文件
- ✅ **Linux**：.AppImage 便携包

---

## 🚀 快速开始

### 方式一：下载安装包（推荐）

1. 前往 [GitHub Releases](https://github.com/Liman-fully/resume-toolkit/releases)
2. 下载对应平台的安装包
3. 双击运行，无需配置环境

### 方式二：命令行使用

```bash
# 克隆仓库
git clone https://github.com/Liman-fully/resume-toolkit.git
cd resume-toolkit/unified/desktop

# 安装依赖
npm install

# 开发模式
npm run dev

# 打包所有平台
npm run build

# 打包单个平台
npm run build:win   # Windows
npm run build:mac   # macOS
npm run build:linux # Linux
```

---

## 📖 使用指南

### 基础使用

1. **选择源目录**：包含所有简历的文件夹（可以是根目录，支持递归扫描）
2. **选择目标目录**：整理后的简历存放位置
3. **预览模式**：默认开启，只显示预览结果，不实际移动文件
4. **点击预览**：查看整理效果
5. **确认执行**：取消预览模式，点击执行，开始整理

### 高级功能

#### 自定义分类规则

编辑用户配置文件（自动生成）：
```json
{
  "categories": {
    "技术": ["前端", "后端", "全栈", "架构师"],
    "产品": ["产品经理", "产品总监"],
    "运营": ["运营", "市场", "销售"]
  }
}
```

#### 调整重命名规则

默认格式：`职位-姓名-学历-年龄-城市.pdf`

可在配置文件中自定义：
```json
{
  "renameFormat": "姓名-职位-城市-学历"
}
```

---

## 🏗️ 技术架构

### 三层安全架构

```
┌─────────────────────────────────────┐
│   Renderer (Vue 3)                  │
│   - UI 界面                          │
│   - 只负责显示，无业务逻辑           │
│   - 通过 preload 与主进程通信        │
└──────────────┬──────────────────────┘
               │ IPC (安全沙箱)
┌──────────────▼──────────────────────┐
│   Preload (桥接层)                   │
│   - 暴露安全的 API                   │
│   - contextIsolation: true          │
│   - nodeIntegration: false          │
└──────────────┬──────────────────────┘
               │ IPC
┌──────────────▼──────────────────────┐
│   Main (Node.js)                    │
│   - 核心逻辑（混淆）                 │
│   - 文件系统操作                     │
│   - 简历解析/去重/归类               │
└─────────────────────────────────────┘
```

### 技术栈

| 层级 | 技术 |
|------|------|
| 框架 | Electron 30.0+ |
| 前端 | Vue 3 + Vite |
| 后端 | Node.js |
| 解析 | PyMuPDF、python-docx、Tesseract.js |
| 构建 | electron-builder |
| 混淆 | JavaScript Obfuscator |

---

## 📊 项目进度

| 模块 | 状态 |
|------|------|
| 核心解析器 | ✅ 完成 |
| 深度扫描 | ✅ 完成 |
| 自动去重 | ✅ 完成 |
| 智能归类 | ✅ 完成 |
| 统一重命名 | ✅ 完成 |
| Web UI | ✅ 完成 |
| 自动更新 | ✅ 完成 |
| 代码混淆 | ✅ 完成 |
| 单元测试 | 🔄 进行中 |
| 打包测试 | 🔄 进行中 |

---

## 🔒 安全性说明

### 代码保护

- ✅ **JavaScript Obfuscator**：核心算法混淆，变量名、函数名十六进制化
- ✅ **Asar 打包**：源码加密打包
- ✅ **逻辑分离**：核心逻辑在 Node.js，前端只通过 IPC 调用
- ✅ **沙箱隔离**：Preload 启用上下文隔离，禁用 node 集成
- ✅ **最小权限**：只暴露必要的 API，不暴露核心算法

### 数据隐私

- ✅ **本地运行**：所有文件操作在本地完成，不上传云端
- ✅ **无数据收集**：不收集用户任何个人信息
- ✅ **开源透明**：核心算法可审计（混淆前）

---

## 📝 更新日志

详见 [CHANGELOG.md](CHANGELOG.md)

### v1.0.0 (2024-03-17)

**重大更新：**
- ✨ 首个正式版本发布
- ✨ 支持 PDF/Word/图片/网页 解析
- ✨ 智能归类 + 统一重命名
- ✨ 桌面应用 + Web UI
- ✨ 代码混淆保护

---

## 🤝 贡献指南

欢迎贡献代码、报告问题、提出建议！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📄 开源协议

本项目采用 [MIT License](LICENSE) 开源协议。

---

## 🙏 致谢

感谢以下开源项目：
- [Electron](https://www.electronjs.org/)
- [Vue.js](https://vuejs.org/)
- [Tesseract.js](https://github.com/naptha/tesseract.js)
- [PyMuPDF](https://github.com/pymupdf/PyMuPDF)

---

## 📞 联系方式

- GitHub Issues: [提交问题](https://github.com/Liman-fully/resume-toolkit/issues)
- 邮箱: liman@example.com

---

<div align="center">

**如果这个项目对你有帮助，请给个 ⭐️ 支持一下！**

Made with ❤️ by Liman

</div>
