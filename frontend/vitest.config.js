//frontend/vitest.config.js
import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";
import "@testing-library/jest-dom/vitest";

export default defineConfig({
  plugins: [react()],
  test: {
    environment: "jsdom",
    globals: true,

    setupFiles: ["./tests/integration/setup/setupTests.js"],

    include: [
      "tests/unit/**/*.{test,spec}.{js,jsx}",
      "tests/integration/**/*.{test,spec}.{js,jsx}",
    ],

    exclude: ["node_modules", "tests/e2e/**"],
  },
  coverage: {
    provider: "v8",
    reporter: ["text", "html"],
    reportsDirectory: "./coverage",
    all: true,
    include: ["src/**/*.{js,jsx}"],
  },
});
