/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        // Operations-dashboard dark palette.
        ink: {
          950: "#0a0f1a",
          900: "#0f172a",
          850: "#141d31",
          800: "#1e293b",
          700: "#334155",
        },
        accent: {
          DEFAULT: "#34d399",
          soft: "#6ee7b7",
        },
      },
      fontFamily: {
        sans: [
          "Inter",
          "ui-sans-serif",
          "system-ui",
          "-apple-system",
          "Segoe UI",
          "Roboto",
          "sans-serif",
        ],
      },
    },
  },
  plugins: [],
};
