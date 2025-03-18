import { defineConfig, loadEnv } from 'vite';
import vue from '@vitejs/plugin-vue';

export default defineConfig(({ mode }) => {
  // Load the correct .env file based on the mode
  const env = loadEnv(mode, process.cwd());

  return {
    plugins: [
      vue({
        template: {
          compilerOptions: {
            // ✅ Ignore <v-motion> component warning
            isCustomElement: (tag) => tag === "v-motion",
          },
        },
      }),
    ],
    define: {
      'import.meta.env.VITE_API_BASE_URL': JSON.stringify(env.VITE_API_BASE_URL),
    },
  };
});
