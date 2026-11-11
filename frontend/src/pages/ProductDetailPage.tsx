import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { 
  Heart, ShoppingBag, ShieldCheck, Truck, RefreshCw, 
  ChevronRight, Star, AlertCircle, CheckCircle2, Info, Sparkles, Check, Gem 
} from 'lucide-react';
import { api } from '../services/api';
import { Product, ProductVariant, RecommendationResult } from '../types';
import { ReviewStars } from '../components/common/ReviewStars';
import { ProductCard } from '../components/common/ProductCard';
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import { ImageWithFallback } from '../components/common/ImageWithFallback';
import { formatPrice } from '../utils/formatters';
import { useCart } from '../context/CartContext';
import { useWishlist } from '../context/WishlistContext';
import { useAuth } from '../context/AuthContext';

export const ProductDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const { addToCart } = useCart();
  const { isInWishlist, toggleWishlist } = useWishlist();
  const { isAuthenticated } = useAuth();

  const [product, setProduct] = useState<Product | null>(null);
  const [recommendations, setRecommendations] = useState<RecommendationResult[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  // Selection states
  const [selectedImage, setSelectedImage] = useState<string>('');
  const [selectedSize, setSelectedSize] = useState<string>('');
  const [selectedColor, setSelectedColor] = useState<string>('');
  const [quantity, setQuantity] = useState<number>(1);
  const [activeTab, setActiveTab] = useState<'details' | 'materials' | 'shipping'>('details');

  // Review Form states
  const [reviewRating, setReviewRating] = useState<number>(5);
  const [reviewTitle, setReviewTitle] = useState<string>('');
  const [reviewComment, setReviewComment] = useState<string>('');
  const [reviewSubmitting, setReviewSubmitting] = useState<boolean>(false);
  const [reviewSuccessMsg, setReviewSuccessMsg] = useState<string>('');

  // Fabric & Drape AI Advisor state
  const [fabricQuestion, setFabricQuestion] = useState<string>('');
  const [fabricAnswer, setFabricAnswer] = useState<string>('');
  const [isAskingFabric, setIsAskingFabric] = useState<boolean>(false);

  const handleAskFabric = async (q: string) => {
    if (!product || !q.trim()) return;
    setIsAskingFabric(true);
    setFabricQuestion(q);
    try {
      const res = await api.askFabricAdvisor(product.id, q);
      setFabricAnswer(res.answer || '');
    } catch (e: any) {
      setFabricAnswer(e.message || 'The Fabric Advisor is momentarily indisposed.');
    } finally {
      setIsAskingFabric(false);
    }
  };
  const [reviewErrorMsg, setReviewErrorMsg] = useState<string>('');

  // Cart feedback
  const [cartSuccessMsg, setCartSuccessMsg] = useState<string>('');
  const [cartErrorMsg, setCartErrorMsg] = useState<string>('');

  // Fetch product and recommendations
  useEffect(() => {
    const fetchProductData = async () => {
      if (!id) return;
      setIsLoading(true);
      try {
        const res = await api.getProduct(id);
        const prod: Product = res.product;
        setProduct(prod);

        // Preselect first available variant and its matching color image
        let initialImage = prod.primary_image;
        if (prod.variants && prod.variants.length > 0) {
          const firstInStock = prod.variants.find(v => v.stock_quantity > 0) || prod.variants[0];
          setSelectedSize(firstInStock.size);
          setSelectedColor(firstInStock.color);

          if (prod.images && prod.images.length > 0) {
            const matchedImg = prod.images.find(img => img.color && img.color.toLowerCase() === firstInStock.color.toLowerCase());
            if (matchedImg) {
              initialImage = matchedImg.image_url;
            }
          }
        }
        setSelectedImage(initialImage);

        // Fetch algorithmic recommendations
        try {
          const recRes = await api.getProductRecommendations(prod.id);
          setRecommendations(recRes.recommendations || []);
        } catch (recErr) {
          console.warn("Could not load recommendations:", recErr);
        }

      } catch (err) {
        console.error("Failed to load product details:", err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchProductData();
  }, [id]);

  const handleColorChange = (c: any, colorIdx: number) => {
    const colorName = typeof c === 'string' ? c : c.color;
    setSelectedColor(colorName);

    // Switch hero image to corresponding color image
    if (typeof c === 'object' && c.image_url) {
      setSelectedImage(c.image_url);
    } else if (product?.images && product.images.length > 0) {
      const match = product.images.find(img => img.color && img.color.toLowerCase() === colorName.toLowerCase());
      if (match) {
        setSelectedImage(match.image_url);
      } else if (product.images[colorIdx]) {
        setSelectedImage(product.images[colorIdx].image_url);
      }
    }
  };

  const handleThumbnailClick = (imgUrl: string, _idx: number) => {
    setSelectedImage(imgUrl);
    if (product?.images) {
      const clicked = product.images.find(img => img.image_url === imgUrl);
      if (clicked && clicked.color) {
        setSelectedColor(clicked.color);
      }
    }
  };

  const handleAddToCart = async () => {
    if (!product) return;
    setCartSuccessMsg('');
    setCartErrorMsg('');

    if (!selectedSize || !selectedColor) {
      setCartErrorMsg("Please choose both your size and color preference.");
      return;
    }

    const matchedVariant = product.variants?.find(
      v => v.size === selectedSize && v.color === selectedColor
    );

    if (!matchedVariant) {
      setCartErrorMsg("This combination is currently not available in our atelier.");
      return;
    }

    if (matchedVariant.stock_quantity < quantity) {
      setCartErrorMsg(`Only ${matchedVariant.stock_quantity} units available.`);
      return;
    }

    try {
      await addToCart(matchedVariant.id, quantity);
      setCartSuccessMsg(`Added ${quantity} piece${quantity > 1 ? 's' : ''} to your shopping bag.`);
      setTimeout(() => setCartSuccessMsg(''), 4000);
    } catch (err: any) {
      setCartErrorMsg(err.message || "Failed to add piece to shopping bag.");
    }
  };

  const handleReviewSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!product) return;

    if (!isAuthenticated) {
      setReviewErrorMsg("Please sign in to publish an authentic review.");
      return;
    }

    setReviewSubmitting(true);
    setReviewSuccessMsg('');
    setReviewErrorMsg('');

    try {
      const res = await api.addProductReview(product.id, {
        rating: reviewRating,
        title: reviewTitle,
        comment: reviewComment
      });

      setReviewSuccessMsg("Thank you for your review! It is now published.");
      setReviewTitle('');
      setReviewComment('');
      setReviewRating(5);

      if (res.product) {
        setProduct(res.product);
      }
    } catch (err: any) {
      setReviewErrorMsg(err.message || "Could not publish your review.");
    } finally {
      setReviewSubmitting(false);
    }
  };

  if (isLoading) {
    return <LoadingSpinner fullPage message="Presenting Garment Details..." />;
  }

  if (!product) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-20 text-center">
        <h2 className="text-2xl font-serif font-bold text-neutral-900 dark:text-neutral-100">Piece Not Found</h2>
        <p className="text-xs text-neutral-500 mt-2">The apparel item you requested is no longer in the active catalogue.</p>
        <Link to="/products" className="mt-6 inline-block px-6 py-2.5 liquid-btn-gold text-neutral-950 text-xs font-bold uppercase rounded-full">
          Browse Collections
        </Link>
      </div>
    );
  }

  const wishlisted = isInWishlist(product.id);
  const hasDiscount = product.discount_price && product.discount_price > 0 && product.discount_price < product.base_price;
  const effectivePrice = hasDiscount ? product.discount_price! : product.base_price;

  const currentVariant: ProductVariant | undefined = product.variants?.find(
    v => v.size === selectedSize && v.color === selectedColor
  );

  const effectiveStock = currentVariant ? currentVariant.stock_quantity : product.total_stock;
  const isOutOfStock = effectiveStock <= 0;
  const isLowStock = effectiveStock > 0 && effectiveStock <= 5;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12 space-y-16">
      
      {/* Breadcrumb Path */}
      <nav className="flex items-center space-x-2 text-xs font-medium text-neutral-400">
        <Link to="/" className="hover:text-aura-gold transition-colors">Atelier</Link>
        <ChevronRight size={12} />
        <Link to="/products" className="hover:text-aura-gold transition-colors">Catalogue</Link>
        <ChevronRight size={12} />
        <Link to={`/products?category=${product.category_slug}`} className="hover:text-aura-gold transition-colors">
          {product.category_name}
        </Link>
        <ChevronRight size={12} />
        <span className="text-neutral-700 dark:text-neutral-300 truncate max-w-xs">{product.name}</span>
      </nav>

      {/* Main Showcase Stage */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-10 xl:gap-14 items-start">
        
        {/* Left Column: Liquid Glass Gallery */}
        <div className="space-y-4">
          <div className="relative aspect-[3/4] liquid-glass rounded-3xl overflow-hidden p-3 border border-white/80 dark:border-white/10 shadow-2xl">
            <div className="w-full h-full rounded-2xl overflow-hidden relative">
              <ImageWithFallback
                src={selectedImage}
                alt={product.name}
                categoryName={product.category_name}
                className="w-full h-full object-cover object-center transition-all duration-700 ease-out"
              />
              
              {/* Badges Overlay */}
              <div className="absolute top-4 left-4 flex flex-col gap-2 z-10">
                {hasDiscount && (
                  <span className="bg-rose-500/90 backdrop-blur-md text-white text-[11px] font-bold uppercase tracking-wider px-3 py-1 rounded-full shadow-lg border border-white/30 animate-pulse">
                    Sale
                  </span>
                )}
                {product.is_featured && !hasDiscount && (
                  <span className="liquid-pill text-aura-gold dark:text-aura-goldLight text-[11px] font-bold uppercase tracking-wider px-3 py-1 shadow-md">
                    Featured
                  </span>
                )}
              </div>

              {/* Wishlist Button */}
              <button
                onClick={() => toggleWishlist(product.id)}
                className="absolute top-4 right-4 z-10 w-11 h-11 rounded-full liquid-pill flex items-center justify-center text-neutral-700 dark:text-neutral-300 hover:text-rose-500 dark:hover:text-rose-400 hover:scale-110 active:scale-95 shadow-lg transition-all"
                aria-label="Wishlist"
              >
                <Heart size={20} className={wishlisted ? 'fill-rose-500 text-rose-500' : ''} />
              </button>
            </div>
          </div>

          {/* Thumbnail list - Liquid Glass Tiles */}
          {product.images && product.images.length > 1 && (
            <div className="flex gap-3 overflow-x-auto pb-2 pt-1">
              {product.images.map((img, imgIdx) => (
                <button
                  key={img.id}
                  onClick={() => handleThumbnailClick(img.image_url, imgIdx)}
                  className={`w-20 aspect-[3/4] rounded-2xl overflow-hidden p-1 transition-all shrink-0 ${
                    selectedImage === img.image_url 
                      ? 'liquid-glass border-aura-gold ring-2 ring-aura-gold/50 shadow-md scale-105' 
                      : 'liquid-glass opacity-70 hover:opacity-100'
                  }`}
                >
                  <div className="w-full h-full rounded-xl overflow-hidden">
                    <ImageWithFallback src={img.image_url} alt="thumbnail" className="w-full h-full object-cover" />
                  </div>
                </button>
              ))}
            </div>
          )}
        </div>

        {/* Right Column: Liquid Glass Purchasing Console */}
        <div className="liquid-glass rounded-3xl p-7 sm:p-10 border border-white/80 dark:border-white/10 shadow-2xl flex flex-col space-y-6">
          <div>
            <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full liquid-pill text-aura-gold text-[10px] uppercase tracking-[0.25em] font-semibold">
              <Gem size={12} /> {product.brand} &bull; {product.category_name}
            </div>
            <h1 className="text-3xl sm:text-5xl font-serif font-normal tracking-tight text-neutral-950 dark:text-white mt-2 leading-[1.12]">
              {product.name}
            </h1>

            {/* Ratings & Purchases */}
            <div className="flex items-center gap-3 mt-3">
              <ReviewStars rating={product.average_rating} size={14} showScore reviewCount={product.review_count} />
              <span className="text-neutral-300 dark:text-neutral-700">•</span>
              <span className="text-xs text-neutral-500 dark:text-neutral-400 font-medium">{product.sales_count} Patrons Acquired</span>
            </div>

            {/* Pricing Section */}
            <div className="flex items-baseline gap-3 mt-4 pt-3 border-t border-neutral-200/50 dark:border-neutral-800/60">
              <span className="text-3xl sm:text-4xl font-normal font-serif text-neutral-950 dark:text-white">
                {formatPrice(effectivePrice)}
              </span>
              {hasDiscount && (
                <span className="text-lg text-neutral-400 dark:text-neutral-500 line-through font-serif">
                  {formatPrice(product.base_price)}
                </span>
              )}
              {hasDiscount && (
                <span className="text-xs font-bold text-emerald-600 dark:text-emerald-400 bg-emerald-500/10 px-2.5 py-1 rounded-full border border-emerald-500/20">
                  Save {formatPrice(product.base_price - product.discount_price!)}
                </span>
              )}
            </div>
          </div>

          <p className="text-sm text-neutral-600 dark:text-neutral-300 leading-relaxed font-normal">
            {product.description}
          </p>

          <hr className="border-neutral-200/50 dark:border-neutral-800/60" />

          {/* Color Selector */}
          <div>
            <div className="flex items-center justify-between mb-3 text-xs">
              <span className="uppercase tracking-wider font-bold text-neutral-900 dark:text-neutral-100">
                Palette: <span className="text-aura-gold">{selectedColor}</span>
              </span>
            </div>
            <div className="flex items-center gap-3">
              {product.available_colors?.map((c: any, colorIdx: number) => {
                const colorName = typeof c === 'string' ? c : c.color;
                const colorHex = typeof c === 'string' ? '#000' : c.color_hex;
                const isSelected = selectedColor === colorName;
                const isLight = colorHex.toLowerCase() === '#ffffff' || colorHex.toLowerCase() === '#f8f9fa' || colorHex.toLowerCase() === '#f4f1ec';

                return (
                  <button
                    key={colorName}
                    type="button"
                    onClick={() => handleColorChange(c, colorIdx)}
                    title={colorName}
                    className={`w-10 h-10 rounded-full p-0.5 flex items-center justify-center transition-all ${
                      isSelected ? 'border-2 border-aura-gold ring-4 ring-aura-gold/30 scale-110 shadow-lg' : 'border border-neutral-300 dark:border-neutral-700 hover:scale-105'
                    }`}
                  >
                    <span
                      className="w-full h-full rounded-full border border-black/10 dark:border-white/20 shadow-inner flex items-center justify-center"
                      style={{ backgroundColor: colorHex }}
                    >
                      {isSelected && (
                        <Check size={13} className={isLight ? 'text-black' : 'text-white'} strokeWidth={3} />
                      )}
                    </span>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Size Selector */}
          <div>
            <div className="flex items-center justify-between mb-3 text-xs">
              <span className="uppercase tracking-wider font-bold text-neutral-900 dark:text-neutral-100">
                Tailored Size: <span className="text-aura-gold">{selectedSize}</span>
              </span>
              <span className="text-neutral-400 dark:text-neutral-500 text-xs font-semibold">
                Fit: {product.fit_type || 'Standard'}
              </span>
            </div>
            <div className="flex flex-wrap gap-2.5">
              {['XS', 'S', 'M', 'L', 'XL'].map((sz) => {
                const isSelected = selectedSize === sz;
                const variantForSize = product.variants?.find(v => v.size === sz && v.color === selectedColor);
                const isAvailable = variantForSize ? variantForSize.stock_quantity > 0 : false;

                return (
                  <button
                    key={sz}
                    disabled={!isAvailable}
                    onClick={() => setSelectedSize(sz)}
                    className={`min-w-14 h-12 px-3 rounded-2xl text-xs font-bold flex items-center justify-center transition-all ${
                      isSelected
                        ? 'liquid-btn-gold text-neutral-950 shadow-lg scale-105'
                        : isAvailable
                          ? 'liquid-pill text-neutral-800 dark:text-neutral-200 hover:border-aura-gold/60'
                          : 'bg-neutral-100/50 dark:bg-neutral-900/50 text-neutral-300 dark:text-neutral-600 border border-neutral-200/40 dark:border-neutral-800/40 cursor-not-allowed line-through'
                    }`}
                  >
                    {sz}
                  </button>
                );
              })}
            </div>
          </div>

          {/* Stock Indicator */}
          <div className="text-xs">
            {isOutOfStock ? (
              <span className="text-rose-500 font-semibold flex items-center gap-1.5">
                <AlertCircle size={15} /> Currently Sold Out in this variation
              </span>
            ) : isLowStock ? (
              <span className="text-amber-600 dark:text-amber-400 font-semibold flex items-center gap-1.5 bg-amber-500/10 px-3 py-1.5 rounded-xl border border-amber-500/20">
                <AlertCircle size={15} /> Only {effectiveStock} units remaining in atelier. Order promptly.
              </span>
            ) : (
              <span className="text-emerald-600 dark:text-emerald-400 font-semibold flex items-center gap-1.5">
                <CheckCircle2 size={15} /> In Stock ({effectiveStock} available for dispatch)
              </span>
            )}
          </div>

          {/* Quantity Selector & Grand Add to Bag Button */}
          <div className="flex items-center gap-4 pt-2">
            <div className="flex items-center liquid-glass rounded-2xl border border-white/60 dark:border-white/10 p-1">
              <button
                disabled={quantity <= 1 || isOutOfStock}
                onClick={() => setQuantity(Math.max(1, quantity - 1))}
                className="w-10 h-11 text-base font-bold hover:bg-white/60 dark:hover:bg-white/10 text-neutral-800 dark:text-neutral-200 disabled:opacity-30 rounded-xl transition-all"
              >
                -
              </button>
              <span className="w-12 text-center text-sm font-bold text-neutral-900 dark:text-neutral-100 font-mono">{quantity}</span>
              <button
                disabled={quantity >= effectiveStock || isOutOfStock}
                onClick={() => setQuantity(quantity + 1)}
                className="w-10 h-11 text-base font-bold hover:bg-white/60 dark:hover:bg-white/10 text-neutral-800 dark:text-neutral-200 disabled:opacity-30 rounded-xl transition-all"
              >
                +
              </button>
            </div>

            <button
              disabled={isOutOfStock}
              onClick={handleAddToCart}
              className="flex-1 h-14 liquid-btn-gold text-neutral-950 text-xs uppercase tracking-widest font-bold rounded-2xl shadow-xl transition-all flex items-center justify-center gap-2.5 disabled:opacity-40 disabled:cursor-not-allowed"
            >
              <ShoppingBag size={18} />
              <span>{isOutOfStock ? 'Sold Out' : 'Add to Shopping Bag'}</span>
            </button>
          </div>

          {/* Status Alerts Feedback */}
          {cartSuccessMsg && (
            <div className="p-3.5 bg-emerald-500/15 border border-emerald-500/30 text-emerald-700 dark:text-emerald-300 text-xs font-semibold rounded-2xl flex items-center gap-2 animate-in fade-in">
              <CheckCircle2 size={16} />
              <span>{cartSuccessMsg}</span>
            </div>
          )}
          {cartErrorMsg && (
            <div className="p-3.5 bg-rose-500/15 border border-rose-500/30 text-rose-700 dark:text-rose-300 text-xs font-semibold rounded-2xl flex items-center gap-2 animate-in fade-in">
              <AlertCircle size={16} />
              <span>{cartErrorMsg}</span>
            </div>
          )}

          {/* Four Value Perks */}
          <div className="grid grid-cols-2 gap-3 pt-4 border-t border-neutral-200/50 dark:border-neutral-800/60 text-xs text-neutral-600 dark:text-neutral-300">
            <div className="flex items-center gap-2 p-2 rounded-xl liquid-glass">
              <Truck size={16} className="text-aura-gold shrink-0" />
              <span>Free Express Delivery over ₹2,499</span>
            </div>
            <div className="flex items-center gap-2 p-2 rounded-xl liquid-glass">
              <RefreshCw size={16} className="text-aura-gold shrink-0" />
              <span>30-Day Effortless Returns</span>
            </div>
            <div className="flex items-center gap-2 p-2 rounded-xl liquid-glass">
              <ShieldCheck size={16} className="text-aura-gold shrink-0" />
              <span>Authenticity Guaranteed</span>
            </div>
            <div className="flex items-center gap-2 p-2 rounded-xl liquid-glass">
              <Sparkles size={16} className="text-aura-gold shrink-0" />
              <span>Complimentary Gift Box</span>
            </div>
          </div>

          {/* Accordion Specification Tabs */}
          <div className="border-t border-neutral-200/50 dark:border-neutral-800/60 pt-6">
            <div className="flex gap-2 border-b border-neutral-200/50 dark:border-neutral-800/60 pb-2">
              <button
                onClick={() => setActiveTab('details')}
                className={`py-2 px-4 text-xs uppercase tracking-wider font-bold rounded-xl transition-all ${
                  activeTab === 'details' ? 'liquid-btn-gold text-neutral-950 shadow-md' : 'liquid-pill text-neutral-600 dark:text-neutral-400'
                }`}
              >
                Specifications
              </button>
              <button
                onClick={() => setActiveTab('materials')}
                className={`py-2 px-4 text-xs uppercase tracking-wider font-bold rounded-xl transition-all ${
                  activeTab === 'materials' ? 'liquid-btn-gold text-neutral-950 shadow-md' : 'liquid-pill text-neutral-600 dark:text-neutral-400'
                }`}
              >
                Material & Care
              </button>
              <button
                onClick={() => setActiveTab('shipping')}
                className={`py-2 px-4 text-xs uppercase tracking-wider font-bold rounded-xl transition-all ${
                  activeTab === 'shipping' ? 'liquid-btn-gold text-neutral-950 shadow-md' : 'liquid-pill text-neutral-600 dark:text-neutral-400'
                }`}
              >
                Delivery & Returns
              </button>
            </div>

            <div className="py-4 text-xs text-neutral-600 dark:text-neutral-300 space-y-2 leading-relaxed">
              {activeTab === 'details' && (
                <div className="space-y-2">
                  <p><span className="font-bold text-neutral-900 dark:text-neutral-100">SKU:</span> {currentVariant?.sku || 'AUR-STD'}</p>
                  <p><span className="font-bold text-neutral-900 dark:text-neutral-100">Fit Silhouette:</span> {product.fit_type || 'Tailored Modern Regular'}</p>
                  <p><span className="font-bold text-neutral-900 dark:text-neutral-100">Category:</span> {product.category_name}</p>
                </div>
              )}
              {activeTab === 'materials' && (
                <div className="space-y-2">
                  <p><span className="font-bold text-neutral-900 dark:text-neutral-100">Fabric Composition:</span> {product.material || '100% Premium Natural Fibers'}</p>
                  <p><span className="font-bold text-neutral-900 dark:text-neutral-100">Care Instructions:</span> {product.care_instructions || 'Hand wash cold or gentle dry clean. Line dry in shade.'}</p>
                </div>
              )}
              {activeTab === 'shipping' && (
                <div className="space-y-2">
                  <p>Dispatched within 24-48 business hours via Aura Express Courier.</p>
                  <p>Standard delivery arrives in 3-5 business days. Complimentary on orders exceeding ₹2,499.</p>
                  <p>Returns accepted within 30 days of delivery in pristine unworn condition.</p>
                </div>
              )}
            </div>

            {/* Tactile Fabric & Drape AI Advisor */}
            <div className="mt-4 p-4 rounded-2xl liquid-glass border border-aura-gold/30 space-y-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <div className="w-6 h-6 rounded-full bg-aura-gold/20 flex items-center justify-center text-aura-gold">
                    <Sparkles size={13} className="animate-pulse" />
                  </div>
                  <div>
                    <h4 className="text-xs uppercase tracking-wider font-bold text-neutral-900 dark:text-neutral-100">
                      Tactile Drape & Fabric Advisor
                    </h4>
                    <p className="text-[10px] text-neutral-500 dark:text-neutral-400">
                      Inquire about tactile weight, breathability, and wrinkle resilience
                    </p>
                  </div>
                </div>
                <span className="text-[9px] uppercase tracking-widest font-mono text-aura-gold font-bold px-2 py-0.5 rounded-full bg-aura-gold/10 border border-aura-gold/20">
                  Gemini AI
                </span>
              </div>

              {/* Quick Prompt Chips */}
              <div className="flex flex-wrap gap-1.5 pt-1">
                {[
                  "How does this fabric drape and move?",
                  "Is it breathable for warm climates?",
                  "Will this garment wrinkle easily?",
                  "How does the tactile weight feel?"
                ].map((q, idx) => (
                  <button
                    key={idx}
                    type="button"
                    onClick={() => handleAskFabric(q)}
                    disabled={isAskingFabric}
                    className="text-[11px] px-2.5 py-1 rounded-full liquid-pill text-neutral-700 dark:text-neutral-300 hover:text-aura-gold hover:border-aura-gold/50 transition-all text-left"
                  >
                    {q}
                  </button>
                ))}
              </div>

              {/* Custom Inquire Form */}
              <div className="flex gap-2 pt-1">
                <input
                  type="text"
                  value={fabricQuestion}
                  onChange={(e) => setFabricQuestion(e.target.value)}
                  placeholder="Ask specific fabric physics..."
                  onKeyDown={(e) => {
                    if (e.key === 'Enter') {
                      e.preventDefault();
                      handleAskFabric(fabricQuestion);
                    }
                  }}
                  className="flex-1 px-3 py-1.5 text-xs liquid-input rounded-xl text-neutral-900 dark:text-white placeholder-neutral-400"
                />
                <button
                  type="button"
                  onClick={() => handleAskFabric(fabricQuestion)}
                  disabled={isAskingFabric || !fabricQuestion.trim()}
                  className="px-3 py-1.5 liquid-btn-gold text-neutral-950 text-xs font-bold rounded-xl transition-all disabled:opacity-50 flex items-center gap-1 shrink-0"
                >
                  {isAskingFabric ? (
                    <span className="flex items-center gap-1">
                      <Sparkles size={12} className="animate-spin" /> Analyzing...
                    </span>
                  ) : (
                    <span>Ask AI</span>
                  )}
                </button>
              </div>

              {/* AI Drape Output */}
              {fabricAnswer && (
                <div className="mt-2 p-3 rounded-xl bg-amber-500/10 dark:bg-aura-gold/10 border border-aura-gold/30 text-xs text-neutral-800 dark:text-neutral-200 leading-relaxed animate-in fade-in">
                  <div className="flex items-center gap-1.5 text-[10px] uppercase font-bold text-aura-gold mb-1">
                    <Sparkles size={11} />
                    <span>Fabric Specialist Note</span>
                  </div>
                  <p>{fabricAnswer}</p>
                </div>
              )}
            </div>
          </div>

        </div>
      </div>

      {/* Algorithmic Recommendations Section */}
      <section className="pt-8">
        <div className="mb-8">
          <div className="flex items-center gap-2">
            <span className="text-[10px] uppercase tracking-[0.25em] text-aura-gold font-bold flex items-center gap-1.5">
              <Sparkles size={12} /> Algorithmic Haute Matching
            </span>
            <div className="group relative cursor-pointer text-neutral-400 hover:text-neutral-700">
              <Info size={14} />
              <div className="absolute left-1/2 -translate-x-1/2 bottom-full mb-2 w-72 p-3 liquid-glass text-neutral-900 dark:text-white text-[11px] rounded-2xl shadow-2xl opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none z-30 border border-white/60 dark:border-white/10">
                <p className="font-bold mb-1 text-aura-gold">MCA Project Synopsis Ranking Method:</p>
                <p>• Category Match: 40%</p>
                <p>• Price Proximity: 25%</p>
                <p>• Customer Rating: 20%</p>
                <p>• Garment Popularity: 15%</p>
              </div>
            </div>
          </div>
          <h2 className="text-2xl sm:text-3xl font-serif font-bold text-neutral-900 dark:text-neutral-100 mt-1">
            You May Also Like
          </h2>
          <p className="text-xs text-neutral-500 dark:text-neutral-400 mt-1">
            Styling complements scored via category similarity, price matching, and verified reviews.
          </p>
        </div>

        {recommendations.length > 0 ? (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 sm:gap-6">
            {recommendations.slice(0, 4).map((rec) => (
              <ProductCard
                key={rec.product.id}
                product={rec.product}
                recommendationScore={rec.score}
                recommendationBreakdown={rec.breakdown}
              />
            ))}
          </div>
        ) : (
          <p className="text-xs text-neutral-400">Discovering matching items...</p>
        )}
      </section>

      {/* Customer Reviews Section */}
      <section className="pt-8 border-t border-neutral-200/50 dark:border-neutral-800/60">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 sm:gap-12">
          
          {/* Reviews Summary & Review Submission */}
          <div className="space-y-6">
            <div>
              <h2 className="text-2xl font-serif font-bold text-neutral-900 dark:text-neutral-100">
                Patron Evaluation
              </h2>
              <div className="flex items-baseline gap-3 mt-3">
                <span className="text-4xl font-serif font-bold text-neutral-900 dark:text-neutral-100 font-mono">
                  {product.average_rating.toFixed(1)}
                </span>
                <div className="flex flex-col">
                  <ReviewStars rating={product.average_rating} size={16} />
                  <span className="text-xs text-neutral-500 dark:text-neutral-400 mt-0.5">
                    Based on {product.review_count} verified reviews
                  </span>
                </div>
              </div>

              {/* Rating distribution breakdown */}
              <div className="mt-6 space-y-2 text-xs">
                {[5, 4, 3, 2, 1].map((stars) => {
                  const count = product.rating_breakdown ? (product.rating_breakdown[stars] || 0) : 0;
                  const pct = product.review_count > 0 ? Math.round((count / product.review_count) * 100) : 0;
                  return (
                    <div key={stars} className="flex items-center gap-2">
                      <span className="w-12 text-neutral-600 dark:text-neutral-400 font-medium">{stars} Stars</span>
                      <div className="flex-1 h-2 bg-neutral-200 dark:bg-neutral-800 rounded-full overflow-hidden">
                        <div className="h-full bg-aura-gold rounded-full" style={{ width: `${pct}%` }} />
                      </div>
                      <span className="w-8 text-right text-neutral-400 font-mono">{count}</span>
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Write a review card */}
            <div className="liquid-glass rounded-3xl p-6 border border-white/70 dark:border-white/10 shadow-xl">
              <h3 className="text-sm font-bold text-neutral-900 dark:text-neutral-100 mb-1">Share Your Experience</h3>
              <p className="text-xs text-neutral-500 dark:text-neutral-400 mb-4">
                Purchased this piece? Help other patrons find their ideal silhouette.
              </p>

              {reviewSuccessMsg && (
                <div className="mb-4 p-3 bg-emerald-500/15 border border-emerald-500/30 text-emerald-700 dark:text-emerald-300 text-xs font-semibold rounded-xl">
                  {reviewSuccessMsg}
                </div>
              )}
              {reviewErrorMsg && (
                <div className="mb-4 p-3 bg-rose-500/15 border border-rose-500/30 text-rose-700 dark:text-rose-300 text-xs font-semibold rounded-xl">
                  {reviewErrorMsg}
                </div>
              )}

              <form onSubmit={handleReviewSubmit} className="space-y-4">
                <div>
                  <label className="text-[11px] uppercase tracking-wider font-bold text-neutral-700 dark:text-neutral-300 block mb-1">
                    Rating
                  </label>
                  <div className="flex gap-1 text-aura-gold">
                    {[1, 2, 3, 4, 5].map((starVal) => (
                      <button
                        type="button"
                        key={starVal}
                        onClick={() => setReviewRating(starVal)}
                        className="p-1 hover:scale-120 transition-transform"
                      >
                        <Star size={20} className={starVal <= reviewRating ? 'fill-aura-gold' : 'text-neutral-300 dark:text-neutral-700'} />
                      </button>
                    ))}
                  </div>
                </div>

                <div>
                  <label className="text-[11px] uppercase tracking-wider font-bold text-neutral-700 dark:text-neutral-300 block mb-1">
                    Review Headline
                  </label>
                  <input
                    type="text"
                    required
                    value={reviewTitle}
                    onChange={(e) => setReviewTitle(e.target.value)}
                    placeholder="e.g. Incomparable cashmere drape & softness"
                    className="w-full px-3.5 py-2.5 text-xs liquid-input text-neutral-900 dark:text-white rounded-xl"
                  />
                </div>

                <div>
                  <label className="text-[11px] uppercase tracking-wider font-bold text-neutral-700 dark:text-neutral-300 block mb-1">
                    Review Narrative
                  </label>
                  <textarea
                    required
                    rows={3}
                    value={reviewComment}
                    onChange={(e) => setReviewComment(e.target.value)}
                    placeholder="Share observations on texture, fit silhouette, and styling versatility..."
                    className="w-full px-3.5 py-2.5 text-xs liquid-input text-neutral-900 dark:text-white rounded-xl"
                  />
                </div>

                <button
                  type="submit"
                  disabled={reviewSubmitting}
                  className="w-full py-3 liquid-btn-gold text-neutral-950 text-xs uppercase tracking-widest font-bold rounded-xl shadow-lg transition-all"
                >
                  {reviewSubmitting ? 'Publishing...' : 'Publish Patron Review'}
                </button>
              </form>
            </div>
          </div>

          {/* Reviews List */}
          <div className="lg:col-span-2 space-y-6">
            <h3 className="text-base font-serif font-bold text-neutral-900 dark:text-neutral-100 pb-3 border-b border-neutral-200/50 dark:border-neutral-800/60">
              Verified Patron Feedback ({product.review_count})
            </h3>

            {product.recent_reviews && product.recent_reviews.length > 0 ? (
              <div className="space-y-4">
                {product.recent_reviews.map((rev) => (
                  <div key={rev.id} className="liquid-glass rounded-2xl p-5 border border-white/60 dark:border-white/10 shadow-sm space-y-2">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <ReviewStars rating={rev.rating} size={13} />
                        <h4 className="text-xs font-bold text-neutral-900 dark:text-neutral-100">{rev.title}</h4>
                      </div>
                      <span className="text-[11px] text-neutral-400 font-mono">
                        {new Date(rev.created_at).toLocaleDateString()}
                      </span>
                    </div>

                    <p className="text-xs text-neutral-600 dark:text-neutral-300 leading-relaxed">
                      &ldquo;{rev.comment}&rdquo;
                    </p>

                    <div className="flex items-center gap-2 pt-1 text-[11px] text-neutral-400">
                      <span className="font-semibold text-neutral-800 dark:text-neutral-200">{rev.user_name}</span>
                      {rev.is_verified_purchase && (
                        <span className="inline-flex items-center gap-1 text-emerald-600 dark:text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded-full text-[10px] font-semibold">
                          <CheckCircle2 size={11} /> Verified Patron
                        </span>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="liquid-glass rounded-3xl p-12 text-center text-xs text-neutral-400">
                Be the inaugural patron to publish a review for this piece.
              </div>
            )}
          </div>

        </div>
      </section>

    </div>
  );
};
