// vite.config.js
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// https://vite.dev/config/
export default defineConfig({
  base: "/Connecto/",
  plugins: [react()],
  server: {
    port: 3000,
    open: false,
  },
});
