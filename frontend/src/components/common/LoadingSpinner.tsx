import React from 'react';

export const LoadingSpinner: React.FC<{ message?: string; fullPage?: boolean }> = ({ 
  message = "Loading...", 
  fullPage = false 
}) => {
  const content = (
    <div className="flex flex-col items-center justify-center p-8 gap-4 liquid-glass rounded-3xl border border-white/70 dark:border-white/10 shadow-2xl max-w-sm mx-auto">
      <div className="relative w-12 h-12 flex items-center justify-center">
        <div className="absolute inset-0 rounded-full border-2 border-aura-gold/20 animate-ping" />
        <div className="w-10 h-10 border-2 border-aura-gold/30 border-t-aura-gold rounded-full animate-spin" />
      </div>
      <span className="text-xs uppercase tracking-[0.2em] text-aura-gold font-bold">
        {message}
      </span>
    </div>
  );

  if (fullPage) {
    return (
      <div className="min-h-[60vh] flex items-center justify-center px-4">
        {content}
      </div>
    );
  }

  return content;
};
