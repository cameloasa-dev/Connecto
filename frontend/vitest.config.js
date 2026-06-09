// frontend/vitest.config.js

import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  test: {
    environment: "jsdom",
    globals: true,
    setupFiles: ["./tests/setupTests.js"],
    include: ["**/*.{test,spec}.{js,jsx}"],
    exclude: ["**/node_modules/**", "**/e2e/**"],
  },
});
