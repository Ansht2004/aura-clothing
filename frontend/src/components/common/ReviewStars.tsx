import React from 'react';
import { Star } from 'lucide-react';

interface ReviewStarsProps {
  rating: number;
  maxStars?: number;
  size?: number;
  showScore?: boolean;
  reviewCount?: number;
}

export const ReviewStars: React.FC<ReviewStarsProps> = ({
  rating,
  maxStars = 5,
  size = 14,
  showScore = false,
  reviewCount
}) => {
  return (
    <div className="flex items-center gap-1.5">
      <div className="flex items-center text-amber-500">
        {Array.from({ length: maxStars }).map((_, idx) => {
          const filled = idx + 1 <= Math.round(rating);
          return (
            <Star
              key={idx}
              size={size}
              className={`${filled ? 'fill-amber-400 text-amber-400' : 'text-neutral-300'}`}
            />
          );
        })}
      </div>
      {showScore && (
        <span className="text-xs font-medium text-neutral-700 ml-1">
          {rating.toFixed(1)}
        </span>
      )}
      {reviewCount !== undefined && (
        <span className="text-xs text-neutral-400">
          ({reviewCount})
        </span>
      )}
    </div>
  );
};
