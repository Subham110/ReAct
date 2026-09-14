import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8001',
        changeOrigin: true,
      },
      '/health': {
        target: 'http://localhost:8001',
        changeOrigin: true,
      },
    },
  },
  build: {
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (id.includes('node_modules')) {
            if(id.includes('recharts')) {
              return 'vendor_recharts';
            }
            if(id.includes('lucide')) {
              return 'vendor_lucide';
            }
            if(id.includes('chart.js')) {
              return 'vendor_chartjs';
            }
            if(id.includes('react-chartjs-2')) {
              return 'vendor_react_chartjs';
            }
            if(id.includes('react')) {
              return 'vendor_react';
            }
            if(id.includes('react-dom')) {
              return 'vendor_react_dom';
            }
            if(id.includes('axios')) {
              return 'vendor_axios';
            }
            return 'vendor-utils';
          }
        },
      },
    },
  },
});
