/**
 * 预加载脚本
 * 桥接前端和主进程，桥接层，安全沙箱
 */

const { contextBridge, ipcRenderer } = require('electron');

// 只暴露必要的 API，不暴露核心逻辑
contextBridge.exposeInMainWorld('resumeToolkit', {
  // 文件操作
  selectFolder: () => ipcRenderer.invoke('select-folder'),
  scanResumes: (sourceDir) => ipcRenderer.invoke('scan-resumes', sourceDir),
  moveFile: (sourcePath, targetPath) => ipcRenderer.invoke('move-file', sourcePath, targetPath),
  deleteFile: (filePath) => ipcRenderer.invoke('delete-file', filePath),

  // 简历解析
  parseResume: (filePath) => ipcRenderer.invoke('parse-resume', filePath),
  fileHash: (filePath) => ipcRenderer.invoke('file-hash', filePath),

  // 配置管理
  saveConfig: (config) => ipcRenderer.invoke('save-config', config),
  loadConfig: () => ipcRenderer.invoke('load-config'),

  // 自动更新
  checkUpdates: () => ipcRenderer.invoke('check-updates'),
  on: (channel, callback) => {
    const validChannels = [
      'update:checking',
      'update:available',
      'update:not-available',
      'update:progress',
      'update:downloaded',
      'update:error',
    ];
    if (validChannels.includes(channel)) {
      ipcRenderer.on(channel, (event, ...args) => callback(...args));
    }
  },
});
