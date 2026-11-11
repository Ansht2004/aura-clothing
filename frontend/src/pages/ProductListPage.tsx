import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { Filter, X, SlidersHorizontal, Check, RefreshCw } from 'lucide-react';
import { api } from '../services/api';
import { Product, Category } from '../types';
import { ProductCard } from '../components/common/ProductCard';
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import { EmptyState } from '../components/common/EmptyState';

const AVAILABLE_SIZES = ['XS', 'S', 'M', 'L', 'XL'];
const AVAILABLE_COLORS = [
  { name: 'Black', hex: '#1A1A1A' },
  { name: 'White', hex: '#F8F9FA' },
  { name: 'Navy', hex: '#1E2A38' },
  { name: 'Olive', hex: '#556B2F' },
  { name: 'Beige', hex: '#C19A6B' },
  { name: 'Burgundy', hex: '#800020' },
  { name: 'Grey', hex: '#36454F' },
  { name: 'Cerulean', hex: '#007BA7' },
];

export const ProductListPage: React.FC = () => {
  const [searchParams, setSearchParams] = useSearchParams();

  const [products, setProducts] = useState<Product[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [pagination, setPagination] = useState({
    page: 1,
    per_page: 12,
    total_items: 0,
    total_pages: 1
  });
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [connectionError, setConnectionError] = useState<boolean>(false);
  const [mobileFilterOpen, setMobileFilterOpen] = useState<boolean>(false);

  // Filter states extracted from URL
  const currentCategory = searchParams.get('category') || '';
  const currentSearch = searchParams.get('search') || '';
  const currentSort = searchParams.get('sort') || 'popular';
  const currentSize = searchParams.get('size') || '';
  const currentColor = searchParams.get('color') || '';
  const currentMinPrice = searchParams.get('min_price') || '';
  const currentMaxPrice = searchParams.get('max_price') || '';
  const currentMinRating = searchParams.get('min_rating') || '';
  const currentInStock = searchParams.get('in_stock') === 'true';
  const currentPage = parseInt(searchParams.get('page') || '1', 10);

  // Local price inputs
  const [priceRange, setPriceRange] = useState({
    min: currentMinPrice,
    max: currentMaxPrice
  });

  // Load categories
  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const res = await api.getCategories();
        setCategories(res.categories || []);
      } catch (err) {
        console.error("Failed to load categories:", err);
      }
    };
    fetchCategories();
  }, []);

  // Fetch products with active filters
  useEffect(() => {
    const fetchProducts = async () => {
      setIsLoading(true);
      setConnectionError(false);
      try {
        const queryParams = new URLSearchParams(searchParams);
        if (!queryParams.has('per_page')) {
          queryParams.set('per_page', '12');
        }
        const res = await api.getProducts(queryParams.toString());
        setProducts(res.products || []);
        if (res.pagination) {
          setPagination(res.pagination);
        }
      } catch (err) {
        console.error("Failed to fetch products:", err);
        setConnectionError(true);
      } finally {
        setIsLoading(false);
      }
    };

    fetchProducts();
  }, [searchParams]);

  const updateParam = (key: string, value: string) => {
    const next = new URLSearchParams(searchParams);
    if (value) {
      next.set(key, value);
    } else {
      next.delete(key);
    }
    if (key !== 'page') {
      next.delete('page');
    }
    setSearchParams(next);
  };

  const handleClearAllFilters = () => {
    setSearchParams(new URLSearchParams());
    setPriceRange({ min: '', max: '' });
  };

  const activeFiltersCount = [
    currentCategory, currentSize, currentColor, currentMinPrice,
    currentMaxPrice, currentMinRating, currentInStock ? 'instock' : ''
  ].filter(Boolean).length;

  const FilterSidebarContent = (
    <div className="space-y-6 text-xs">
      {/* Category Filter */}
      <div>
        <h4 className="uppercase tracking-widest font-bold text-neutral-900 dark:text-neutral-100 mb-3 text-[11px] flex items-center justify-between">
          <span>Categories</span>
          <span className="text-[10px] text-aura-gold font-mono">{categories.length}</span>
        </h4>
        <div className="space-y-1.5 max-h-56 overflow-y-auto pr-1">
          <button
            onClick={() => updateParam('category', '')}
            className={`w-full text-left py-2 px-3 rounded-xl transition-all flex items-center justify-between ${
              !currentCategory 
                ? 'liquid-btn-gold text-neutral-950 font-bold shadow-md' 
                : 'text-neutral-600 dark:text-neutral-300 hover:bg-white/60 dark:hover:bg-white/5'
            }`}
          >
            <span>All Categories</span>
          </button>
          {categories.map((cat) => (
            <button
              key={cat.id}
              onClick={() => updateParam('category', cat.slug)}
              className={`w-full text-left py-2 px-3 rounded-xl transition-all flex items-center justify-between ${
                currentCategory === cat.slug 
                  ? 'liquid-btn-gold text-neutral-950 font-bold shadow-md' 
                  : 'text-neutral-600 dark:text-neutral-300 hover:bg-white/60 dark:hover:bg-white/5'
              }`}
            >
              <span>{cat.name}</span>
              {cat.product_count !== undefined && (
                <span className={`text-[10px] font-mono ${currentCategory === cat.slug ? 'text-neutral-950 font-bold' : 'text-neutral-400'}`}>
                  {cat.product_count}
                </span>
              )}
            </button>
          ))}
        </div>
      </div>

      {/* Size Filter */}
      <div className="border-t border-neutral-200/50 dark:border-neutral-800/60 pt-5">
        <h4 className="uppercase tracking-widest font-bold text-neutral-900 dark:text-neutral-100 mb-3 text-[11px]">
          Tailored Size
        </h4>
        <div className="flex flex-wrap gap-2">
          {AVAILABLE_SIZES.map((sz) => {
            const isSelected = currentSize === sz;
            return (
              <button
                key={sz}
                onClick={() => updateParam('size', isSelected ? '' : sz)}
                className={`w-10 h-10 rounded-xl text-xs font-bold flex items-center justify-center transition-all ${
                  isSelected 
                    ? 'liquid-btn-gold text-neutral-950 shadow-md scale-105' 
                    : 'liquid-pill text-neutral-700 dark:text-neutral-300 hover:border-aura-gold/50'
                }`}
              >
                {sz}
              </button>
            );
          })}
        </div>
      </div>

      {/* Color Filter */}
      <div className="border-t border-neutral-200/50 dark:border-neutral-800/60 pt-5">
        <h4 className="uppercase tracking-widest font-bold text-neutral-900 dark:text-neutral-100 mb-3 text-[11px]">
          Palette Selection
        </h4>
        <div className="grid grid-cols-4 gap-2">
          {AVAILABLE_COLORS.map((col) => {
            const isSelected = currentColor.toLowerCase() === col.name.toLowerCase();
            return (
              <button
                key={col.name}
                onClick={() => updateParam('color', isSelected ? '' : col.name)}
                title={col.name}
                className={`flex flex-col items-center p-1.5 rounded-xl border transition-all ${
                  isSelected 
                    ? 'border-aura-gold bg-aura-gold/15 shadow-sm ring-1 ring-aura-gold' 
                    : 'border-transparent hover:bg-white/50 dark:hover:bg-white/5'
                }`}
              >
                <span
                  className="w-6 h-6 rounded-full border border-black/10 dark:border-white/20 shadow-inner flex items-center justify-center transition-transform hover:scale-110"
                  style={{ backgroundColor: col.hex }}
                >
                  {isSelected && (
                    <Check size={12} className={col.name === 'White' ? 'text-black' : 'text-white'} />
                  )}
                </span>
                <span className="text-[10px] text-neutral-600 dark:text-neutral-300 mt-1 truncate max-w-full font-medium">{col.name}</span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Price Range Filter */}
      <div className="border-t border-neutral-200/50 dark:border-neutral-800/60 pt-5">
        <h4 className="uppercase tracking-widest font-bold text-neutral-900 dark:text-neutral-100 mb-3 text-[11px]">
          Price Range (₹)
        </h4>
        <div className="flex items-center gap-2">
          <input
            type="number"
            placeholder="Min"
            value={priceRange.min}
            onChange={(e) => setPriceRange({ ...priceRange, min: e.target.value })}
            className="w-full px-3 py-2 liquid-input text-neutral-900 dark:text-white rounded-xl text-xs"
          />
          <span className="text-neutral-400 font-bold">-</span>
          <input
            type="number"
            placeholder="Max"
            value={priceRange.max}
            onChange={(e) => setPriceRange({ ...priceRange, max: e.target.value })}
            className="w-full px-3 py-2 liquid-input text-neutral-900 dark:text-white rounded-xl text-xs"
          />
        </div>
        <button
          onClick={() => {
            updateParam('min_price', priceRange.min);
            updateParam('max_price', priceRange.max);
          }}
          className="mt-2.5 w-full py-2 liquid-btn-glass text-neutral-800 dark:text-neutral-200 text-[11px] uppercase tracking-wider font-bold rounded-xl transition-all"
        >
          Apply Filter
        </button>
      </div>

      {/* Minimum Rating */}
      <div className="border-t border-neutral-200/50 dark:border-neutral-800/60 pt-5">
        <h4 className="uppercase tracking-widest font-bold text-neutral-900 dark:text-neutral-100 mb-3 text-[11px]">
          Patron Evaluation
        </h4>
        <div className="space-y-1.5">
          {[4, 3].map((stars) => (
            <button
              key={stars}
              onClick={() => updateParam('min_rating', currentMinRating === String(stars) ? '' : String(stars))}
              className={`w-full text-left py-2 px-3 rounded-xl flex items-center justify-between transition-all ${
                currentMinRating === String(stars) 
                  ? 'liquid-glass border-aura-gold/50 text-aura-gold font-bold shadow-sm' 
                  : 'text-neutral-600 dark:text-neutral-300 hover:bg-white/60 dark:hover:bg-white/5'
              }`}
            >
              <span>{stars} Stars & Above</span>
              {currentMinRating === String(stars) && <Check size={13} className="text-aura-gold" />}
            </button>
          ))}
        </div>
      </div>

      {/* In Stock Only Toggle */}
      <div className="border-t border-neutral-200/50 dark:border-neutral-800/60 pt-5">
        <label className="flex items-center gap-2.5 cursor-pointer select-none">
          <input
            type="checkbox"
            checked={currentInStock}
            onChange={(e) => updateParam('in_stock', e.target.checked ? 'true' : '')}
            className="w-4 h-4 rounded text-aura-gold focus:ring-aura-gold border-neutral-300 dark:border-neutral-700 bg-white dark:bg-neutral-800"
          />
          <span className="text-neutral-700 dark:text-neutral-300 text-xs font-semibold">In Stock Garments Only</span>
        </label>
      </div>

      {/* Clear All Filters Button */}
      {activeFiltersCount > 0 && (
        <button
          onClick={handleClearAllFilters}
          className="w-full py-2.5 rounded-xl border border-rose-300 dark:border-rose-900/60 text-rose-600 dark:text-rose-400 hover:bg-rose-500/10 text-xs uppercase tracking-wider font-bold transition-all flex items-center justify-center gap-1.5 shadow-sm"
        >
          <RefreshCw size={12} />
          Reset All Filters ({activeFiltersCount})
        </button>
      )}
    </div>
  );

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12 space-y-8">
      {connectionError && (
        <div className="liquid-glass border border-amber-500/40 text-neutral-900 dark:text-neutral-100 px-5 py-3.5 rounded-2xl shadow-lg flex items-center justify-between">
          <span className="text-xs font-semibold flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded-full bg-amber-500 animate-pulse" />
            Backend connection offline. Re-establishing link on port 5000...
          </span>
          <button onClick={() => window.location.reload()} className="px-4 py-1.5 liquid-btn-gold text-neutral-950 rounded-full text-xs font-bold">
            Retry Connection
          </button>
        </div>
      )}

      {/* Header and Controls - Liquid Glass Banner */}
      <div className="liquid-glass rounded-3xl p-6 sm:p-8 border border-white/80 dark:border-white/10 shadow-xl flex flex-col md:flex-row md:items-end justify-between gap-6">
        <div>
          <span className="inline-flex items-center gap-1.5 px-3.5 py-1 rounded-full liquid-pill text-[9.5px] uppercase tracking-[0.25em] text-aura-gold font-semibold">
            CATALOGUE ÉDITION
          </span>
          <h1 className="text-3xl sm:text-5xl font-serif font-normal tracking-tight text-neutral-950 dark:text-white mt-2">
            {currentCategory 
              ? categories.find(c => c.slug === currentCategory)?.name || 'Collection'
              : currentSearch 
                ? `Search: "${currentSearch}"` 
                : 'All Apparel Pieces'}
          </h1>
          <p className="text-xs text-neutral-500 dark:text-neutral-400 mt-1 font-light tracking-wide">
            Presenting {pagination.total_items} handcrafted couture garments
          </p>
        </div>

        {/* Sort & Mobile Filter Toggle */}
        <div className="flex items-center gap-3">
          {/* Mobile Filter Button */}
          <button
            onClick={() => setMobileFilterOpen(true)}
            className="lg:hidden flex items-center gap-2 px-4 py-2.5 liquid-pill text-xs font-bold text-neutral-800 dark:text-neutral-200 shadow-sm"
          >
            <Filter size={14} />
            <span>Refine {activeFiltersCount > 0 && `(${activeFiltersCount})`}</span>
          </button>

          {/* Sort Dropdown */}
          <div className="relative flex items-center liquid-glass px-3 py-1.5 rounded-2xl border border-white/60 dark:border-white/10">
            <span className="text-[10px] text-neutral-400 dark:text-neutral-500 mr-2 uppercase tracking-wider font-bold hidden sm:inline">Sort:</span>
            <select
              value={currentSort}
              onChange={(e) => updateParam('sort', e.target.value)}
              className="bg-transparent text-xs text-neutral-800 dark:text-neutral-200 py-1 pr-6 font-semibold focus:outline-none cursor-pointer"
            >
              <option value="popular" className="bg-white dark:bg-neutral-900">Most Popular</option>
              <option value="rating" className="bg-white dark:bg-neutral-900">Highest Rated</option>
              <option value="price_asc" className="bg-white dark:bg-neutral-900">Price: Low to High</option>
              <option value="price_desc" className="bg-white dark:bg-neutral-900">Price: High to Low</option>
              <option value="newest" className="bg-white dark:bg-neutral-900">Newest Arrivals</option>
            </select>
          </div>
        </div>
      </div>

      {/* Active Filter Tags */}
      {activeFiltersCount > 0 && (
        <div className="flex flex-wrap items-center gap-2 py-1">
          <span className="text-xs text-neutral-400 font-semibold">Active Criteria:</span>
          {currentCategory && (
            <span className="inline-flex items-center gap-1.5 px-3 py-1 liquid-pill text-neutral-800 dark:text-neutral-200 text-xs font-semibold">
              Category: {categories.find(c => c.slug === currentCategory)?.name || currentCategory}
              <button onClick={() => updateParam('category', '')} className="hover:text-rose-500"><X size={12} /></button>
            </span>
          )}
          {currentSize && (
            <span className="inline-flex items-center gap-1.5 px-3 py-1 liquid-pill text-neutral-800 dark:text-neutral-200 text-xs font-semibold">
              Size: {currentSize}
              <button onClick={() => updateParam('size', '')} className="hover:text-rose-500"><X size={12} /></button>
            </span>
          )}
          {currentColor && (
            <span className="inline-flex items-center gap-1.5 px-3 py-1 liquid-pill text-neutral-800 dark:text-neutral-200 text-xs font-semibold">
              Color: {currentColor}
              <button onClick={() => updateParam('color', '')} className="hover:text-rose-500"><X size={12} /></button>
            </span>
          )}
          {(currentMinPrice || currentMaxPrice) && (
            <span className="inline-flex items-center gap-1.5 px-3 py-1 liquid-pill text-neutral-800 dark:text-neutral-200 text-xs font-semibold">
              Price: ₹{currentMinPrice || '0'} - ₹{currentMaxPrice || '∞'}
              <button onClick={() => { updateParam('min_price', ''); updateParam('max_price', ''); }} className="hover:text-rose-500"><X size={12} /></button>
            </span>
          )}
          {currentInStock && (
            <span className="inline-flex items-center gap-1.5 px-3 py-1 liquid-pill text-neutral-800 dark:text-neutral-200 text-xs font-semibold">
              In Stock Only
              <button onClick={() => updateParam('in_stock', '')} className="hover:text-rose-500"><X size={12} /></button>
            </span>
          )}
          <button
            onClick={handleClearAllFilters}
            className="text-xs text-aura-gold hover:underline font-bold ml-2"
          >
            Clear All
          </button>
        </div>
      )}

      {/* Main Layout Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
        
        {/* Desktop Sidebar Filters - Sticky Liquid Glass Card */}
        <aside className="hidden lg:block lg:col-span-1">
          <div className="sticky top-28 liquid-glass p-6 rounded-3xl border border-white/70 dark:border-white/10 shadow-xl">
            <div className="flex items-center justify-between pb-3 mb-5 border-b border-neutral-200/50 dark:border-neutral-800/60">
              <span className="font-serif font-bold text-base tracking-wide text-neutral-900 dark:text-neutral-100">
                Filter Apparel
              </span>
              <SlidersHorizontal size={16} className="text-aura-gold" />
            </div>
            {FilterSidebarContent}
          </div>
        </aside>

        {/* Product Grid Area */}
        <main className="lg:col-span-3">
          {isLoading ? (
            <LoadingSpinner message="Refining Catalogue..." />
          ) : products.length === 0 ? (
            <div className="liquid-glass rounded-3xl p-12 text-center border border-white/60 dark:border-white/10 shadow-xl">
              <EmptyState
                icon={SlidersHorizontal}
                title="No garments matched your criteria"
                description="Try adjusting your filter settings or search query to explore other pieces from our collections."
                actionText="Reset All Filters"
                onAction={handleClearAllFilters}
              />
            </div>
          ) : (
            <>
              <div className="grid grid-cols-2 sm:grid-cols-3 gap-5 sm:gap-6">
                {products.map((product) => (
                  <ProductCard key={product.id} product={product} />
                ))}
              </div>

              {/* Pagination Controls - Liquid Glass Stepper */}
              {pagination.total_pages > 1 && (
                <div className="mt-14 pt-8 border-t border-neutral-200/50 dark:border-neutral-800/60 flex items-center justify-center gap-2">
                  <button
                    disabled={currentPage <= 1}
                    onClick={() => updateParam('page', String(currentPage - 1))}
                    className="px-4 py-2 liquid-pill text-xs font-bold text-neutral-700 dark:text-neutral-300 disabled:opacity-30 disabled:cursor-not-allowed transition-all"
                  >
                    Previous
                  </button>

                  {Array.from({ length: pagination.total_pages }).map((_, idx) => {
                    const pageNum = idx + 1;
                    const isActive = pageNum === currentPage;
                    return (
                      <button
                        key={pageNum}
                        onClick={() => updateParam('page', String(pageNum))}
                        className={`w-9 h-9 rounded-xl text-xs font-bold transition-all ${
                          isActive 
                            ? 'liquid-btn-gold text-neutral-950 shadow-md scale-105' 
                            : 'liquid-pill text-neutral-700 dark:text-neutral-300'
                        }`}
                      >
                        {pageNum}
                      </button>
                    );
                  })}

                  <button
                    disabled={currentPage >= pagination.total_pages}
                    onClick={() => updateParam('page', String(currentPage + 1))}
                    className="px-4 py-2 liquid-pill text-xs font-bold text-neutral-700 dark:text-neutral-300 disabled:opacity-30 disabled:cursor-not-allowed transition-all"
                  >
                    Next
                  </button>
                </div>
              )}
            </>
          )}
        </main>
      </div>

      {/* Mobile Drawer Filter Dialog - Liquid Glass Sheet */}
      {mobileFilterOpen && (
        <div className="fixed inset-0 z-50 flex lg:hidden bg-black/60 backdrop-blur-md animate-in fade-in">
          <div className="liquid-glass w-4/5 max-w-sm h-full shadow-2xl p-6 overflow-y-auto ml-auto flex flex-col justify-between border-l border-white/30 dark:border-white/10 rounded-l-3xl">
            <div>
              <div className="flex items-center justify-between pb-4 mb-4 border-b border-white/20 dark:border-white/10">
                <h3 className="font-serif font-bold text-lg text-neutral-900 dark:text-neutral-100">Filter Pieces</h3>
                <button onClick={() => setMobileFilterOpen(false)} className="w-8 h-8 rounded-full liquid-pill flex items-center justify-center text-neutral-500">
                  <X size={18} />
                </button>
              </div>
              {FilterSidebarContent}
            </div>
            <div className="pt-6 border-t border-white/20 dark:border-white/10 mt-6">
              <button
                onClick={() => setMobileFilterOpen(false)}
                className="w-full py-3.5 liquid-btn-gold text-neutral-950 text-xs uppercase tracking-widest font-bold rounded-2xl shadow-xl"
              >
                Show Results
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
