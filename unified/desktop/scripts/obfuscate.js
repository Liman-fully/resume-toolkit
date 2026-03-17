#!/usr/bin/env node

/**
 * 代码混淆脚本
 * 混淆核心逻辑，防止逆向
 */

const JavaScriptObfuscator = require('javascript-obfuscator');
const fs = require('fs');
const path = require('path');

// 要混淆的文件
const filesToObfuscate = [
  'src/main/core/parser.js',
];

// 混淆配置
const obfuscationOptions = {
  compact: true,
  controlFlowFlattening: true,
  controlFlowFlatteningThreshold: 0.75,
  deadCodeInjection: true,
  deadCodeInjectionThreshold: 0.4,
  debugProtection: false,  // 关闭，否则会影响性能
  debugProtectionInterval: false,
  disableConsoleOutput: false,
  identifierNamesGenerator: 'hexadecimal',
  log: false,
  numbersToExpressions: true,
  renameGlobals: false,
  selfDefending: false,
  simplify: true,
  splitStrings: true,
  splitStringsChunkLength: 10,
  stringArray: true,
  stringArrayCallsTransform: true,
  stringArrayCallsTransformThreshold: 0.75,
  stringArrayEncoding: ['rc4'],
  stringArrayIndexShift: true,
  stringArrayRotate: true,
  stringArrayShuffle: true,
  stringArrayWrappersCount: 2,
  stringArrayWrappersChainedCalls: true,
  stringArrayWrappersParametersMaxCount: 4,
  stringArrayWrappersType: 'function',
  stringArrayThreshold: 0.75,
  transformObjectKeys: true,
  unicodeEscapeSequence: false,
};

// 混淆文件
for (const filePath of filesToObfuscate) {
  if (!fs.existsSync(filePath)) {
    console.log(`跳过不存在的文件: ${filePath}`);
    continue;
  }

  console.log(`正在混淆: ${filePath}`);
  const code = fs.readFileSync(filePath, 'utf-8');
  const obfuscatedCode = JavaScriptObfuscator.obfuscate(code, obfuscationOptions).getObfuscatedCode();

  // 保存混淆后的代码
  const outputPath = filePath.replace('.js', '-obfuscated.js');
  fs.writeFileSync(outputPath, obfuscatedCode, 'utf-8');
  console.log(`已保存混淆后的代码: ${outputPath}`);
}

console.log('\n混淆完成！');
