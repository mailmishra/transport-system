import type { Config } from "tailwindcss";

// Design tokens from the approved Style B ("Freight ERP") mockup:
// https://claude.ai/artifact/HTUkVrMB3aozxAuaJY57oT
export default {
  darkMode: ["class"],
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        navy: {
          DEFAULT: "#122A42",
          light: "#1C3A57",
        },
        gold: {
          DEFAULT: "#C89B3C",
        },
        status: {
          paid: "#12805C",
          pending: "#B4670E",
          overdue: "#B23A2E",
        },
        border: "#DCE2E8",
        background: "#EEF1F5",
        foreground: "#1C2430",
        muted: "#7A8797",
      },
      fontFamily: {
        sans: ["IBM Plex Sans", "system-ui", "sans-serif"],
        mono: ["IBM Plex Mono", "monospace"],
      },
      borderRadius: {
        DEFAULT: "5px",
      },
    },
  },
  plugins: [],
} satisfies Config;
