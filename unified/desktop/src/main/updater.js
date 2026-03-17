/**
 * 自动更新模块
 * 使用 electron-updater 实现自动更新
 */

const { autoUpdater } = require('electron-updater');
const { dialog } = require('electron');

class Updater {
  constructor(mainWindow) {
    this.mainWindow = mainWindow;
    this.isCheckingForUpdates = false;
    
    this.setupAutoUpdater();
  }

  setupAutoUpdater() {
    // 配置自动更新
    autoUpdater.setFeedURL({
      provider: 'github',
      owner: 'Liman-fully',
      repo: 'resume-toolkit'
    });

    autoUpdater.autoDownload = false; // 不自动下载，让用户确认
    autoUpdater.autoInstallOnAppQuit = false; // 退出时不自动安装

    // 监听更新事件
    autoUpdater.on('checking-for-update', () => {
      console.log('正在检查更新...');
      this.sendToRenderer('update:checking');
    });

    autoUpdater.on('update-available', (info) => {
      console.log('发现新版本:', info.version);
      this.sendToRenderer('update:available', info);
      
      // 显示更新对话框
      dialog.showMessageBox(this.mainWindow, {
        type: 'info',
        title: '发现新版本',
        message: `发现新版本 ${info.version}`,
        detail: '当前版本: ' + require('../../package.json').version + '\n\n是否立即下载更新？',
        buttons: ['立即下载', '稍后'],
        defaultId: 0
      }).then(result => {
        if (result.response === 0) {
          autoUpdater.downloadUpdate();
        }
      });
    });

    autoUpdater.on('update-not-available', (info) => {
      console.log('当前已是最新版本');
      this.sendToRenderer('update:not-available');
      
      dialog.showMessageBox(this.mainWindow, {
        type: 'info',
        title: '已是最新版本',
        message: '当前已是最新版本',
        detail: `当前版本: ${info.version}`,
        buttons: ['确定']
      });
    });

    autoUpdater.on('error', (err) => {
      console.error('更新错误:', err);
      this.sendToRenderer('update:error', err);
      
      dialog.showErrorBox('更新错误', `检查更新时发生错误: ${err.message}`);
    });

    autoUpdater.on('download-progress', (progressObj) => {
      console.log('下载进度:', progressObj);
      this.sendToRenderer('update:progress', progressObj);
    });

    autoUpdater.on('update-downloaded', (info) => {
      console.log('更新下载完成:', info);
      this.sendToRenderer('update:downloaded', info);
      
      // 显示安装对话框
      dialog.showMessageBox(this.mainWindow, {
        type: 'info',
        title: '更新已下载',
        message: '更新已下载完成',
        detail: '是否立即安装更新？安装后应用将自动重启。',
        buttons: ['立即安装', '稍后'],
        defaultId: 0
      }).then(result => {
        if (result.response === 0) {
          autoUpdater.quitAndInstall();
        }
      });
    });
  }

  checkForUpdates() {
    if (this.isCheckingForUpdates) {
      return;
    }
    
    this.isCheckingForUpdates = true;
    autoUpdater.checkForUpdates()
      .finally(() => {
        this.isCheckingForUpdates = false;
      });
  }

  downloadUpdate() {
    autoUpdater.downloadUpdate();
  }

  quitAndInstall() {
    autoUpdater.quitAndInstall();
  }

  sendToRenderer(channel, ...args) {
    if (this.mainWindow && !this.mainWindow.isDestroyed()) {
      this.mainWindow.webContents.send(channel, ...args);
    }
  }
}

module.exports = Updater;
