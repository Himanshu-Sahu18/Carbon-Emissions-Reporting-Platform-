import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  build: {
    // Output directory
    outDir: "dist",
    // Generate sourcemaps for production debugging
    sourcemap: false,
    // Chunk size warning limit
    chunkSizeWarningLimit: 1000,
    // Rollup options for code splitting
    rollupOptions: {
      output: {
        // Manual chunk splitting strategy
        manualChunks: {
          // Vendor chunks
          "react-vendor": ["react", "react-dom"],
          "chart-vendor": ["recharts"],
          "form-vendor": ["react-hook-form"],
        },
        // Asset file naming
        assetFileNames: (assetInfo) => {
          const info = assetInfo.name?.split(".");
          const ext = info?.[info.length - 1];
          if (/png|jpe?g|svg|gif|tiff|bmp|ico/i.test(ext || "")) {
            return `assets/images/[name]-[hash][extname]`;
          } else if (/woff|woff2|eot|ttf|otf/i.test(ext || "")) {
            return `assets/fonts/[name]-[hash][extname]`;
          }
          return `assets/[name]-[hash][extname]`;
        },
        // Chunk file naming
        chunkFileNames: "assets/js/[name]-[hash].js",
        // Entry file naming
        entryFileNames: "assets/js/[name]-[hash].js",
      },
    },
    // Minification
    minify: "esbuild",
    // Target browsers
    target: "es2015",
  },
  // Server configuration
  server: {
    port: 5173,
    host: true,
    proxy: {
      "/api": {
        target: process.env.VITE_API_BASE_URL || "http://localhost:8000",
        changeOrigin: true,
      },
    },
  },
  // Preview server configuration
  preview: {
    port: 4173,
    host: true,
  },
});
