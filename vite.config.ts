import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'
import { resolve } from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": resolve(__dirname, "./"),
      "@api": resolve(__dirname, "./src/api"),
      "@mocks": resolve(__dirname, "./src/mocks"),
      "@routes": resolve(__dirname, "./src/routes"),
      "@components": resolve(__dirname, "./src/components"),
    },
  },
})