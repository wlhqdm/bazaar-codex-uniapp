import { defineConfig } from 'vite'
import uni from '@dcloudio/vite-plugin-uni'

// 相对路径，方便 GitHub Pages 子目录部署，也兼容本地预览
export default defineConfig({
  base: './',
  plugins: [uni()],
})
