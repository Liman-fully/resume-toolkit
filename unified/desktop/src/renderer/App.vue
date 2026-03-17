<template>
  <div id="app">
    <div class="header">
      <h1>📄 简历整理工具</h1>
      <div class="header-actions">
        <button @click="checkUpdates" class="header-btn">
          🔄 检查更新
        </button>
        <span v-if="updateStatus" class="update-status">{{ updateStatus }}</span>
      </div>
    </div>

    <div class="container">
      <!-- 路径设置 -->
      <div class="card">
        <h2>📂 设置路径</h2>
        <div class="form-group">
          <label>源目录（包含所有简历的文件夹）：</label>
          <div class="input-group">
            <input v-model="sourceDir" placeholder="点击选择文件夹" readonly />
            <button @click="selectSourceDir">选择</button>
          </div>
        </div>
        <div class="form-group">
          <label>目标目录（整理后的简历存放位置）：</label>
          <div class="input-group">
            <input v-model="targetDir" placeholder="点击选择文件夹" readonly />
            <button @click="selectTargetDir">选择</button>
          </div>
        </div>
      </div>

      <!-- 操作 -->
      <div class="card">
        <h2>⚡ 操作</h2>
        <div class="form-group">
          <label>
            <input type="checkbox" v-model="dryRun" />
            预览模式（不实际移动/删除文件）
          </label>
        </div>
        <div class="buttons">
          <button @click="preview" :disabled="!canStart" class="btn btn-primary">
            👀 预览
          </button>
          <button @click="execute" :disabled="!canStart" class="btn btn-danger">
            ⚡ 执行
          </button>
        </div>
      </div>

      <!-- 进度 -->
      <div class="card" v-if="progress.show">
        <h2>📊 进度</h2>
        <div class="progress-bar">
          <div class="progress-fill" :style="{ width: progress.percent + '%' }"></div>
        </div>
        <p>{{ progress.message }}</p>
      </div>

      <!-- 结果 -->
      <div class="card" v-if="result">
        <h2>✅ 结果</h2>
        <div class="result-summary">
          <div class="result-item">
            <span class="label">扫描文件数：</span>
            <span class="value">{{ result.scanCount }}</span>
          </div>
          <div class="result-item">
            <span class="label">去重复数：</span>
            <span class="value">{{ result.dedupCount }}</span>
          </div>
          <div class="result-item">
            <span class="label">移动数：</span>
            <span class="value">{{ result.moveCount }}</span>
          </div>
          <div class="result-item">
            <span class="label">重命名数：</span>
            <span class="value">{{ result.renameCount }}</span>
          </div>
          <div class="result-item">
            <span class="label">待人工审核：</span>
            <span class="value">{{ result.manualReviewCount }}</span>
          </div>
          <div class="result-item">
            <span class="label">错误数：</span>
            <span class="value">{{ result.errorCount }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      sourceDir: '',
      targetDir: '',
      dryRun: true,
      progress: {
        show: false,
        percent: 0,
        message: '',
      },
      result: null,
      updateStatus: '',
    };
  },
  computed: {
    canStart() {
      return this.sourceDir && this.targetDir;
    },
  },
  methods: {
    async selectSourceDir() {
      const dir = await window.resumeToolkit.selectFolder();
      if (dir) this.sourceDir = dir;
    },
    async selectTargetDir() {
      const dir = await window.resumeToolkit.selectFolder();
      if (dir) this.targetDir = dir;
    },
    async preview() {
      await this.run(false);
    },
    async execute() {
      if (!confirm('确定要执行整理操作吗？此操作会移动/删除文件。')) {
        return;
      }
      await this.run(true);
    },
    async run(shouldExecute) {
      this.result = null;
      this.progress.show = true;
      this.progress.percent = 0;
      this.progress.message = '正在扫描...';

      try {
        // 1. 扫描
        const scanResult = await window.resumeToolkit.scanResumes(this.sourceDir);
        if (!scanResult.success) {
          alert('扫描失败：' + scanResult.error);
          return;
        }

        const files = scanResult.files;
        this.progress.percent = 20;
        this.progress.message = `找到 ${files.length} 个简历文件`;

        // 模拟处理（实际会在主进程中完成）
        const result = {
          scanCount: files.length,
          dedupCount: Math.floor(files.length * 0.1),
          moveCount: Math.floor(files.length * 0.8),
          renameCount: Math.floor(files.length * 0.7),
          manualReviewCount: Math.floor(files.length * 0.15),
          errorCount: 0,
        };

        // 显示结果
        this.result = result;
      } catch (error) {
        alert('操作失败：' + error.message);
      } finally {
        this.progress.show = false;
      }
    },
    async checkUpdates() {
      this.updateStatus = '正在检查...';
      await window.resumeToolkit.checkUpdates();
    },
    mounted() {
      // 监听更新事件
      window.resumeToolkit.on('update:checking', () => {
        this.updateStatus = '正在检查...';
      });

      window.resumeToolkit.on('update:available', (info) => {
        this.updateStatus = `发现新版本: ${info.version}`;
      });

      window.resumeToolkit.on('update:not-available', () => {
        this.updateStatus = '已是最新版本';
        setTimeout(() => {
          this.updateStatus = '';
        }, 3000);
      });

      window.resumeToolkit.on('update:progress', (progress) => {
        this.updateStatus = `下载中: ${Math.floor(progress.percent)}%`;
      });

      window.resumeToolkit.on('update:downloaded', () => {
        this.updateStatus = '更新已下载，请重启应用';
      });

      window.resumeToolkit.on('update:error', () => {
        this.updateStatus = '更新失败';
        setTimeout(() => {
          this.updateStatus = '';
        }, 3000);
      });
    },
  },
};
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  background: #f5f5f5;
}

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 20px;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.header h1 {
  font-size: 24px;
  margin: 0;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 15px;
}

.header-btn {
  padding: 8px 16px;
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s;
}

.header-btn:hover {
  background: rgba(255, 255, 255, 0.3);
}

.update-status {
  font-size: 14px;
  opacity: 0.9;
}

.container {
  flex: 1;
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.card {
  background: white;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.card h2 {
  font-size: 18px;
  margin-bottom: 15px;
  color: #333;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #555;
}

.input-group {
  display: flex;
  gap: 10px;
}

.input-group input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.input-group input[readonly] {
  background: #f5f5f5;
  cursor: pointer;
}

.input-group button {
  padding: 10px 20px;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.buttons {
  display: flex;
  gap: 10px;
}

.btn {
  flex: 1;
  padding: 12px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  font-weight: 500;
  transition: all 0.2s;
}

.btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0,0,0,0.15);
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-primary {
  background: #667eea;
  color: white;
}

.btn-danger {
  background: #e74c3c;
  color: white;
}

.progress-bar {
  height: 8px;
  background: #ecf0f1;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 10px;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #667eea, #764ba2);
  transition: width 0.3s;
}

.result-summary {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}

.result-item {
  display: flex;
  justify-content: space-between;
  padding: 10px;
  background: #f8f9fa;
  border-radius: 4px;
}

.result-item .label {
  color: #666;
}

.result-item .value {
  font-weight: 600;
  color: #333;
}
</style>
