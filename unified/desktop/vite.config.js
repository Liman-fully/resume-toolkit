import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import electron from 'vite-plugin-electron';

export default defineConfig({
  plugins: [
    vue(),
    electron([
      {
        // 主进程入口
        entry: 'src/main/index.js',
        vite: {
          build: {
            outDir: 'dist/main',
          },
        },
      },
      {
        // 预加载脚本入口
        entry: 'src/preload/index.js',
        onstart(args) {
          args.reload();
        },
        vite: {
          build: {
            outDir: 'dist/preload',
          },
        },
      },
    ]),
  ],
  build: {
    outDir: 'dist/renderer',
  },
});
