export default {
  darkMode: ["class"],
  content: [
    './Pages/**/*.{js,jsx}',
    './Components/**/*.{js,jsx}',
    './index.html',
    './*.{js,jsx}',
  ],
  theme: {
    extend: {
      colors: {
        // Classic Theme (Legacy)
        primary: {
          DEFAULT: '#1e3a5f',
          50: '#f0f4f8',
          500: '#1e3a5f',
          600: '#1a324f',
        },
        secondary: {
          DEFAULT: '#2563eb',
          500: '#2563eb',
        },
        accent: {
          DEFAULT: '#c9a227',
          500: '#c9a227',
        },
        // Shadow Seven - Cyber Theme
        shadow: {
          bg: '#0a0a0f',           // Dark background
          surface: '#1a1a2e',      // Dark surfaces
          card: '#16213e',         // Card background
          primary: '#00ff88',      // Neon green
          secondary: '#ff0080',    // Neon pink
          accent: '#00d4ff',       // Neon cyan
          text: '#e0e0e0',         // Light text
          muted: '#666677',        // Muted text
          border: '#2a2a3e',       // Borders
          hover: '#252540',        // Hover state
        },
        glow: {
          green: 'rgba(0, 255, 136, 0.3)',
          pink: 'rgba(255, 0, 128, 0.3)',
          blue: 'rgba(0, 212, 255, 0.3)',
          purple: 'rgba(138, 43, 226, 0.3)',
        },
      },
      fontFamily: {
        sans: ['Cairo', 'system-ui', 'sans-serif'],
        arabic: ['Noto Kufi Arabic', 'Cairo', 'sans-serif'],
        cyber: ['Orbitron', 'Rajdhani', 'monospace'],
      },
      boxShadow: {
        'neon': '0 0 20px rgba(0, 255, 136, 0.5)',
        'neon-pink': '0 0 20px rgba(255, 0, 128, 0.5)',
        'neon-blue': '0 0 20px rgba(0, 212, 255, 0.5)',
        'neon-purple': '0 0 20px rgba(138, 43, 226, 0.5)',
        'cyber': '0 4px 20px rgba(0, 255, 136, 0.2)',
      },
      keyframes: {
        "accordion-down": {
          from: { height: "0" },
          to: { height: "var(--radix-accordion-content-height)" },
        },
        "accordion-up": {
          from: { height: "var(--radix-accordion-content-height)" },
          to: { height: "0" },
        },
        "glow": {
          '0%, 100%': { opacity: '1', filter: 'brightness(1)' },
          '50%': { opacity: '0.8', filter: 'brightness(1.2)' },
        },
        "scan": {
          '0%': { transform: 'translateY(-100%)' },
          '100%': { transform: 'translateY(100%)' },
        },
        "pulse-neon": {
          '0%, 100%': { boxShadow: '0 0 5px rgba(0, 255, 136, 0.5)' },
          '50%': { boxShadow: '0 0 20px rgba(0, 255, 136, 0.8)' },
        },
        "slide-in": {
          '0%': { transform: 'translateX(100%)', opacity: '0' },
          '100%': { transform: 'translateX(0)', opacity: '1' },
        },
      },
      animation: {
        "accordion-down": "accordion-down 0.2s ease-out",
        "accordion-up": "accordion-up 0.2s ease-out",
        "glow": "glow 2s ease-in-out infinite",
        "scan": "scan 8s linear infinite",
        "pulse-neon": "pulse-neon 2s ease-in-out infinite",
        "slide-in": "slide-in 0.3s ease-out",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
}
