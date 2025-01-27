import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  optimizeDeps: {
    include: ["leaflet", "leaflet-routing-machine"],
  },
  resolve: {
    alias: {
      "leaflet-routing-machine": "leaflet-routing-machine",
    },
  },
});
