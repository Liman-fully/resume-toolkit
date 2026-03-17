/**
 * 简历解析器
 * 从不同格式的文件中提取结构化信息
 *
 * 核心逻辑，会被混淆打包
 */

const fs = require('fs').promises;
const path = require('path');
const pdf = require('pdf-parse');
const { JSDOM } = require('jsdom');

class ResumeParser {
  constructor() {
    // 正则表达式模式
    this.patterns = {
      name: [
        /姓名[：:]\s*([^\s\n]{2,4})/,
        /个人简介[：:]\s*([^\s\n]{2,4})/,
        /求职意向[：:]\s*([^\s\n]{2,4})/,
      ],
      jobTitle: [
        /求职意向[：:].*职位[：:]\s*([^\s\n]+)/,
        /应聘职位[：:]\s*([^\s\n]+)/,
        /期望职位[：:]\s*([^\s\n]+)/,
      ],
      education: [
        /(博士|硕士|研究生|本科|大专|专科|高中|初中)/,
        /学历[：:]\s*([^\s\n]+)/,
      ],
      age: [
        /(\d{2})\s*[岁岁]/,
        /年龄[：:]\s*(\d{2})/,
        /(\d{1,2})岁/,
      ],
      city: [
        /(北京|上海|广州|深圳|杭州|南京|苏州|成都|重庆|武汉|西安|天津|青岛|大连)/,
        /城市[：:]\s*([^\s\n]+)/,
        /工作地点[：:]\s*([^\s\n]+)/,
      ],
    };
  }

  /**
   * 解析简历文件
   * @param {string} filePath - 文件路径
   * @returns {Promise<Object>} 解析结果
   */
  async parse(filePath) {
    const ext = path.extname(filePath).toLowerCase();
    let text = '';

    try {
      switch (ext) {
        case '.pdf':
          text = await this.parsePDF(filePath);
          break;
        case '.doc':
        case '.docx':
          text = await this.parseWord(filePath);
          break;
        case '.jpg':
        case '.jpeg':
        case '.png':
        case '.bmp':
          text = await this.parseImage(filePath);
          break;
        case '.html':
        case '.htm':
          text = await this.parseHTML(filePath);
          break;
        default:
          throw new Error(`不支持的文件格式: ${ext}`);
      }

      return this.extractInfo(text);
    } catch (error) {
      throw new Error(`解析失败: ${error.message}`);
    }
  }

  /**
   * 解析 PDF 文件
   */
  async parsePDF(filePath) {
    const dataBuffer = await fs.readFile(filePath);
    const data = await pdf(dataBuffer);
    return data.text;
  }

  /**
   * 解析 Word 文件（简化版，需要 mammoth）
   */
  async parseWord(filePath) {
    // 注意：需要安装 mammoth
    // 这里使用简化版，实际项目中应该用 mammoth 或 docx 库
    try {
      const mammoth = require('mammoth');
      const result = await mammoth.extractRawText({ path: filePath });
      return result.value;
    } catch (error) {
      // 如果 mammoth 未安装，返回提示
      return '提示：Word 解析需要安装 mammoth 库';
    }
  }

  /**
   * 解析图片文件（OCR）
   */
  async parseImage(filePath) {
    // 注意：需要 Tesseract.js
    try {
      const Tesseract = require('tesseract.js');
      const result = await Tesseract.recognize(filePath, 'chi_sim');
      return result.data.text;
    } catch (error) {
      return '提示：图片 OCR 需要 Tesseract.js';
    }
  }

  /**
   * 解析 HTML 文件
   */
  async parseHTML(filePath) {
    const html = await fs.readFile(filePath, 'utf-8');
    const dom = new JSDOM(html);
    return dom.window.document.body.textContent;
  }

  /**
   * 从文本中提取结构化信息
   */
  extractInfo(text) {
    const result = {
      name: null,
      jobTitle: null,
      education: null,
      age: null,
      city: null,
      rawText: text,
    };

    // 提取姓名
    for (const pattern of this.patterns.name) {
      const match = text.match(pattern);
      if (match) {
        result.name = match[1];
        break;
      }
    }

    // 提取职位
    for (const pattern of this.patterns.jobTitle) {
      const match = text.match(pattern);
      if (match) {
        result.jobTitle = match[1];
        break;
      }
    }

    // 提取学历
    for (const pattern of this.patterns.education) {
      const match = text.match(pattern);
      if (match) {
        result.education = match[1];
        break;
      }
    }

    // 提取年龄
    for (const pattern of this.patterns.age) {
      const match = text.match(pattern);
      if (match) {
        result.age = match[1];
        break;
      }
    }

    // 提取城市
    for (const pattern of this.patterns.city) {
      const match = text.match(pattern);
      if (match) {
        result.city = match[1];
        break;
      }
    }

    return result;
  }

  /**
   * 检查解析是否完整
   */
  isComplete(result) {
    return !!(result.name && result.jobTitle && result.education && result.age && result.city);
  }

  /**
   * 获取缺失的字段
   */
  getMissingFields(result) {
    const fields = [];
    if (!result.name) fields.push('姓名');
    if (!result.jobTitle) fields.push('职位');
    if (!result.education) fields.push('学历');
    if (!result.age) fields.push('年龄');
    if (!result.city) fields.push('城市');
    return fields;
  }
}

module.exports = ResumeParser;
