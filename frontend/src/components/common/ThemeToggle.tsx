import React from 'react';
import { Sun, Moon } from 'lucide-react';
import { useTheme } from '../../context/ThemeContext';

interface ThemeToggleProps {
  className?: string;
}

export const ThemeToggle: React.FC<ThemeToggleProps> = ({ className = '' }) => {
  const { theme, toggleTheme } = useTheme();
  const isDark = theme === 'dark';

  return (
    <button
      type="button"
      onClick={toggleTheme}
      className={`relative inline-flex items-center h-8 w-[58px] shrink-0 rounded-full p-1 transition-all duration-300 focus:outline-none select-none cursor-pointer ${
        isDark
          ? 'bg-neutral-900 border border-neutral-700/80 shadow-[inset_0_2px_5px_rgba(0,0,0,0.7)]'
          : 'bg-neutral-200/90 hover:bg-neutral-200 border border-neutral-300/90 shadow-[inset_0_2px_4px_rgba(0,0,0,0.1)]'
      } ${className}`}
      aria-label={isDark ? 'Switch to Day / Light Mode' : 'Switch to Night / Dark Mode'}
      title={isDark ? 'Switch to Day Mode (Light)' : 'Switch to Night Mode (Dark)'}
    >
      <span className="sr-only">Toggle theme</span>

      {/* Track Background Day / Night Icons */}
      <span className="absolute inset-0 flex items-center justify-between px-2.5 pointer-events-none">
        <Sun
          size={12}
          strokeWidth={2.5}
          className={`transition-opacity duration-300 ${
            isDark ? 'text-neutral-400 opacity-60' : 'opacity-0'
          }`}
        />
        <Moon
          size={12}
          strokeWidth={2.5}
          className={`transition-opacity duration-300 ${
            isDark ? 'opacity-0' : 'text-neutral-500 opacity-70'
          }`}
        />
      </span>

      {/* Tactile Sliding Ceramic & Gold Knob */}
      <span
        className={`pointer-events-none inline-flex items-center justify-center w-6 h-6 rounded-full transform transition-transform duration-300 ease-out shadow-md ${
          isDark
            ? 'translate-x-[26px] bg-gradient-to-tr from-aura-gold to-aura-goldLight text-neutral-950 shadow-[0_0_12px_rgba(197,160,89,0.55)]'
            : 'translate-x-0 bg-white text-amber-500 shadow-[0_2px_6px_rgba(0,0,0,0.18),0_0_0_1px_rgba(197,160,89,0.25)]'
        }`}
      >
        {isDark ? (
          <Moon size={13} strokeWidth={2.5} className="text-neutral-950 fill-neutral-950" />
        ) : (
          <Sun size={13} strokeWidth={2.5} className="text-amber-500" />
        )}
      </span>
    </button>
  );
};
