import preact from '@preact/preset-vite';
import { defineConfig, loadEnv, type UserConfigExport } from 'vite';

// https://vitejs.dev/config/
export default async ({ mode }): Promise<UserConfigExport> => {
  process.env = { ...loadEnv(mode, process.cwd()) };

  const port = parseInt(process.env.VITE_PORT, 10);

  return await defineConfig({
    plugins: [preact()],
    server: {
      port: isNaN(port) ? 3000 : port,
    },
  });
};
