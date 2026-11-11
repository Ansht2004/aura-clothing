import React from 'react';
import { Link } from 'react-router-dom';
import { Heart, Trash2, ShoppingBag, Sparkles } from 'lucide-react';
import { useWishlist } from '../context/WishlistContext';
import { useCart } from '../context/CartContext';
import { useAuth } from '../context/AuthContext';
import { EmptyState } from '../components/common/EmptyState';
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import { ImageWithFallback } from '../components/common/ImageWithFallback';
import { formatPrice } from '../utils/formatters';

export const WishlistPage: React.FC = () => {
  const { wishlist, isLoading, removeFromWishlist } = useWishlist();
  const { addToCart } = useCart();
  const { isAuthenticated } = useAuth();

  if (!isAuthenticated) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-20">
        <div className="liquid-glass rounded-3xl p-12 text-center border border-white/70 dark:border-white/10 shadow-2xl">
          <EmptyState
            icon={Heart}
            title="Sign in to view your wishlist"
            description="Keep track of the garments you love. Sign in to sync your wishlist across all devices."
            actionText="Sign In / Register"
            actionLink="/auth"
          />
        </div>
      </div>
    );
  }

  if (isLoading && wishlist.length === 0) {
    return <LoadingSpinner fullPage message="Accessing Your Wishlist..." />;
  }

  if (wishlist.length === 0) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-20">
        <div className="liquid-glass rounded-3xl p-12 text-center border border-white/70 dark:border-white/10 shadow-2xl">
          <EmptyState
            icon={Heart}
            title="Your wishlist is empty"
            description="Explore our curated clothing collections and tap the heart icon to save items for future consideration."
            actionText="Explore Collections"
            actionLink="/products"
          />
        </div>
      </div>
    );
  }

  const handleQuickAdd = async (product: any) => {
    // Pick first available variant
    const variant = product.variants?.find((v: any) => v.stock_quantity > 0) || product.variants?.[0];
    if (variant) {
      await addToCart(variant.id, 1);
      await removeFromWishlist(product.id);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12 space-y-8">
      {/* Header Banner */}
      <div className="liquid-glass rounded-3xl p-6 sm:p-8 border border-white/70 dark:border-white/10 shadow-xl">
        <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full liquid-pill text-[10px] uppercase tracking-[0.2em] text-aura-gold font-bold">
          <Sparkles size={12} /> Curated Vault
        </span>
        <h1 className="text-2xl sm:text-4xl font-serif font-bold text-neutral-900 dark:text-neutral-100 mt-2">
          Your Curated Wishlist ({wishlist.length})
        </h1>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-5 sm:gap-6">
        {wishlist.map((item) => {
          const product = item.product;
          if (!product) return null;

          const effectivePrice = product.discount_price && product.discount_price > 0 ? product.discount_price : product.base_price;
          const hasDiscount = product.discount_price && product.discount_price > 0 && product.discount_price < product.base_price;

          return (
            <div key={item.id} className="group relative flex flex-col liquid-glass-card rounded-2xl overflow-hidden border border-white/80 dark:border-white/10 shadow-md transition-all">
              
              {/* Product Thumbnail */}
              <Link to={`/products/${product.id}`} className="relative aspect-[3/4] bg-neutral-100/60 dark:bg-neutral-900/60 overflow-hidden block">
                <ImageWithFallback
                  src={product.primary_image}
                  alt={product.name}
                  categoryName={product.category_name}
                  className="w-full h-full object-cover group-hover:scale-108 transition-transform duration-500 ease-out"
                />
                {hasDiscount && (
                  <span className="absolute top-3 left-3 bg-rose-500/90 backdrop-blur-md text-white text-[10px] font-bold uppercase tracking-wider px-2.5 py-0.5 rounded-full shadow-md border border-white/30">
                    Sale
                  </span>
                )}
                <button
                  onClick={(e) => {
                    e.preventDefault();
                    removeFromWishlist(product.id);
                  }}
                  className="absolute top-3 right-3 w-9 h-9 rounded-full liquid-pill flex items-center justify-center text-neutral-600 dark:text-neutral-400 hover:text-rose-500 dark:hover:text-rose-400 shadow-md transition-all"
                  title="Remove from wishlist"
                >
                  <Trash2 size={16} />
                </button>
              </Link>

              {/* Product Details */}
              <div className="p-4 flex flex-col flex-1 justify-between">
                <div>
                  <span className="text-[10px] uppercase tracking-[0.2em] text-aura-gold font-bold">
                    {product.brand}
                  </span>
                  <Link to={`/products/${product.id}`} className="block mt-1">
                    <h3 className="text-sm font-semibold text-neutral-900 dark:text-neutral-100 line-clamp-1 group-hover:text-aura-gold transition-colors">
                      {product.name}
                    </h3>
                  </Link>

                  <div className="flex items-baseline gap-2 mt-2">
                    <span className="text-base font-bold text-neutral-900 dark:text-neutral-100 font-mono">
                      {formatPrice(effectivePrice)}
                    </span>
                    {hasDiscount && (
                      <span className="text-xs text-neutral-400 dark:text-neutral-500 line-through font-mono">
                        {formatPrice(product.base_price)}
                      </span>
                    )}
                  </div>
                </div>

                <div className="mt-3.5 pt-3 border-t border-neutral-200/50 dark:border-neutral-800/60">
                  <button
                    onClick={() => handleQuickAdd(product)}
                    className="w-full py-2.5 liquid-btn-gold text-neutral-950 text-xs uppercase tracking-wider font-bold rounded-xl shadow-md transition-all flex items-center justify-center gap-1.5"
                  >
                    <ShoppingBag size={14} />
                    <span>Move to Bag</span>
                  </button>
                </div>
              </div>

            </div>
          );
        })}
      </div>
    </div>
  );
};
