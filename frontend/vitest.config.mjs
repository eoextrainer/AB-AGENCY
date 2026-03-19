import { defineConfig } from "vitest/config";
import path from "node:path";

export default defineConfig({
  esbuild: {
    loader: "jsx",
    jsx: "automatic",
    jsxImportSource: "react",
    include: /.*\.[jt]sx?$/,
    exclude: []
  },
  test: {
    environment: "jsdom",
    setupFiles: ["./tests/setup.js"],
    globals: true
  },
  resolve: {
    alias: {
      "@": path.resolve(process.cwd())
    }
  }
});