import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: 'class',
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        // Light theme
        light: {
          bg: '#f8fafc',
          surface: '#ffffff',
          text: '#1e293b',
          textMuted: '#64748b',
          border: '#e2e8f0',
        },
        // Dark theme
        dark: {
          bg: '#0f172a',
          surface: '#1e293b',
          text: '#f1f5f9',
          textMuted: '#94a3b8',
          border: '#334155',
        },
        // Brand colors
        primary: {
          DEFAULT: '#6366f1',
          hover: '#4f46e5',
          light: '#818cf8',
          dark: '#4f46e5',
        },
        success: {
          DEFAULT: '#10b981',
          light: '#34d399',
        },
        warning: {
          DEFAULT: '#f59e0b',
          light: '#fbbf24',
        },
        error: {
          DEFAULT: '#ef4444',
          light: '#f87171',
        },
      },
      boxShadow: {
        '3d': '0 4px 0 var(--primary-dark), 0 5px 10px rgba(0,0,0,0.2)',
        '3d-hover': '0 6px 0 var(--primary-dark), 0 8px 15px rgba(0,0,0,0.25)',
        '3d-active': '0 2px 0 var(--primary-dark), 0 3px 5px rgba(0,0,0,0.2)',
        'card': '5px 5px 10px rgba(0,0,0,0.1), -5px -5px 10px rgba(255,255,255,0.8)',
        'card-dark': '5px 5px 10px rgba(0,0,0,0.3), -5px -5px 10px rgba(255,255,255,0.05)',
      },
      animation: {
        'lift': 'lift 0.2s ease-out',
        'press': 'press 0.1s ease-out',
      },
      keyframes: {
        lift: {
          '0%': { transform: 'translateY(0)' },
          '100%': { transform: 'translateY(-2px)' },
        },
        press: {
          '0%': { transform: 'translateY(0)' },
          '100%': { transform: 'translateY(2px)' },
        },
      },
    },
  },
  plugins: [],
};
export default config;
