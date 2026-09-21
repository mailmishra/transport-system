import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  server: {
    // Local dev only: the built app is served by FastAPI's StaticFiles in
    // production (see backend/app/main.py), so this proxy only matters
    // when running `npm run dev` against `docker compose up`'s backend.
    proxy: {
      "/api": "http://localhost:8000",
      "/media": "http://localhost:8000",
    },
  },
});
