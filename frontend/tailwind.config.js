/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#6C63FF', // Electric Purple
          light: '#8F88FF',
          dark: '#4B44CC',
        },
        secondary: {
          DEFAULT: '#00C9A7', // Ocean Teal
          light: '#4DDFC6',
          dark: '#00967D',
        },
        accent: {
          orange: '#FF8C42', // Sunset Orange
          yellow: '#FFD93D', // Sunny Yellow
          pink: '#FF5D8F',   // Bubblegum Pink
        },
        surface: {
          DEFAULT: '#F9F9F9', // Soft Cream
          card: '#FFFFFF',
        },
        dark: {
          DEFAULT: '#1A1B41', // Deep Navy
          surface: '#25265E',
        }
      },
      fontFamily: {
        sans: ['Nunito', 'Quicksand', 'sans-serif'],
        heading: ['Fredoka One', 'Baloo 2', 'cursive'],
      },
      borderRadius: {
        'xl': '1rem',
        '2xl': '1.5rem',
        '3xl': '2rem',
      }
    },
  },
  plugins: [],
}
