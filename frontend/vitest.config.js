// frontend/vitest.config.js

import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  test: {
    environment: "jsdom",
    globals: true,
    setupFiles: ["./tests/setupTests.js"],
    test:{
      root: "./tests", // Set the root directory for tests
    },
    include: ["**/*.{test,spec}.{js,jsx}"], // Only include unit test files
    exclude: ["**/node_modules/**", "**/tests/e2e/**"], // Exclude e2e tests
  },
});
