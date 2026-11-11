import React, { useState } from 'react';
import { Shirt } from 'lucide-react';

interface ImageWithFallbackProps extends React.ImgHTMLAttributes<HTMLImageElement> {
  fallbackSrc?: string;
  categoryName?: string;
}

// Fallback luxury placeholder SVG encoded as data URI
const DEFAULT_FALLBACK_SVG = "data:image/svg+xml;charset=UTF-8,%3Csvg xmlns='http://www.w3.org/2000/svg' width='600' height='800' viewBox='0 0 600 800'%3E%3Crect width='600' height='800' fill='%23F4F1EC'/%3E%3Cpath d='M250 280 L350 280 L380 480 L220 480 Z' fill='%23E5DEC9'/%3E%3Ccircle cx='300' cy='230' r='35' fill='%23C5A059' opacity='0.3'/%3E%3Ctext x='300' y='540' font-family='serif' font-size='22' font-weight='600' letter-spacing='4' fill='%231F2421' text-anchor='middle'%3EAURA APPAREL%3C/text%3E%3Ctext x='300' y='575' font-family='sans-serif' font-size='12' letter-spacing='2' fill='%238C8275' text-anchor='middle'%3EHAUTE COLLECTION%3C/text%3E%3C/svg%3E";

export const ImageWithFallback: React.FC<ImageWithFallbackProps> = ({
  src,
  alt = 'Aura Apparel Piece',
  className = '',
  fallbackSrc = DEFAULT_FALLBACK_SVG,
  categoryName,
  ...props
}) => {
  const [imgSrc, setImgSrc] = useState<string>(src || fallbackSrc);
  const [hasError, setHasError] = useState<boolean>(!src);
  const [isLoaded, setIsLoaded] = useState<boolean>(false);

  // Sync state when src prop updates
  React.useEffect(() => {
    if (src) {
      setImgSrc(src);
      setHasError(false);
      setIsLoaded(false);
    } else {
      setImgSrc(fallbackSrc);
      setHasError(true);
    }
  }, [src, fallbackSrc]);

  const handleError = () => {
    if (!hasError) {
      setHasError(true);
      setImgSrc(fallbackSrc);
    }
  };

  return (
    <div className={`relative overflow-hidden bg-neutral-100/80 dark:bg-neutral-900/80 ${className}`}>
      {/* Loading Skeleton Shimmer */}
      {!isLoaded && !hasError && (
        <div className="absolute inset-0 bg-gradient-to-r from-neutral-200/50 via-neutral-100/70 to-neutral-200/50 dark:from-neutral-800/40 dark:via-neutral-700/50 dark:to-neutral-800/40 animate-pulse pointer-events-none" />
      )}

      <img
        {...props}
        src={imgSrc}
        alt={alt}
        referrerPolicy="no-referrer"
        loading="lazy"
        decoding="async"
        onLoad={() => setIsLoaded(true)}
        onError={handleError}
        className={`w-full h-full object-cover object-center transition-opacity duration-500 ${
          isLoaded || hasError ? 'opacity-100' : 'opacity-0'
        }`}
      />

      {hasError && categoryName && (
        <div className="absolute inset-0 flex flex-col items-center justify-center p-4 bg-aura-50/90 dark:bg-neutral-900/90 text-center pointer-events-none">
          <Shirt size={28} className="text-aura-gold mb-2 opacity-60" />
          <span className="text-xs font-serif font-bold tracking-wider text-neutral-800 dark:text-neutral-200 uppercase">
            {categoryName}
          </span>
          <span className="text-[10px] text-neutral-500 dark:text-neutral-400 tracking-widest uppercase mt-0.5">
            Aura Haute Collection
          </span>
        </div>
      )}
    </div>
  );
};
