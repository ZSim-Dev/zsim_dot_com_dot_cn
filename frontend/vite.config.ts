import { fileURLToPath, URL } from 'node:url'

import vue from '@vitejs/plugin-vue'
import { defineConfig } from 'vite'
import { viteStaticCopy } from 'vite-plugin-static-copy'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  // 根据环境模式加载不同的后端地址
  const apiTarget = mode === 'production'
    ? process.env.VITE_API_URL || 'http://localhost:8000'
    : process.env.VITE_DEV_API_URL || 'http://localhost:8000'

  return {
    plugins: [
      vue(),
      vueDevTools(),
      // 复制静态资源插件
      viteStaticCopy({
        targets: [
          {
            src: 'docs/*',
            dest: 'docs'
          }
        ]
      })
    ],
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url))
      },
    },
    build: {
      // 构建配置
      outDir: 'dist',
      assetsDir: 'assets',
      // 复制静态资源
      rollupOptions: {
        input: {
          main: fileURLToPath(new URL('./index.html', import.meta.url))
        }
      },
      // 确保assets和docs目录被包含
      copyPublicDir: true
    },
    // 静态资源处理
    publicDir: 'public',
    // 确保assets和docs目录在开发和构建时都可访问
    assetsInclude: ['**/*.md', '**/*.pdf', '**/*.doc', '**/*.docx'],
    server: {
      proxy: {
        '/api': {
          target: apiTarget,
          changeOrigin: true,
        }
      }
    }
  }
})
