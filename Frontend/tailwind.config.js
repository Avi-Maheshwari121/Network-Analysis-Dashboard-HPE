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
      }
    },
  },
  plugins: [],
}
