/**
 * Electron 主进程
 * 核心逻辑都在这里，会混淆打包
 */

const { app, BrowserWindow, ipcMain, dialog } = require('electron');
const path = require('path');
const fs = require('fs').promises;
const crypto = require('crypto');
const Updater = require('./updater');

// 加载混淆后的核心模块
// 生产环境会混淆，开发环境直接引入
let ResumeParser;
try {
  ResumeParser = require('./core/parser-obfuscated.js');
} catch {
  ResumeParser = require('./core/parser.js');
}

let mainWindow = null;
let updater = null;

// 创建主窗口
function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    minWidth: 900,
    minHeight: 600,
    webPreferences: {
      preload: path.join(__dirname, '../preload/index.js'),
      nodeIntegration: false,  // 安全：禁用 node 集成
      contextIsolation: true,  // 安全：启用上下文隔离
    }
  });

  // 加载前端页面
  if (process.env.NODE_ENV === 'development') {
    mainWindow.loadURL('http://localhost:5173');
    mainWindow.webContents.openDevTools();
  } else {
    mainWindow.loadFile(path.join(__dirname, '../renderer/index.html'));
  }

  mainWindow.on('closed', () => {
    mainWindow = null;
  });

  // 初始化自动更新（仅在生产环境）
  if (process.env.NODE_ENV !== 'development') {
    updater = new Updater(mainWindow);
  }
}

// 选择文件夹
ipcMain.handle('select-folder', async () => {
  const result = await dialog.showOpenDialog(mainWindow, {
    properties: ['openDirectory']
  });
  return result.canceled ? null : result.filePaths[0];
});

// 扫描简历文件
ipcMain.handle('scan-resumes', async (event, sourceDir) => {
  try {
    const files = await scanDirectory(sourceDir);
    return { success: true, files };
  } catch (error) {
    return { success: false, error: error.message };
  }
});

// 递归扫描目录（核心逻辑）
async function scanDirectory(dir, extensions = ['.pdf', '.doc', '.docx', '.jpg', '.jpeg', '.png', '.html']) {
  const entries = await fs.readdir(dir, { withFileTypes: true });
  const files = [];

  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);

    if (entry.isDirectory()) {
      // 跳过隐藏目录和系统目录
      if (!entry.name.startsWith('.') && entry.name !== 'node_modules' && entry.name !== '__pycache__') {
        const subFiles = await scanDirectory(fullPath, extensions);
        files.push(...subFiles);
      }
    } else if (entry.isFile() && extensions.includes(path.extname(entry.name).toLowerCase())) {
      files.push(fullPath);
    }
  }

  return files;
}

// 解析简历（核心逻辑，会混淆）
ipcMain.handle('parse-resume', async (event, filePath) => {
  try {
    const parser = new ResumeParser();
    const result = await parser.parse(filePath);
    return { success: true, result };
  } catch (error) {
    return { success: false, error: error.message };
  }
});

// 计算文件哈希（去重）
ipcMain.handle('file-hash', async (event, filePath) => {
  try {
    const hash = await calculateFileHash(filePath);
    return { success: true, hash };
  } catch (error) {
    return { success: false, error: error.message };
  }
});

async function calculateFileHash(filePath) {
  const hash = crypto.createHash('md5');
  const stream = await fs.readFile(filePath);
  hash.update(stream);
  return hash.digest('hex');
}

// 移动文件
ipcMain.handle('move-file', async (event, sourcePath, targetPath) => {
  try {
    // 确保目标目录存在
    const targetDir = path.dirname(targetPath);
    await fs.mkdir(targetDir, { recursive: true });

    // 如果目标文件已存在，追加序号
    let finalTargetPath = targetPath;
    let counter = 1;
    while (await fileExists(finalTargetPath)) {
      const ext = path.extname(targetPath);
      const base = path.basename(targetPath, ext);
      finalTargetPath = path.join(targetDir, `${base}_${counter}${ext}`);
      counter++;
    }

    await fs.rename(sourcePath, finalTargetPath);
    return { success: true, newPath: finalTargetPath };
  } catch (error) {
    return { success: false, error: error.message };
  }
});

async function fileExists(filePath) {
  try {
    await fs.access(filePath);
    return true;
  } catch {
    return false;
  }
}

// 删除文件
ipcMain.handle('delete-file', async (event, filePath) => {
  try {
    await fs.unlink(filePath);
    return { success: true };
  } catch (error) {
    return { success: false, error: error.message };
  }
});

// 保存用户配置
ipcMain.handle('save-config', async (event, config) => {
  try {
    const configPath = path.join(app.getPath('userData'), 'config.json');
    await fs.writeFile(configPath, JSON.stringify(config, null, 2));
    return { success: true };
  } catch (error) {
    return { success: false, error: error.message };
  }
});

// 读取用户配置
ipcMain.handle('load-config', async () => {
  try {
    const configPath = path.join(app.getPath('userData'), 'config.json');
    const data = await fs.readFile(configPath, 'utf-8');
    return { success: true, config: JSON.parse(data) };
  } catch (error) {
    return { success: true, config: {} };  // 返回空配置
  }
});

// 检查更新
ipcMain.handle('check-updates', () => {
  if (updater) {
    updater.checkForUpdates();
    return { success: true };
  }
  return { success: false, error: '自动更新不可用' };
});

// App 生命周期
app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});
