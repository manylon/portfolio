import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";
import mkcert from "vite-plugin-mkcert";

const __dirname = new URL(".", import.meta.url).pathname;

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss(), mkcert()],
  server: { https: true }, // Not needed for Vite 5+
  resolve: {
    alias: {
      "@": `${__dirname}/src`,
      "@components": `${__dirname}/src/components`,
      "@pages": `${__dirname}/src/app/pages`,
      "@assets": `${__dirname}/src/assets`,
      "@styles": `${__dirname}/src/styles`,
      "@ctypes": `${__dirname}/src/types`,
    },
  },
});
