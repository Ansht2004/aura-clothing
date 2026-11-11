import React from 'react';
import { Link } from 'react-router-dom';
import { Heart, Sparkles } from 'lucide-react';
import { Product } from '../../types';
import { ReviewStars } from './ReviewStars';
import { ImageWithFallback } from './ImageWithFallback';
import { useWishlist } from '../../context/WishlistContext';
import { formatPrice } from '../../utils/formatters';

interface ProductCardProps {
  product: Product;
  recommendationScore?: number;
  recommendationBreakdown?: any;
}

export const ProductCard: React.FC<ProductCardProps> = ({ 
  product, 
  recommendationScore,
  recommendationBreakdown 
}) => {
  const { isInWishlist, toggleWishlist } = useWishlist();
  const wishlisted = isInWishlist(product.id);

  const hasDiscount = product.discount_price && product.discount_price > 0 && product.discount_price < product.base_price;
  const discountPercent = hasDiscount 
    ? Math.round(((product.base_price - product.discount_price!) / product.base_price) * 100) 
    : 0;

  const handleWishlistClick = (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    toggleWishlist(product.id);
  };

  return (
    <div className="group relative flex flex-col liquid-glass-card overflow-hidden rounded-2xl border border-white/85 dark:border-white/10 transition-all duration-400">
      
      {/* Product Image Stage */}
      <Link to={`/products/${product.id}`} className="relative block aspect-[3/4] overflow-hidden bg-neutral-100/60 dark:bg-neutral-900/60">
        <ImageWithFallback
          src={product.primary_image}
          alt={product.name}
          categoryName={product.category_name}
          className="w-full h-full object-cover object-center group-hover:scale-108 transition-transform duration-700 ease-out"
        />

        {/* Specular Liquid Gradient Sheen Overlay */}
        <div className="absolute inset-0 bg-gradient-to-t from-black/40 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none" />

        {/* Liquid Badges Overlay */}
        <div className="absolute top-3 left-3 flex flex-col gap-1.5 z-10 pointer-events-none">
          {hasDiscount && (
            <span className="bg-rose-500/90 backdrop-blur-md text-white text-[9.5px] font-bold tracking-widest px-2.5 py-0.5 rounded-full shadow-md border border-white/30 animate-pulse uppercase">
              {discountPercent}% OFF
            </span>
          )}
          {product.is_featured && !hasDiscount && (
            <span className="liquid-pill text-aura-gold dark:text-aura-goldLight font-bold text-[9.5px] uppercase tracking-widest px-2.5 py-0.5 shadow-sm">
              Featured
            </span>
          )}
          {!product.in_stock && (
            <span className="bg-neutral-900/80 backdrop-blur-md text-neutral-300 text-[9.5px] uppercase font-bold tracking-widest px-2.5 py-0.5 rounded-full border border-white/10">
              Sold Out
            </span>
          )}
          {recommendationScore !== undefined && (
            <span 
              className="liquid-btn-gold text-neutral-950 text-[9.5px] font-bold tracking-wider px-2.5 py-0.5 rounded-full shadow-md flex items-center gap-1 uppercase"
              title={`MCA Ranking Score: ${(recommendationScore * 100).toFixed(0)}% Match`}
            >
              <Sparkles size={9} />
              {(recommendationScore * 100).toFixed(0)}% Match
            </span>
          )}
        </div>

        {/* Liquid Glass Floating Wishlist Button */}
        <button
          onClick={handleWishlistClick}
          aria-label={wishlisted ? 'Remove from wishlist' : 'Add to wishlist'}
          className="absolute top-3 right-3 z-10 w-9 h-9 rounded-full liquid-pill flex items-center justify-center text-neutral-700 dark:text-neutral-300 hover:text-rose-500 dark:hover:text-rose-400 hover:scale-110 active:scale-95 shadow-md transition-all duration-200"
        >
          <Heart size={15} className={wishlisted ? 'fill-rose-500 text-rose-500' : ''} />
        </button>

        {/* Quick Sizes Preview Revealed on Hover */}
        <div className="absolute bottom-3 inset-x-3 liquid-glass py-1.5 px-3 rounded-xl text-center text-[10.5px] font-medium tracking-wider text-neutral-800 dark:text-neutral-200 opacity-0 group-hover:opacity-100 transform translate-y-2 group-hover:translate-y-0 transition-all duration-300 shadow-xl border border-white/80 dark:border-white/20 uppercase">
          Sizes: {product.available_sizes?.join(' · ') || 'Standard'}
        </div>
      </Link>

      {/* Product Details Section */}
      <div className="p-4 flex flex-col flex-1 justify-between">
        <div>
          <div className="text-[9.5px] text-aura-gold dark:text-aura-goldLight uppercase tracking-[0.25em] font-semibold mb-1">
            {product.category_name || product.brand}
          </div>
          <Link to={`/products/${product.id}`} className="block">
            <h3 className="font-serif text-[15px] sm:text-base font-normal tracking-tight text-neutral-900 dark:text-neutral-100 line-clamp-1 group-hover:text-aura-gold transition-colors duration-200">
              {product.name}
            </h3>
          </Link>
          
          <div className="mt-1.5 flex items-center gap-1.5">
            <ReviewStars rating={product.average_rating} reviewCount={product.review_count} size={11} />
          </div>
        </div>

        {/* Pricing & Stock Status */}
        <div className="mt-3.5 pt-3 border-t border-neutral-200/50 dark:border-neutral-800/60 flex items-center justify-between">
          <div className="flex items-baseline gap-2">
            <span className="text-[15px] font-semibold text-neutral-950 dark:text-neutral-50 tracking-tight">
              {formatPrice(product.discount_price && product.discount_price > 0 ? product.discount_price : product.base_price)}
            </span>
            {hasDiscount && (
              <span className="text-xs text-neutral-400 dark:text-neutral-500 line-through">
                {formatPrice(product.base_price)}
              </span>
            )}
          </div>
          
          <div className="flex items-center gap-1.5 text-[10.5px] font-medium text-neutral-500 dark:text-neutral-400">
            <span className={`w-1.5 h-1.5 rounded-full ${product.in_stock ? 'bg-emerald-500 shadow-[0_0_8px_rgba(16,185,129,0.7)]' : 'bg-neutral-400'}`} />
            <span>{product.in_stock ? 'In Stock' : 'Out of Stock'}</span>
          </div>
        </div>
      </div>
    </div>
  );
};
