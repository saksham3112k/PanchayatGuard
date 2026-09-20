/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        pg: {
          navy: '#0A2540',
          blue: '#1E40AF',
          green: '#10B981',
          amber: '#F59E0B',
          red: '#EF4444',
          slate: '#475569',
          light: '#F8FAFC'
        }
      }
    },
  },
  plugins: [],
}
