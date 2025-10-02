import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        secure: false,
        // rewrite는 그대로 두면 기본적으로 경로 유지됩니다.
        // 필요시: rewrite: (path) => path
      },
    },
  },
})