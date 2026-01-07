/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        operational: '#10B981',
        partial: '#F59E0B',
        outage: '#EF4444',
        nodata: '#6B7280',
      },
    },
  },
  plugins: [],
};
