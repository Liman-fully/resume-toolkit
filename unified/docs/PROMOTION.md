# 简历整理工具 - 发布推广指南

## 📋 发布清单

### GitHub Releases

- [ ] 创建 GitHub Release
- [ ] 上传三个平台的安装包
- [ ] 发布到 GitHub Marketplace

### 推广平台

- [ ] 掘金
- [ ] 知乎
- [ ] V2EX
- [ ] 少数派
- [ ] SegmentFault
- [ ] CSDN
- [ ] 简书

### 社交媒体

- [ ] 微博
- [ ] Twitter
- [ ] Reddit (r/software)
- [ ] Product Hunt

---

## 🎯 GitHub Release

### 1. 打包应用

```bash
cd /Users/liman/WorkBuddy/20260316201131/resume-toolkit/unified/desktop

# 安装依赖
npm install

# 打包 Windows
npm run build:win

# 打包 macOS
npm run build:mac

# 打包 Linux
npm run build:linux
```

### 2. 创建 Release

使用 GitHub CLI：

```bash
gh release create v1.0.0 \
  --title "简历整理工具 v1.0.0 - 首个正式版本" \
  --notes "RELEASE_NOTES.md" \
  release/*.exe \
  release/*.dmg \
  release/*.AppImage
```

### 3. Release Notes

```markdown
## 简历整理工具 v1.0.0

🎉 首个正式版本发布！

### ✨ 核心功能

- 📂 **深度扫描**：递归扫描指定目录，支持 PDF/Word/图片/网页
- 🧠 **智能解析**：从简历提取姓名、职位、学历、年龄、城市
- 🔄 **自动去重**：MD5 哈希识别重复文件
- 📁 **智能归类**：半固定分类体系 + 用户自定义扩展
- ✏️ **统一重命名**：自动重命名为 `职位-姓名-学历-年龄-城市.pdf`
- 🎨 **友好界面**：现代化 UI，实时显示处理进度

### 🔧 技术特性

- ✅ 代码混淆保护
- ✅ 本地运行，不上传云端
- ✅ 预览模式，安全可靠
- ✅ 跨平台支持（Windows/macOS/Linux）
- ✅ 自动更新功能

### 📦 下载

- **Windows**: `简历整理工具-1.0.0-setup.exe`
- **macOS**: `简历整理工具-1.0.0.dmg`
- **Linux**: `简历整理工具-1.0.0.AppImage`

### 📖 使用指南

详细文档：https://github.com/Liman-fully/resume-toolkit/tree/main/docs

### 🙏 感谢

感谢所有参与测试和反馈的用户！

---

## 完整更新日志

详见 [CHANGELOG.md](https://github.com/Liman-fully/resume-toolkit/blob/main/CHANGELOG.md)
```

---

## 📝 掘金发布

### 标题

```
🚀 开源一款简历整理工具，一键整理你的简历库
```

### 正文

```markdown
# 🚀 开源一款简历整理工具，一键整理你的简历库

大家好，我是 Liman。今天开源一款我开发的**简历整理工具**，帮助大家快速整理散落在电脑各处的简历文件。

## 🎯 为什么开发这个工具？

作为 HR 或猎头，我们经常遇到这样的问题：

1. 简历散落在各个文件夹，找不到
2. 文件名不统一，难以识别
3. 重复简历太多，浪费存储空间
4. 手动整理效率太低

于是，我开发了这款**简历整理工具**，一键解决以上问题。

## ✨ 核心功能

### 1. 深度扫描

递归扫描指定目录，简历藏得再深也能找到。

### 2. 智能解析

从简历内容提取结构化信息：
- 姓名
- 职位
- 学历
- 年龄
- 城市

### 3. 自动去重

MD5 哈希识别重复文件，保留最优版本。

### 4. 智能归类

半固定分类体系 + 用户自定义扩展：
- 技术
- 产品
- 运营
- 设计
- 市场
- 其他

### 5. 统一重命名

自动重命名为 `职位-姓名-学历-年龄-城市.pdf`。

## 🎨 界面预览

![界面预览](https://github.com/Liman-fully/resume-toolkit/raw/main/screenshots/screenshot.png)

## 🚀 快速开始

### 方式一：下载安装包（推荐）

1. 访问 [GitHub Releases](https://github.com/Liman-fully/resume-toolkit/releases)
2. 下载对应平台的安装包
3. 双击运行，无需配置环境

### 方式二：命令行使用

```bash
git clone https://github.com/Liman-fully/resume-toolkit.git
cd resume-toolkit/unified/desktop
npm install
npm run dev
```

## 🔒 安全性

- ✅ 代码混淆保护
- ✅ 本地运行，不上传云端
- ✅ 预览模式，安全可靠

## 📦 技术栈

- 框架：Electron + Vue 3
- 解析：PyMuPDF、python-docx、Tesseract.js
- 打包：electron-builder

## 🎁 开源协议

MIT License，欢迎贡献代码！

## 📞 联系方式

- GitHub：https://github.com/Liman-fully/resume-toolkit
- 邮箱：liman@example.com

## 🙏 感谢

如果这个项目对你有帮助，请给个 ⭐️ 支持一下！

---

**Made with ❤️ by Liman**
```

---

## 📝 知乎发布

### 标题

```
作为 HR，我开发了一款简历整理工具，现在开源了
```

### 正文

```markdown
# 作为 HR，我开发了一款简历整理工具，现在开源了

## 背景

作为 HR，每天要处理大量简历。最头疼的是：

- 简历散落在各个文件夹，找不到
- 文件名不统一，难以识别
- 重复简历太多，浪费存储空间
- 手动整理效率太低

## 解决方案

我开发了一款**简历整理工具**，一键解决以上问题。

## 核心功能

### 1. 深度扫描

递归扫描指定目录，简历藏得再深也能找到。

### 2. 智能解析

从简历内容提取结构化信息：姓名、职位、学历、年龄、城市。

### 3. 自动去重

MD5 哈希识别重复文件，保留最优版本。

### 4. 智能归类

半固定分类体系：技术、产品、运营、设计、市场、其他。

### 5. 统一重命名

自动重命名为 `职位-姓名-学历-年龄-城市.pdf`。

## 使用效果

整理前：
```
Downloads/
├── 简历_张三.pdf
├── 李四-产品经理.docx
├── resume-wangwu.jpg
└── backup/
    ├── 张三-copy.pdf
    └── 2024/
        └── 李四.pdf
```

整理后：
```
已整理简历/
├── 产品/
│   ├── 产品经理-张三-本科-28-北京.pdf
│   └── 运营专员-李四-硕士-26-上海.pdf
├── 技术/
│   └── 前端工程师-王五-本科-25-深圳.pdf
└── 待人工审核/
    └── 重复文件备份/
```

## 技术亮点

1. **代码混淆**：核心算法打包混淆，防止逆向
2. **本地运行**：所有操作在本地完成，不上传云端
3. **预览模式**：默认预览，确认后再执行
4. **跨平台**：Windows/macOS/Linux 三个版本

## 开源原因

1. 帮助更多 HR 提高效率
2. 收集用户反馈，持续改进
3. 推广开源精神

## 下载使用

GitHub：https://github.com/Liman-fully/resume-toolkit

直接下载安装包，双击运行，无需配置环境。

## 反馈建议

欢迎提 Issue、PR，或发邮件：liman@example.com

---

**如果对你有帮助，请给个 ⭐️！**
```

---

## 📝 V2EX 发布

### 标题

```
[开源] 开发了一款简历整理工具，一键整理你的简历库
```

### 正文

```markdown
[开源] 开发了一款简历整理工具，一键整理你的简历库

大家好，分享一款我开发的简历整理工具。

## 功能介绍

- 深度扫描：递归扫描指定目录
- 智能解析：提取姓名、职位、学历、年龄、城市
- 自动去重：MD5 哈希识别重复文件
- 智能归类：半固定分类体系
- 统一重命名：职位-姓名-学历-年龄-城市.pdf

## 技术栈

- Electron + Vue 3
- PyMuPDF、python-docx、Tesseract.js
- electron-builder

## 仓库地址

https://github.com/Liman-fully/resume-toolkit

## 下载

GitHub Releases：https://github.com/Liman-fully/resume-toolkit/releases

支持 Windows/macOS/Linux。

## 开源协议

MIT License

欢迎提 Issue、PR！
```

---

## 📝 少数派发布

### 标题

```
App 推荐：简历整理工具 - 一键整理你的简历库
```

### 正文

```markdown
# App 推荐：简历整理工具 - 一键整理你的简历库

作为 HR 或求职者，你是不是也有这样的困扰：

- 简历散落在各个文件夹，找不到
- 文件名不统一，难以识别
- 重复简历太多，浪费存储空间
- 手动整理效率太低

今天，我推荐一款**简历整理工具**，一键解决以上问题。

## 核心功能

### 1. 深度扫描

递归扫描指定目录，简历藏得再深也能找到。

### 2. 智能解析

从简历内容提取结构化信息：姓名、职位、学历、年龄、城市。

### 3. 自动去重

MD5 哈希识别重复文件，保留最优版本。

### 4. 智能归类

半固定分类体系：技术、产品、运营、设计、市场、其他。

### 5. 统一重命名

自动重命名为 `职位-姓名-学历-年龄-城市.pdf`。

## 使用效果

整理前：
```
Downloads/
├── 简历_张三.pdf
├── 李四-产品经理.docx
├── resume-wangwu.jpg
└── backup/
    ├── 张三-copy.pdf
    └── 2024/
        └── 李四.pdf
```

整理后：
```
已整理简历/
├── 产品/
│   ├── 产品经理-张三-本科-28-北京.pdf
│   └── 运营专员-李四-硕士-26-上海.pdf
├── 技术/
│   └── 前端工程师-王五-本科-25-深圳.pdf
└── 待人工审核/
    └── 重复文件备份/
```

## 技术亮点

1. **代码混淆**：核心算法打包混淆，防止逆向
2. **本地运行**：所有操作在本地完成，不上传云端
3. **预览模式**：默认预览，确认后再执行
4. **跨平台**：Windows/macOS/Linux 三个版本

## 下载使用

GitHub：https://github.com/Liman-fully/resume-toolkit

GitHub Releases：https://github.com/Liman-fully/resume-toolkit/releases

直接下载安装包，双击运行，无需配置环境。

## 开源协议

MIT License，免费使用。

## 反馈建议

欢迎提 Issue、PR，或发邮件：liman@example.com

---

**如果对你有帮助，请给个 ⭐️！**
```

---

## 📝 Product Hunt

### 标题

```
Resume Toolkit - 简历整理工具
```

### 描述

```
一键整理你的简历库，智能解析、自动归类、统一命名。
```

### 正文

```
📄 Resume Toolkit - 简历整理工具

一键整理你的简历库，智能解析、自动归类、统一命名。

✨ 核心功能：
- 深度扫描：递归扫描指定目录
- 智能解析：提取姓名、职位、学历、年龄、城市
- 自动去重：MD5 哈希识别重复文件
- 智能归类：半固定分类体系
- 统一重命名：职位-姓名-学历-年龄-城市.pdf

🎯 适用人群：
- HR 招聘
- 猎头顾问
- 求职者
- 企业档案管理

🚀 跨平台：Windows/macOS/Linux

🔒 安全性：
- 代码混淆保护
- 本地运行，不上传云端
- 预览模式，安全可靠

📦 下载：https://github.com/Liman-fully/resume-toolkit/releases

📖 文档：https://github.com/Liman-fully/resume-toolkit

🙏 如果对你有帮助，请给个 ⭐️！
```

---

## 📝 Reddit

### 标题

```
[Open Source] Resume Toolkit - A Universal Resume Organizer Tool
```

### 正文

```
Hi everyone,

I've developed an open-source tool called **Resume Toolkit** to help organize resume files efficiently.

## Features

- **Deep Scanning**: Recursively scan directories
- **Smart Parsing**: Extract name, job title, education, age, city
- **Automatic Deduplication**: MD5 hash-based duplicate detection
- **Smart Classification**: Semi-fixed category system
- **Unified Renaming**: Format: `Position-Name-Education-Age-City.pdf`

## Tech Stack

- Electron + Vue 3
- PyMuPDF, python-docx, Tesseract.js
- electron-builder

## GitHub

https://github.com/Liman-fully/resume-toolkit

## Download

https://github.com/Liman-fully/resume-toolkit/releases

Supports Windows/macOS/Linux.

## License

MIT License

Feel free to try it out and give feedback!
```

---

## 📝 CSDN / 简书

### 标题

```
开源项目：简历整理工具，一键整理你的简历库
```

### 正文

```markdown
# 开源项目：简历整理工具，一键整理你的简历库

## 项目介绍

简历整理工具是一款通用的简历管理软件，帮助你快速整理散落在电脑各处的简历文件。

## 核心功能

1. 深度扫描：递归扫描指定目录
2. 智能解析：提取姓名、职位、学历、年龄、城市
3. 自动去重：MD5 哈希识别重复文件
4. 智能归类：半固定分类体系
5. 统一重命名：职位-姓名-学历-年龄-城市.pdf

## 技术栈

- 框架：Electron + Vue 3
- 解析：PyMuPDF、python-docx、Tesseract.js
- 打包：electron-builder

## 下载使用

GitHub：https://github.com/Liman-fully/resume-toolkit

GitHub Releases：https://github.com/Liman-fully/resume-toolkit/releases

支持 Windows/macOS/Linux。

## 开源协议

MIT License

欢迎贡献代码！
```

---

## 📊 推广计划

### 第一周

- 发布到 GitHub Releases
- 推广到掘金、知乎、V2EX

### 第二周

- 推广到少数派、SegmentFault、CSDN
- 发布到 Product Hunt

### 第三周

- 收集用户反馈
- 修复 Bug
- 发布 v1.0.1

### 第四周

- 推广到社交媒体
- 发布教程视频
- 增加 Star 数量

---

## 📈 预期目标

- GitHub Stars: 100+
- 下载量: 1000+
- Issue 数量: 20+
- Fork 数量: 10+

---

**Good luck! 🚀**
