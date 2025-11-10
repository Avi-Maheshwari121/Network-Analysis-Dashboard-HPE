/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'base-dark': '#0D1117',
        'surface-dark': '#161B22',
        'primary-accent': '#2DD4BF',
        'text-main': '#E6EDF3',
        'text-secondary': '#8B949E',
        'border-dark': '#30363D',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-8px)' },
        },
        fadeIn: {
          '0%': { opacity: '0', transform: 'translateY(10px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        fadeOut: {
          '0%': { opacity: '1', transform: 'translateY(0)' },
          '100%': { opacity: '0', transform: 'translateY(10px)' },
        },
        // --- ADDED PULSE FOR GLOW ---
        // Tailwind's default pulse is fine, but a custom one can be softer.
        // Let's just use the built-in `animate-pulse` for simplicity.
        // If you want a custom one, you'd add it here.
      },
      animation: {
        float: 'float 3s ease-in-out infinite',
        fadeIn: 'fadeIn 0.5s ease-out forwards',
        fadeOut: 'fadeOut 0.5s ease-in forwards',
        // `animate-pulse` is already available by default in Tailwind
      },
    },
  },
  plugins: [],
}