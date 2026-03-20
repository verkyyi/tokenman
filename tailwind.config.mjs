/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,ts,tsx}'],
  theme: {
    extend: {
      typography: {
        DEFAULT: {
          css: {
            maxWidth: 'none',
            color: '#374151',
            a: { color: '#111827', textDecoration: 'underline' },
            'h1, h2, h3, h4': { color: '#111827', fontWeight: '600' },
          },
        },
      },
    },
  },
  plugins: [],
};
