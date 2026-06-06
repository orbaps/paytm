/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'canvas-cream': '#F3F0EE',
        'lifted-cream': '#FCFBFA',
        'ink-black': '#141413',
        'signal-orange': '#CF4500',
        'light-orange': '#F37338',
      },
      fontFamily: {
        'sans': ['Outfit', 'system-ui', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
