import { defineConfig, loadEnv } from 'vite';
import preact from '@preact/preset-vite';

// https://vitejs.dev/config/
export default ({ mode }) => {
  process.env = {...loadEnv(mode, process.cwd())};

  const apiAddress = process.env.VITE_API_ADDRESS;
  const apiPort = process.env.VITE_API_PORT;

  return defineConfig({
    plugins: [preact()],
    server: {
      proxy: {
        '/api': {
          target: `http://${apiAddress}:${apiPort}/api`,
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/api/, ''),
        },
      },
    },
  });
};
