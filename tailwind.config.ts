import type { Config } from "tailwindcss"

const config: Config = {
  darkMode: "class",
  content: [
    "./pages/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    "./app/**/*.{ts,tsx}",
    "./src/**/*.{ts,tsx}",
  ],
  theme: {
    container: {
      center: true,
      padding: "2rem",
      screens: {
        "2xl": "1400px",
      },
    },
    extend: {
      colors: {
        "vaporwave-pink": "#ff71ce",
        "vaporwave-blue": "#01cdfe",
        "vaporwave-purple": "#b967ff",
        "vaporwave-yellow": "#fffb96",
        "vaporwave-teal": "#05ffa1",
        "vaporwave-dark": "#1a1a1a",
      },
      backgroundImage: {
        "vaporwave-gradient": "linear-gradient(45deg, #ff71ce, #01cdfe, #05ffa1)",
      },
    },
  },
  plugins: [],
}

export default config

