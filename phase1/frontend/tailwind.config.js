/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        paytm: {
          blue: "#00A8E0",
          navy: "#06283D",
          ink: "#17202A"
        }
      }
    }
  },
  plugins: []
};
