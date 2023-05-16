import { defineConfig, loadEnv } from 'vite';
import preact from '@preact/preset-vite';

// https://vitejs.dev/config/
export default ({ mode }) => {
  process.env = {...loadEnv(mode, process.cwd())};

  const port = process.env.VITE_PORT;

  return defineConfig({
    plugins: [preact()],
    server: {
      port: parseInt(port as string, 10) || 3000,
    },
  });
};
