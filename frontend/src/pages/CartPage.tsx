import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { 
  Trash2, ShoppingBag, ArrowRight, Tag, 
  Check, AlertCircle, ShieldCheck, Truck, X, Sparkles 
} from 'lucide-react';
import { useCart } from '../context/CartContext';
import { useAuth } from '../context/AuthContext';
import { EmptyState } from '../components/common/EmptyState';
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import { ImageWithFallback } from '../components/common/ImageWithFallback';
import { formatPrice } from '../utils/formatters';

export const CartPage: React.FC = () => {
  const { 
    items, summary, isLoading, appliedCoupon, 
    updateQuantity, removeItem, clearCart, applyCoupon, removeCoupon 
  } = useCart();
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();

  const [couponInput, setCouponInput] = useState<string>('');
  const [couponFeedback, setCouponFeedback] = useState<{ type: 'success' | 'error'; message: string } | null>(null);
  const [isApplyingCoupon, setIsApplyingCoupon] = useState<boolean>(false);

  const handleApplyCoupon = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!couponInput.trim()) return;

    setIsApplyingCoupon(true);
    setCouponFeedback(null);

    const res = await applyCoupon(couponInput.trim());
    if (res.success) {
      setCouponFeedback({ type: 'success', message: res.message });
      setCouponInput('');
    } else {
      setCouponFeedback({ type: 'error', message: res.message });
    }
    setIsApplyingCoupon(false);
  };

  if (!isAuthenticated) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-20">
        <div className="liquid-glass rounded-3xl p-12 text-center border border-white/70 dark:border-white/10 shadow-2xl">
          <EmptyState
            icon={ShoppingBag}
            title="Sign in to view your shopping bag"
            description="Your bag is waiting. Please sign in to review your saved pieces and complete your purchase."
            actionText="Sign In / Register"
            actionLink="/auth"
          />
        </div>
      </div>
    );
  }

  if (isLoading && items.length === 0) {
    return <LoadingSpinner fullPage message="Retrieving Shopping Bag..." />;
  }

  if (items.length === 0) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-20">
        <div className="liquid-glass rounded-3xl p-12 text-center border border-white/70 dark:border-white/10 shadow-2xl">
          <EmptyState
            icon={ShoppingBag}
            title="Your shopping bag is empty"
            description="You haven't added any garments to your bag yet. Explore our curated collections to find your signature look."
            actionText="Explore Collections"
            actionLink="/products"
          />
        </div>
      </div>
    );
  }

  const freeShippingProgress = Math.min(100, Math.round((summary.subtotal / summary.free_shipping_threshold) * 100));
  const remainingForFreeShipping = Math.max(0, summary.free_shipping_threshold - summary.subtotal);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12 space-y-8">
      
      {/* Header Banner */}
      <div className="liquid-glass rounded-3xl p-6 sm:p-8 border border-white/70 dark:border-white/10 shadow-xl flex items-center justify-between">
        <div>
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full liquid-pill text-[10px] uppercase tracking-[0.2em] text-aura-gold font-bold">
            <Sparkles size={12} /> Atelier Shopping Bag
          </span>
          <h1 className="text-2xl sm:text-4xl font-serif font-bold text-neutral-900 dark:text-neutral-100 mt-2">
            Your Selected Pieces ({summary.item_count})
          </h1>
        </div>
        <button
          onClick={clearCart}
          className="text-xs text-neutral-400 hover:text-rose-500 transition-colors font-medium underline"
        >
          Clear All Pieces
        </button>
      </div>

      {/* Free shipping progress notification - Liquid Glass Card */}
      <div className="liquid-glass p-5 rounded-2xl border border-white/70 dark:border-white/10 shadow-md">
        <div className="flex items-center justify-between text-xs font-semibold mb-2 text-neutral-800 dark:text-neutral-200">
          <span className="flex items-center gap-2">
            <Truck size={16} className="text-aura-gold" />
            {remainingForFreeShipping === 0 ? (
              <span className="text-emerald-600 dark:text-emerald-400 font-bold">You qualify for Complimentary Express Courier Delivery!</span>
            ) : (
              <span>Add <strong className="text-aura-gold font-mono">{formatPrice(remainingForFreeShipping)}</strong> more to receive Complimentary Shipping</span>
            )}
          </span>
          <span className="font-mono text-aura-gold font-bold">{freeShippingProgress}%</span>
        </div>
        <div className="w-full h-2 bg-neutral-200/50 dark:bg-neutral-800 rounded-full overflow-hidden p-0.5 border border-white/20">
          <div
            className="h-full bg-gradient-to-r from-aura-gold to-aura-goldLight rounded-full transition-all duration-700 shadow-sm"
            style={{ width: `${freeShippingProgress}%` }}
          />
        </div>
      </div>

      {/* Main Cart Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 sm:gap-10">
        
        {/* Items List - Liquid Glass Container */}
        <div className="lg:col-span-2 space-y-4">
          <div className="divide-y divide-neutral-200/50 dark:divide-neutral-800/60 liquid-glass rounded-3xl border border-white/70 dark:border-white/10 shadow-2xl overflow-hidden">
            {items.map((item) => (
              <div key={item.id} className="p-5 sm:p-6 flex flex-col sm:flex-row gap-5 items-start sm:items-center justify-between hover:bg-white/40 dark:hover:bg-white/5 transition-colors">
                
                {/* Item Thumbnail & Basic Info */}
                <div className="flex gap-4">
                  <Link to={`/products/${item.product_id}`} className="w-20 sm:w-24 aspect-[3/4] liquid-glass rounded-2xl overflow-hidden p-1 shrink-0 border border-white/80 dark:border-white/10 shadow-sm group">
                    <div className="w-full h-full rounded-xl overflow-hidden">
                      <ImageWithFallback
                        src={item.primary_image}
                        alt={item.product_name}
                        className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                      />
                    </div>
                  </Link>

                  <div className="space-y-1.5">
                    <Link to={`/products/${item.product_id}`} className="text-sm font-bold text-neutral-900 dark:text-neutral-100 hover:text-aura-gold transition-colors leading-snug">
                      {item.product_name}
                    </Link>
                    <div className="flex flex-wrap items-center gap-2 text-xs text-neutral-500 dark:text-neutral-400">
                      <span>Size: <strong className="text-neutral-800 dark:text-neutral-200">{item.size}</strong></span>
                      <span>•</span>
                      <span className="flex items-center gap-1.5">
                        Color: <strong className="text-neutral-800 dark:text-neutral-200">{item.color}</strong>
                        <span className="w-3 h-3 rounded-full inline-block border border-black/10 dark:border-white/20 shadow-inner" style={{ backgroundColor: item.color_hex }} />
                      </span>
                    </div>
                    <p className="text-[10px] text-neutral-400 font-mono">SKU: {item.sku}</p>
                    <div className="text-xs font-bold text-neutral-800 dark:text-neutral-200 pt-0.5 font-mono">
                      {formatPrice(item.unit_price)} each
                    </div>
                  </div>
                </div>

                {/* Quantity Controls & Line Total */}
                <div className="flex items-center justify-between w-full sm:w-auto gap-6 pt-3 sm:pt-0 border-t sm:border-t-0 border-neutral-200/40 dark:border-neutral-800/40">
                  <div className="flex items-center liquid-glass rounded-xl border border-white/60 dark:border-white/10 p-0.5 shadow-sm">
                    <button
                      onClick={() => updateQuantity(item.id, Math.max(1, item.quantity - 1))}
                      className="w-8 h-8 flex items-center justify-center text-xs font-bold hover:bg-white/60 dark:hover:bg-white/10 text-neutral-800 dark:text-neutral-200 rounded-lg transition-all"
                    >
                      -
                    </button>
                    <span className="w-9 text-center text-xs font-bold text-neutral-900 dark:text-neutral-100 font-mono">{item.quantity}</span>
                    <button
                      disabled={item.quantity >= item.stock_available}
                      onClick={() => updateQuantity(item.id, item.quantity + 1)}
                      className="w-8 h-8 flex items-center justify-center text-xs font-bold hover:bg-white/60 dark:hover:bg-white/10 text-neutral-800 dark:text-neutral-200 disabled:opacity-30 rounded-lg transition-all"
                    >
                      +
                    </button>
                  </div>

                  <div className="text-right min-w-20">
                    <span className="text-base font-bold text-neutral-900 dark:text-neutral-100 block font-mono">
                      {formatPrice(item.total_price)}
                    </span>
                    <button
                      onClick={() => removeItem(item.id)}
                      className="text-neutral-400 hover:text-rose-500 transition-colors mt-1 p-1 inline-block"
                      title="Remove item"
                    >
                      <Trash2 size={16} />
                    </button>
                  </div>
                </div>

              </div>
            ))}
          </div>

          <div className="flex items-center justify-between text-xs text-neutral-500 dark:text-neutral-400 px-2">
            <Link to="/products" className="hover:text-aura-gold font-bold flex items-center gap-1 transition-colors">
              ← Continue Curating Wardrobe
            </Link>
            <span>Items reserved during active session</span>
          </div>
        </div>

        {/* Order Summary & Coupon Card - Sticky Liquid Glass */}
        <div className="space-y-6">
          <div className="liquid-glass rounded-3xl p-7 sm:p-8 border border-white/80 dark:border-white/10 shadow-2xl space-y-6 sticky top-28">
            <h3 className="font-serif font-bold text-xl text-neutral-900 dark:text-neutral-100 pb-3 border-b border-neutral-200/50 dark:border-neutral-800/60">
              Order Summary
            </h3>

            {/* Subtotal breakdown */}
            <div className="space-y-3 text-xs text-neutral-600 dark:text-neutral-300">
              <div className="flex justify-between">
                <span>Subtotal ({summary.item_count} garments)</span>
                <span className="font-bold text-neutral-900 dark:text-neutral-100 font-mono">{formatPrice(summary.subtotal)}</span>
              </div>

              {appliedCoupon && (
                <div className="flex justify-between text-emerald-600 dark:text-emerald-400 font-semibold">
                  <span className="flex items-center gap-1.5">
                    Invitation ({appliedCoupon.code})
                    <button onClick={removeCoupon} className="text-neutral-400 hover:text-rose-500">
                      <X size={13} />
                    </button>
                  </span>
                  <span className="font-mono">-{formatPrice(appliedCoupon.discount_amount)}</span>
                </div>
              )}

              <div className="flex justify-between">
                <span>Estimated GST (12%)</span>
                <span className="font-mono">{formatPrice(summary.tax)}</span>
              </div>

              <div className="flex justify-between">
                <span>Express Courier</span>
                <span>
                  {summary.shipping === 0 ? (
                    <strong className="text-emerald-600 dark:text-emerald-400 uppercase">COMPLIMENTARY</strong>
                  ) : (
                    <span className="font-mono">{formatPrice(summary.shipping)}</span>
                  )}
                </span>
              </div>
            </div>

            <div className="pt-4 border-t border-neutral-200/50 dark:border-neutral-800/60 flex justify-between items-baseline">
              <div>
                <span className="text-sm font-bold text-neutral-900 dark:text-neutral-100">Estimated Total</span>
                <span className="text-[10px] text-neutral-400 block">INR includes all duties & GST</span>
              </div>
              <span className="text-2xl font-serif font-bold text-neutral-900 dark:text-neutral-100 font-mono">
                {formatPrice(summary.total)}
              </span>
            </div>

            {/* Coupon Code Input */}
            <div className="pt-4 border-t border-neutral-200/50 dark:border-neutral-800/60">
              <span className="text-[11px] uppercase tracking-wider font-bold text-neutral-700 dark:text-neutral-300 block mb-2.5">
                Promotional Voucher
              </span>

              {appliedCoupon ? (
                <div className="p-3 bg-emerald-500/15 border border-emerald-500/30 text-emerald-700 dark:text-emerald-300 text-xs rounded-2xl flex items-center justify-between font-semibold">
                  <span className="flex items-center gap-1.5">
                    <Tag size={13} /> Voucher '{appliedCoupon.code}' Applied
                  </span>
                  <button onClick={removeCoupon} className="text-xs text-rose-500 hover:underline font-bold">
                    Remove
                  </button>
                </div>
              ) : (
                <form onSubmit={handleApplyCoupon} className="space-y-2.5">
                  <div className="flex gap-2">
                    <input
                      type="text"
                      placeholder="e.g. WELCOME15"
                      value={couponInput}
                      onChange={(e) => setCouponInput(e.target.value)}
                      className="flex-1 px-3.5 py-2.5 liquid-input text-neutral-900 dark:text-white rounded-xl text-xs uppercase font-mono font-bold"
                    />
                    <button
                      type="submit"
                      disabled={isApplyingCoupon || !couponInput.trim()}
                      className="px-4 py-2.5 liquid-btn-gold text-neutral-950 text-xs uppercase font-bold tracking-wider rounded-xl disabled:opacity-40 transition-all shadow-md"
                    >
                      {isApplyingCoupon ? '...' : 'Apply'}
                    </button>
                  </div>

                  {couponFeedback && (
                    <div className={`p-2.5 text-xs rounded-xl flex items-center gap-1.5 font-medium ${
                      couponFeedback.type === 'success' 
                        ? 'bg-emerald-500/15 text-emerald-700 dark:text-emerald-300 border border-emerald-500/30' 
                        : 'bg-rose-500/15 text-rose-700 dark:text-rose-300 border border-rose-500/30'
                    }`}>
                      {couponFeedback.type === 'success' ? <Check size={14} /> : <AlertCircle size={14} />}
                      <span>{couponFeedback.message}</span>
                    </div>
                  )}

                  <div className="text-[10px] text-neutral-400">
                    Active codes: <strong className="text-aura-gold">WELCOME15</strong> (15% off) or <strong className="text-aura-gold">LUXE20</strong> (20% off)
                  </div>
                </form>
              )}
            </div>

            {/* Checkout CTA */}
            <button
              onClick={() => navigate('/checkout')}
              className="w-full py-4 liquid-btn-gold text-neutral-950 text-xs uppercase tracking-widest font-bold rounded-2xl shadow-xl transition-all flex items-center justify-center gap-2 group"
            >
              <span>Proceed to Checkout</span>
              <ArrowRight size={15} className="group-hover:translate-x-1 transition-transform" />
            </button>

            <div className="flex items-center justify-center gap-2 text-[11px] text-neutral-400 pt-1">
              <ShieldCheck size={14} className="text-aura-gold" />
              <span>Encrypted 256-bit Secure Checkout</span>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
};
