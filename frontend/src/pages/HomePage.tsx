import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { 
  ArrowRight, Sparkles, Tag, Check, ChevronRight, 
  ShieldCheck, Truck, RotateCcw, Award, Gem, Flame 
} from 'lucide-react';
import { api } from '../services/api';
import { Product, Category } from '../types';
import { ProductCard } from '../components/common/ProductCard';
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import { ImageWithFallback } from '../components/common/ImageWithFallback';
import { 
  FALLBACK_CATEGORIES, 
  FALLBACK_FEATURED, 
  FALLBACK_TRENDING 
} from '../data/fallbackData';

export const HomePage: React.FC = () => {
  // Pre-load with curated luxury apparel so page renders instantly with zero wait
  const [featuredProducts, setFeaturedProducts] = useState<Product[]>(FALLBACK_FEATURED);
  const [trendingProducts, setTrendingProducts] = useState<Product[]>(FALLBACK_TRENDING);
  const [categories, setCategories] = useState<Category[]>(FALLBACK_CATEGORIES);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [copiedCoupon, setCopiedCoupon] = useState<boolean>(false);

  // Silently revalidate data from live backend when connected
  const loadHomeData = async () => {
    try {
      const [catRes, prodRes, trendRes] = await Promise.allSettled([
        api.getCategories(),
        api.getProducts('featured=true&per_page=8'),
        api.getTrendingProducts()
      ]);

      if (catRes.status === 'fulfilled' && catRes.value?.categories?.length) {
        setCategories(catRes.value.categories);
      }
      if (prodRes.status === 'fulfilled' && prodRes.value?.products?.length) {
        setFeaturedProducts(prodRes.value.products);
      }
      if (trendRes.status === 'fulfilled' && trendRes.value?.trending?.length) {
        setTrendingProducts(trendRes.value.trending.slice(0, 8));
      }
    } catch (err) {
      console.warn("Using curated luxury cache while syncing with backend:", err);
    }
  };

  useEffect(() => {
    loadHomeData();
  }, []);

  const handleCopyCoupon = (code: string) => {
    navigator.clipboard.writeText(code);
    setCopiedCoupon(true);
    setTimeout(() => setCopiedCoupon(false), 2500);
  };

  return (
    <div className="space-y-16 lg:space-y-28 pb-16">
      
      {/* 1. Hero Haute Lookbook - Liquid Glass Stage */}
      <section className="relative min-h-[85vh] flex items-center overflow-hidden">
        {/* Background Editorial Visual */}
        <div className="absolute inset-0 z-0">
          <img
            src="https://images.unsplash.com/photo-1490481651871-ab68de25d43d?auto=format&fit=crop&w=2400&q=90"
            alt="Aura Apparel Editorial"
            className="w-full h-full object-cover object-center scale-105 transition-transform duration-1000 ease-out"
          />
          {/* Liquid Shading Overlay */}
          <div className="absolute inset-0 bg-gradient-to-r from-neutral-950/90 via-neutral-950/60 to-transparent dark:from-black/95 dark:via-neutral-950/70 dark:to-transparent" />
          <div className="absolute inset-0 bg-gradient-to-t from-[#faf9f6] dark:from-[#0c0a09] via-transparent to-transparent h-40 bottom-0 top-auto" />
        </div>

        {/* Floating Liquid Glass Hero Panel */}
        <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 w-full">
          <div className="max-w-2xl liquid-glass rounded-3xl p-8 sm:p-12 shadow-2xl border border-white/60 dark:border-white/10 space-y-6">
            
            {/* Liquid Capsule Pill */}
            <div className="inline-flex items-center gap-2 px-3.5 py-1.5 liquid-pill text-[10px] font-semibold tracking-[0.25em] uppercase text-aura-gold dark:text-aura-goldLight">
              <Sparkles size={12} className="text-aura-gold animate-pulse" />
              <span>COLLECTION PRINTEMPS / ÉTÉ 2026</span>
            </div>

            {/* Editorial Headline */}
            <h1 className="text-4xl sm:text-6xl lg:text-7xl font-serif font-light tracking-tight leading-[1.06] text-neutral-950 dark:text-white">
              The Architecture <br />
              <span className="italic font-light text-aura-gold">of Modern Dress.</span>
            </h1>

            {/* Narrative Subtitle */}
            <p className="text-sm sm:text-base text-neutral-600 dark:text-neutral-300 font-light leading-relaxed max-w-xl">
              Certified Grade 6A mulberry silk, unspun Mongolian cashmere, and artisanal Japanese twill. Sculpted wardrobe foundations designed to outlast transient fashion.
            </p>

            {/* Liquid Action CTAs */}
            <div className="flex flex-wrap gap-4 pt-3">
              <Link
                to="/products"
                className="px-8 py-3.5 liquid-btn-gold rounded-full text-neutral-950 text-xs font-semibold uppercase tracking-[0.15em] flex items-center gap-2 shadow-xl group"
              >
                <span>Explore Atelier</span>
                <ArrowRight size={14} className="group-hover:translate-x-1 transition-transform" />
              </Link>
              <Link
                to="/products?category=womens-dresses"
                className="px-8 py-3.5 liquid-btn-glass rounded-full text-xs font-semibold uppercase tracking-[0.15em] text-neutral-900 dark:text-white shadow-lg"
              >
                Mulberry Silk Dresses
              </Link>
            </div>

            {/* Micro Highlights Pill Row */}
            <div className="pt-6 border-t border-neutral-200/50 dark:border-neutral-800/60 grid grid-cols-3 gap-4 text-center">
              <div>
                <p className="text-[10px] uppercase tracking-[0.2em] text-neutral-400 font-semibold">Origin</p>
                <p className="text-sm font-serif font-normal text-neutral-800 dark:text-neutral-200 mt-0.5">Heritage Mills</p>
              </div>
              <div>
                <p className="text-[10px] uppercase tracking-[0.2em] text-neutral-400 font-semibold">Fibers</p>
                <p className="text-sm font-serif font-normal text-neutral-800 dark:text-neutral-200 mt-0.5">100% Organic</p>
              </div>
              <div>
                <p className="text-[10px] uppercase tracking-[0.2em] text-neutral-400 font-semibold">Shipping</p>
                <p className="text-sm font-serif font-normal text-aura-gold mt-0.5">Complimentary</p>
              </div>
            </div>

          </div>
        </div>
      </section>

      {/* 2. Shop By Category - Liquid Glass Tiles */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col md:flex-row md:items-end justify-between mb-8 pb-3 border-b border-neutral-200/60 dark:border-neutral-800/60">
          <div>
            <span className="text-[10px] uppercase tracking-[0.25em] text-aura-gold font-semibold flex items-center gap-1.5">
              <Gem size={12} /> Curated Collections
            </span>
            <h2 className="text-2xl sm:text-4xl font-serif font-normal text-neutral-900 dark:text-neutral-100 mt-1">
              Pillars of the Wardrobe
            </h2>
          </div>
          <Link
            to="/products"
            className="text-[11px] uppercase tracking-[0.2em] font-semibold text-neutral-700 dark:text-neutral-300 hover:text-aura-gold dark:hover:text-aura-gold flex items-center gap-1 mt-2 md:mt-0 transition-colors"
          >
            <span>View All Categories</span>
            <ChevronRight size={14} />
          </Link>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-8 gap-3 sm:gap-4">
          {categories.slice(0, 8).map((cat, idx) => (
            <Link
              key={cat.id}
              to={`/products?category=${cat.slug}`}
              className="group relative aspect-[3/4] rounded-2xl overflow-hidden liquid-glass-card flex flex-col justify-end p-4 shadow-md border border-white/85 dark:border-white/10"
            >
              <ImageWithFallback
                src={cat.image_url}
                alt={cat.name}
                categoryName={cat.name}
                className="absolute inset-0 w-full h-full object-cover object-center group-hover:scale-110 transition-transform duration-700 ease-out"
              />
              {/* Refractive Gradient Mask */}
              <div className="absolute inset-0 bg-gradient-to-t from-neutral-950/90 via-neutral-950/30 to-transparent" />
              
              <div className="relative z-10 text-white">
                <div className="flex items-center justify-between mb-1.5">
                  <span className="liquid-pill text-[9px] uppercase tracking-widest font-semibold px-2 py-0.5 inline-block text-aura-goldLight">
                    {cat.product_count ? `${cat.product_count} Pieces` : 'Explore'}
                  </span>
                  <span className="text-[9px] font-mono text-neutral-400 font-medium">0{idx + 1}</span>
                </div>
                <h3 className="font-serif text-sm sm:text-base font-normal tracking-wide leading-tight group-hover:text-aura-gold transition-colors">
                  {cat.name}
                </h3>
              </div>
            </Link>
          ))}
        </div>
      </section>

      {/* 3. Exclusive Promotional Invitation - Liquid Glass Voucher */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="relative overflow-hidden liquid-glass rounded-3xl p-8 sm:p-12 shadow-2xl border border-white/60 dark:border-white/10">
          
          {/* Ambient Inner Glowing Glow */}
          <div className="absolute -top-20 -right-20 w-80 h-80 rounded-full bg-aura-gold/20 blur-[80px] pointer-events-none" />
          <div className="absolute -bottom-20 -left-20 w-80 h-80 rounded-full bg-indigo-500/10 blur-[80px] pointer-events-none" />

          <div className="relative z-10 flex flex-col lg:flex-row items-center justify-between gap-8">
            <div className="space-y-3 text-center lg:text-left">
              <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full liquid-pill text-aura-gold dark:text-aura-goldLight text-[11px] uppercase tracking-widest font-bold">
                <Tag size={13} /> Exclusive Patron Invitation
              </span>
              <h3 className="text-2xl sm:text-4xl font-serif font-bold text-neutral-900 dark:text-white">
                Receive 15% Off Your Inaugural Atelier Order
              </h3>
              <p className="text-xs sm:text-sm text-neutral-600 dark:text-neutral-300 max-w-xl font-normal leading-relaxed">
                Experience high-caliber natural fabrics with complimentary express courier delivery applied to all orders exceeding ₹2,499.
              </p>
            </div>

            <div className="flex items-center gap-3 liquid-glass p-2.5 sm:p-3 rounded-2xl border border-white/80 dark:border-white/15 shadow-lg">
              <div className="flex flex-col px-3">
                <span className="text-[10px] uppercase tracking-wider text-neutral-400 font-bold">Voucher Code</span>
                <span className="text-lg font-mono font-bold tracking-widest text-aura-gold">WELCOME15</span>
              </div>
              <button
                onClick={() => handleCopyCoupon('WELCOME15')}
                className="px-5 py-2.5 liquid-btn-gold text-neutral-950 text-xs uppercase font-bold tracking-wider rounded-xl transition-all flex items-center gap-1.5 shadow-md"
              >
                {copiedCoupon ? (
                  <>
                    <Check size={14} />
                    <span>Copied!</span>
                  </>
                ) : (
                  <span>Copy Code</span>
                )}
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* 4. Signature Featured Arrivals */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col md:flex-row md:items-end justify-between mb-8 pb-3 border-b border-neutral-200/60 dark:border-neutral-800/60">
          <div>
            <span className="text-[10px] uppercase tracking-[0.25em] text-aura-gold font-bold flex items-center gap-1.5">
              <Sparkles size={12} /> Seasonal Focus
            </span>
            <h2 className="text-2xl sm:text-3xl font-serif font-bold text-neutral-900 dark:text-neutral-100 mt-1">
              Featured Arrivals
            </h2>
          </div>
          <Link
            to="/products?featured=true"
            className="text-xs uppercase tracking-widest font-bold text-neutral-700 dark:text-neutral-300 hover:text-aura-gold dark:hover:text-aura-gold flex items-center gap-1 mt-2 md:mt-0 transition-colors"
          >
            <span>View All Featured</span>
            <ChevronRight size={14} />
          </Link>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 sm:gap-6">
          {featuredProducts.slice(0, 8).map((product) => (
            <ProductCard key={product.id} product={product} />
          ))}
        </div>
      </section>

      {/* 5. Editorial / Brand Craftsmanship Story - Liquid Glass Panel */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="liquid-glass rounded-3xl p-8 sm:p-14 border border-white/70 dark:border-white/10 shadow-2xl">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            
            <div className="aspect-[4/3] rounded-2xl overflow-hidden shadow-2xl relative group">
              <img
                src="https://images.unsplash.com/photo-1558769132-cb1aea458c5e?auto=format&fit=crop&w=1400&q=85"
                alt="Aura Tailoring Workshop"
                className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-black/50 via-transparent to-transparent" />
              <div className="absolute bottom-4 left-4 right-4 liquid-glass p-3.5 rounded-xl border border-white/50 dark:border-white/10 text-xs font-medium text-neutral-900 dark:text-neutral-100 shadow-lg">
                &ldquo;True elegance lies in the purity of the fiber and the mastery of the stitch.&rdquo;
              </div>
            </div>

            <div className="space-y-6">
              <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full liquid-pill text-aura-gold text-xs uppercase tracking-[0.2em] font-bold">
                <Award size={13} /> The Aura Ethos
              </span>
              <h2 className="text-3xl sm:text-5xl font-serif font-bold text-neutral-900 dark:text-neutral-100 leading-tight">
                Pure Natural Fibers.<br />
                <span className="italic text-aura-gold font-light">Artisanal Integrity.</span>
              </h2>
              <p className="text-sm text-neutral-600 dark:text-neutral-300 leading-relaxed font-normal">
                Every garment begins with uncompromised fiber sourcing: certified Grade 6A mulberry silk from heritage mills, Mongolian cashmere collected during natural spring molting, and Normandy flax linen pre-washed with river stones for butter-soft drape.
              </p>
              
              <div className="grid grid-cols-3 gap-4 pt-4 border-t border-neutral-200/50 dark:border-neutral-800/60">
                <div className="liquid-glass p-3.5 rounded-2xl text-center">
                  <h4 className="text-2xl sm:text-3xl font-serif font-bold text-aura-gold">100%</h4>
                  <p className="text-[10px] text-neutral-500 dark:text-neutral-400 uppercase tracking-wider mt-1 font-bold">Natural Fibers</p>
                </div>
                <div className="liquid-glass p-3.5 rounded-2xl text-center">
                  <h4 className="text-2xl sm:text-3xl font-serif font-bold text-aura-gold">Zero</h4>
                  <p className="text-[10px] text-neutral-500 dark:text-neutral-400 uppercase tracking-wider mt-1 font-bold">Harmful Dyes</p>
                </div>
                <div className="liquid-glass p-3.5 rounded-2xl text-center">
                  <h4 className="text-2xl sm:text-3xl font-serif font-bold text-aura-gold">Lifetime</h4>
                  <p className="text-[10px] text-neutral-500 dark:text-neutral-400 uppercase tracking-wider mt-1 font-bold">Repair Promise</p>
                </div>
              </div>
            </div>

          </div>
        </div>
      </section>

      {/* 6. Trending & Top Rated Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col md:flex-row md:items-end justify-between mb-8 pb-3 border-b border-neutral-200/60 dark:border-neutral-800/60">
          <div>
            <span className="text-[10px] uppercase tracking-[0.25em] text-aura-gold font-bold flex items-center gap-1.5">
              <Flame size={12} className="text-rose-500" /> Patron Favorites
            </span>
            <h2 className="text-2xl sm:text-3xl font-serif font-bold text-neutral-900 dark:text-neutral-100 mt-1">
              Most Loved Pieces
            </h2>
          </div>
          <Link
            to="/products?sort=popular"
            className="text-xs uppercase tracking-widest font-bold text-neutral-700 dark:text-neutral-300 hover:text-aura-gold dark:hover:text-aura-gold flex items-center gap-1 mt-2 md:mt-0 transition-colors"
          >
            <span>Explore Trending</span>
            <ChevronRight size={14} />
          </Link>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 sm:gap-6">
          {trendingProducts.map((product) => (
            <ProductCard key={product.id} product={product} />
          ))}
        </div>
      </section>

      {/* 7. Guarantees & Heritage Pillars - Liquid Glass Row */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          
          <div className="liquid-glass p-6 rounded-2xl border border-white/70 dark:border-white/10 flex items-center gap-4 shadow-sm hover:shadow-md transition-shadow">
            <div className="w-12 h-12 rounded-full liquid-pill flex items-center justify-center text-aura-gold shrink-0">
              <Truck size={22} />
            </div>
            <div>
              <h4 className="text-xs uppercase tracking-wider font-bold text-neutral-900 dark:text-neutral-100">Complimentary Courier</h4>
              <p className="text-xs text-neutral-500 dark:text-neutral-400 mt-0.5">Orders exceeding ₹2,499</p>
            </div>
          </div>

          <div className="liquid-glass p-6 rounded-2xl border border-white/70 dark:border-white/10 flex items-center gap-4 shadow-sm hover:shadow-md transition-shadow">
            <div className="w-12 h-12 rounded-full liquid-pill flex items-center justify-center text-aura-gold shrink-0">
              <RotateCcw size={22} />
            </div>
            <div>
              <h4 className="text-xs uppercase tracking-wider font-bold text-neutral-900 dark:text-neutral-100">30-Day Effortless Returns</h4>
              <p className="text-xs text-neutral-500 dark:text-neutral-400 mt-0.5">Complimentary return labels</p>
            </div>
          </div>

          <div className="liquid-glass p-6 rounded-2xl border border-white/70 dark:border-white/10 flex items-center gap-4 shadow-sm hover:shadow-md transition-shadow">
            <div className="w-12 h-12 rounded-full liquid-pill flex items-center justify-center text-aura-gold shrink-0">
              <Award size={22} />
            </div>
            <div>
              <h4 className="text-xs uppercase tracking-wider font-bold text-neutral-900 dark:text-neutral-100">Heritage Craftsmanship</h4>
              <p className="text-xs text-neutral-500 dark:text-neutral-400 mt-0.5">Mulberry silk, cashmere & flax</p>
            </div>
          </div>

          <div className="liquid-glass p-6 rounded-2xl border border-white/70 dark:border-white/10 flex items-center gap-4 shadow-sm hover:shadow-md transition-shadow">
            <div className="w-12 h-12 rounded-full liquid-pill flex items-center justify-center text-aura-gold shrink-0">
              <ShieldCheck size={22} />
            </div>
            <div>
              <h4 className="text-xs uppercase tracking-wider font-bold text-neutral-900 dark:text-neutral-100">Encrypted Checkout</h4>
              <p className="text-xs text-neutral-500 dark:text-neutral-400 mt-0.5">256-bit bank grade security</p>
            </div>
          </div>

        </div>
      </section>

    </div>
  );
};
