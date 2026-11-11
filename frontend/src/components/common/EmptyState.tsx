import React from 'react';
import { Link } from 'react-router-dom';
import { LucideIcon } from 'lucide-react';

interface EmptyStateProps {
  icon: LucideIcon;
  title: string;
  description: string;
  actionText?: string;
  actionLink?: string;
  onAction?: () => void;
}

export const EmptyState: React.FC<EmptyStateProps> = ({
  icon: Icon,
  title,
  description,
  actionText,
  actionLink,
  onAction
}) => {
  return (
    <div className="flex flex-col items-center justify-center text-center p-12 bg-white rounded-sm border border-neutral-100 max-w-md mx-auto my-8">
      <div className="w-16 h-16 rounded-full bg-aura-100 flex items-center justify-center text-aura-gold mb-4">
        <Icon size={28} strokeWidth={1.5} />
      </div>
      <h3 className="text-lg font-serif font-semibold text-neutral-900 mb-2">
        {title}
      </h3>
      <p className="text-sm text-neutral-500 mb-6 max-w-sm leading-relaxed">
        {description}
      </p>

      {actionText && actionLink && (
        <Link
          to={actionLink}
          className="inline-flex items-center justify-center px-6 py-2.5 bg-neutral-900 hover:bg-black text-white text-xs uppercase tracking-widest font-semibold rounded-sm transition-all"
        >
          {actionText}
        </Link>
      )}

      {actionText && onAction && !actionLink && (
        <button
          onClick={onAction}
          className="inline-flex items-center justify-center px-6 py-2.5 bg-neutral-900 hover:bg-black text-white text-xs uppercase tracking-widest font-semibold rounded-sm transition-all"
        >
          {actionText}
        </button>
      )}
    </div>
  );
};
