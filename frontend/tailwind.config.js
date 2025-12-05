/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  darkMode: 'class', // Enable class-based dark mode
  theme: {
    extend: {
      colors: {
        primary: '#0070f3',
        'primary-hover': '#0051cc',
        secondary: '#6c757d',
        'secondary-hover': '#5a6268',
        danger: '#dc3545',
        'danger-hover': '#c82333',
        success: '#28a745',
      },
    },
  },
  plugins: [],
}
