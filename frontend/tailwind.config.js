/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        aura: {
          50: '#FAF7F2',
          100: '#F5F0E6',
          200: '#E8E1D3',
          300: '#D5C7B2',
          400: '#B5A285',
          500: '#927E61',
          600: '#736148',
          700: '#554734',
          800: '#382F22',
          900: '#1C1710',
          dark: '#0C0B0A',
          gold: '#C5A059',
          goldLight: '#DFBE7A',
          goldLighter: '#F3E4C0',
          goldDark: '#9E7D38',
        },
        alabaster: '#FAF7F2',
        ivory: '#F4EFE6',
        velvet: '#0C0B0A',
        onyx: '#141312',
        obsidian: '#181716',
        champagne: {
          50: '#FAF8F4',
          100: '#F5F0E5',
          200: '#EBE0C7',
          300: '#DFBE7A',
          400: '#D4AF37',
          500: '#C5A059',
          600: '#A8843B',
          700: '#7E6328',
        }
      },
      fontFamily: {
        serif: ['"Cormorant Garamond"', '"Playfair Display"', 'Georgia', 'serif'],
        display: ['"Cormorant Garamond"', '"Playfair Display"', 'Georgia', 'serif'],
        sans: ['"Plus Jakarta Sans"', '"Inter"', 'system-ui', '-apple-system', 'sans-serif'],
      },
      backdropBlur: {
        xs: '2px',
        '2xl': '24px',
        '3xl': '40px',
      },
      boxShadow: {
        'liquid': '0 8px 32px 0 rgba(31, 38, 135, 0.05), inset 0 1px 1px 0 rgba(255, 255, 255, 0.85), inset 0 0 0 1px rgba(197, 160, 89, 0.08)',
        'liquid-hover': '0 16px 44px -4px rgba(197, 160, 89, 0.16), inset 0 1px 2px 0 rgba(255, 255, 255, 1), inset 0 0 0 1px rgba(197, 160, 89, 0.22)',
        'liquid-dark': '0 12px 40px -4px rgba(0, 0, 0, 0.65), inset 0 1px 1px 0 rgba(255, 255, 255, 0.14), inset 0 0 0 1px rgba(197, 160, 89, 0.12)',
        'liquid-dark-hover': '0 22px 55px -6px rgba(0, 0, 0, 0.85), inset 0 1px 2px 0 rgba(255, 255, 255, 0.24), inset 0 0 0 1px rgba(197, 160, 89, 0.28)',
        'liquid-gold': '0 8px 30px -4px rgba(197, 160, 89, 0.45), inset 0 1px 2px rgba(255, 255, 255, 0.6)',
        'crystal': '0 10px 30px -5px rgba(0, 0, 0, 0.04), inset 0 1px 1px 0 rgba(255, 255, 255, 0.95), inset 0 0 0 1px rgba(197, 160, 89, 0.1)',
        'glass-glow': '0 0 30px rgba(197, 160, 89, 0.2)',
      },
      animation: {
        'float-slow': 'floatSlow 9s ease-in-out infinite',
        'float-reverse': 'floatReverse 11s ease-in-out infinite',
        'pulse-glow': 'pulseGlow 5s ease-in-out infinite',
        'shimmer': 'shimmer 3s ease-in-out infinite',
      },
      keyframes: {
        floatSlow: {
          '0%, 100%': { transform: 'translate(0px, 0px) scale(1)' },
          '50%': { transform: 'translate(25px, -20px) scale(1.05)' },
        },
        floatReverse: {
          '0%, 100%': { transform: 'translate(0px, 0px) scale(1)' },
          '50%': { transform: 'translate(-20px, 25px) scale(0.95)' },
        },
        pulseGlow: {
          '0%, 100%': { opacity: '0.45', transform: 'scale(1)' },
          '50%': { opacity: '0.75', transform: 'scale(1.08)' },
        },
        shimmer: {
          '0%': { backgroundPosition: '-200% 0' },
          '100%': { backgroundPosition: '200% 0' },
        }
      }
    },
  },
  plugins: [],
}
