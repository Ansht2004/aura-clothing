import React, { useState, useRef, useEffect } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { 
  ShoppingBag, Heart, Search, User as UserIcon, 
  Menu, X, Bell, ChevronDown, Shield, LogOut, Sparkles 
} from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import { useCart } from '../../context/CartContext';
import { useWishlist } from '../../context/WishlistContext';
import { useNotifications } from '../../context/NotificationContext';
import { ThemeToggle } from './ThemeToggle';

export const Navbar: React.FC = () => {
  const { user, isAuthenticated, isAdmin, logout } = useAuth();
  const { summary } = useCart();
  const { wishlist } = useWishlist();
  const { notifications, unreadCount, markAsRead, markAllAsRead } = useNotifications();
  const navigate = useNavigate();
  const location = useLocation();

  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [searchOpen, setSearchOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [userMenuOpen, setUserMenuOpen] = useState(false);
  const [notifDropdownOpen, setNotifDropdownOpen] = useState(false);

  // Hover-Only Sliding Liquid Glass Lens State
  const navRef = useRef<HTMLElement>(null);
  const [indicator, setIndicator] = useState<{
    left: number;
    top: number;
    width: number;
    height: number;
    opacity: number;
    isMoving: boolean;
  }>({
    left: 0,
    top: 0,
    width: 0,
    height: 0,
    opacity: 0,
    isMoving: false,
  });
  const [hoveredPath, setHoveredPath] = useState<string | null>(null);

  const userRef = useRef<HTMLDivElement>(null);
  const notifRef = useRef<HTMLDivElement>(null);

  const currentPath = location.pathname + location.search;

  // Close dropdowns when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (userRef.current && !userRef.current.contains(event.target as Node)) {
        setUserMenuOpen(false);
      }
      if (notifRef.current && !notifRef.current.contains(event.target as Node)) {
        setNotifDropdownOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleLogout = () => {
    logout();
    setUserMenuOpen(false);
    navigate('/');
  };

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      navigate(`/products?search=${encodeURIComponent(searchQuery.trim())}`);
      setSearchOpen(false);
      setSearchQuery('');
    }
  };

  const navLinks = [
    { label: 'All Pieces', shortLabel: 'All', path: '/products' },
    { label: 'Gowns & Dresses', shortLabel: 'Dresses', path: '/products?category=evening-gowns' },
    { label: 'Fine Knitwear', shortLabel: 'Knitwear', path: '/products?category=fine-knitwear' },
    { label: 'Sweaters', shortLabel: 'Sweaters', path: '/products?category=sweaters-cardigans' },
    { label: 'Formal Shirts', shortLabel: 'Shirts', path: '/products?category=formal-dress-shirts' },
    { label: 'Tailored Blazers', shortLabel: 'Blazers', path: '/products?category=tailored-blazers' },
    { label: 'Selvedge Denim', shortLabel: 'Denim', path: '/products?category=selvedge-denim' },
    { label: 'Leather & Boots', shortLabel: 'Boots', path: '/products?category=leather-boots' },
  ];

  // Mouse move handler: snaps directly on first enter, glides smoothly between links
  const handleLinkMouseEnter = (e: React.MouseEvent<HTMLAnchorElement>, path: string) => {
    setHoveredPath(path);
    if (!navRef.current) return;
    const navRect = navRef.current.getBoundingClientRect();
    const linkRect = e.currentTarget.getBoundingClientRect();
    const targetLeft = linkRect.left - navRect.left;
    const targetTop = linkRect.top - navRect.top;
    const targetWidth = linkRect.width;
    const targetHeight = linkRect.height;

    setIndicator(prev => {
      if (prev.opacity === 0) {
        return {
          left: targetLeft,
          top: targetTop,
          width: targetWidth,
          height: targetHeight,
          opacity: 1,
          isMoving: false,
        };
      }
      return {
        left: targetLeft,
        top: targetTop,
        width: targetWidth,
        height: targetHeight,
        opacity: 1,
        isMoving: true,
      };
    });
  };

  // When mouse leaves nav, fade out completely (no stuck pill)
  const handleNavMouseLeave = () => {
    setHoveredPath(null);
    setIndicator(prev => ({
      ...prev,
      opacity: 0,
      isMoving: false,
    }));
  };

  return (
    <header className="sticky top-0 z-50 liquid-navbar transition-all duration-300">
      {/* Top Announcement Bar - Liquid Glass Banner */}
      <div className="bg-[#151413] dark:bg-black/95 backdrop-blur-md text-neutral-200 text-[10.5px] py-1.5 px-4 text-center font-medium tracking-[0.18em] uppercase border-b border-white/10 dark:border-aura-gold/20 flex items-center justify-center gap-2 shadow-sm">
        <Sparkles size={11} className="text-aura-gold animate-pulse shrink-0" />
        <span className="truncate sm:overflow-visible">Complimentary White-Glove Courier on Orders Over ₹2,499</span>
        <span className="text-aura-gold/80 hidden sm:inline">&bull;</span>
        <span className="text-aura-goldLight font-semibold hidden md:inline">Inaugural Privilege: Code WELCOME15 for 15% Off</span>
      </div>

      {/* Main Nav Bar Container */}
      <div className="w-full max-w-[1600px] mx-auto px-3 sm:px-4 lg:px-6 xl:px-8">
        <div className="flex items-center justify-between h-20 gap-2 sm:gap-4">
          
          {/* Mobile Menu Button */}
          <div className="flex items-center lg:hidden shrink-0">
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="w-10 h-10 rounded-full liquid-pill flex items-center justify-center text-neutral-800 dark:text-neutral-200 focus:outline-none"
              aria-label="Toggle mobile menu"
            >
              {mobileMenuOpen ? <X size={20} /> : <Menu size={20} />}
            </button>
          </div>

          {/* Brand Logo with Liquid Shimmer */}
          <div className="shrink-0 flex items-center">
            <Link to="/" className="flex flex-col group select-none">
              <span className="font-serif text-2xl lg:text-3xl font-medium tracking-[0.32em] text-neutral-950 dark:text-white group-hover:text-aura-gold transition-colors duration-300">
                AURA
              </span>
              <span className="text-[8px] uppercase tracking-[0.38em] text-neutral-400 dark:text-neutral-500 font-medium -mt-0.5 group-hover:text-aura-goldLight transition-colors whitespace-nowrap">
                HAUTE ATELIER
              </span>
            </Link>
          </div>

          {/* Desktop Categories Navigation - Liquid Glass Sliding Pill Track */}
          <nav 
            ref={navRef}
            onMouseLeave={handleNavMouseLeave}
            className="relative hidden lg:flex items-center space-x-0.5 xl:space-x-1 bg-white/50 dark:bg-neutral-900/50 backdrop-blur-md px-1.5 xl:px-2.5 py-1.5 rounded-full border border-white/80 dark:border-white/10 shadow-sm shrink min-w-0"
          >
            {/* Smooth Liquid Glass Gliding Pill (Active Only While Hovering) */}
            <div
              className="absolute top-0 left-0 rounded-full pointer-events-none z-0"
              style={{
                transform: `translate3d(${indicator.left}px, ${indicator.top}px, 0)`,
                width: `${indicator.width}px`,
                height: `${indicator.height}px`,
                opacity: indicator.opacity,
                transition: indicator.isMoving
                  ? 'transform 0.28s cubic-bezier(0.2, 0.8, 0.2, 1), width 0.28s cubic-bezier(0.2, 0.8, 0.2, 1), opacity 0.2s ease'
                  : 'opacity 0.2s ease',
              }}
            >
              {/* True Translucent Venetian Glass Lens (Never Solid Opaque) */}
              <div className="w-full h-full rounded-full bg-white/75 dark:bg-white/[0.08] backdrop-blur-md border border-white/90 dark:border-white/[0.14] shadow-[0_2px_12px_rgba(0,0,0,0.06),inset_0_1px_1px_rgba(255,255,255,0.95)] dark:shadow-[0_4px_16px_rgba(0,0,0,0.5),inset_0_1px_1px_rgba(255,255,255,0.15)] relative overflow-hidden">
                <div className="absolute inset-0 bg-gradient-to-r from-transparent via-aura-gold/15 dark:via-aura-gold/[0.12] to-transparent pointer-events-none" />
              </div>
            </div>

            {navLinks.map((link) => {
              const isHovered = hoveredPath === link.path;
              const isActive = currentPath === link.path;

              return (
                <Link
                  key={link.path}
                  to={link.path}
                  onMouseEnter={(e) => handleLinkMouseEnter(e, link.path)}
                  className={`relative z-10 whitespace-nowrap text-[10px] xl:text-[11px] font-semibold uppercase tracking-[0.14em] xl:tracking-[0.18em] px-2 lg:px-2.5 xl:px-3 py-1 xl:py-1.5 rounded-full transition-colors duration-200 select-none ${
                    isHovered
                      ? 'text-neutral-950 dark:text-white font-semibold'
                      : isActive
                        ? 'text-aura-gold dark:text-aura-goldLight font-semibold'
                        : 'text-neutral-600 dark:text-neutral-400 hover:text-neutral-900 dark:hover:text-white'
                  }`}
                >
                  <span className="inline 2xl:hidden">{link.shortLabel}</span>
                  <span className="hidden 2xl:inline">{link.label}</span>
                  {isActive && !isHovered && (
                    <span className="absolute bottom-0.5 left-1/2 -translate-x-1/2 w-1 h-1 rounded-full bg-aura-gold shadow-[0_0_6px_rgba(197,160,89,0.9)]" />
                  )}
                </Link>
              );
            })}
          </nav>

          {/* Right Action Icons */}
          <div className="flex items-center space-x-1 sm:space-x-2 shrink-0 z-20">
            
            {/* Search Trigger */}
            <button
              onClick={() => setSearchOpen(!searchOpen)}
              className="w-9 h-9 rounded-full flex items-center justify-center text-neutral-700 dark:text-neutral-300 hover:text-black dark:hover:text-white hover:bg-white/60 dark:hover:bg-white/10 border border-transparent hover:border-white/60 dark:hover:border-white/10 transition-all shrink-0"
              aria-label="Search"
              title="Search collections"
            >
              <Search size={18} strokeWidth={1.75} />
            </button>

            {/* Wishlist Link (Compact on mobile) */}
            <Link
              to="/wishlist"
              className="relative w-9 h-9 rounded-full hidden sm:flex items-center justify-center text-neutral-700 dark:text-neutral-300 hover:text-black dark:hover:text-white hover:bg-white/60 dark:hover:bg-white/10 border border-transparent hover:border-white/60 dark:hover:border-white/10 transition-all shrink-0"
              aria-label="Wishlist"
              title="Saved Wishlist"
            >
              <Heart size={18} strokeWidth={1.75} />
              {wishlist.length > 0 && (
                <span className="absolute -top-0.5 -right-0.5 bg-gradient-to-tr from-aura-gold to-aura-goldLight text-neutral-950 text-[10px] w-4 h-4 rounded-full flex items-center justify-center font-bold shadow-sm">
                  {wishlist.length}
                </span>
              )}
            </Link>

            {/* Shopping Cart Link */}
            <Link
              to="/cart"
              className="relative w-9 h-9 rounded-full flex items-center justify-center text-neutral-700 dark:text-neutral-300 hover:text-black dark:hover:text-white hover:bg-white/60 dark:hover:bg-white/10 border border-transparent hover:border-white/60 dark:hover:border-white/10 transition-all shrink-0"
              aria-label="Shopping Cart"
              title="Atelier Cart"
            >
              <ShoppingBag size={18} strokeWidth={1.75} />
              {summary.item_count > 0 && (
                <span className="absolute -top-0.5 -right-0.5 bg-aura-gold text-white text-[10px] w-4 h-4 rounded-full flex items-center justify-center font-bold shadow-sm animate-pulse">
                  {summary.item_count}
                </span>
              )}
            </Link>

            {/* Notifications Dropdown */}
            {isAuthenticated && (
              <div className="relative shrink-0" ref={notifRef}>
                <button
                  onClick={() => setNotifDropdownOpen(!notifDropdownOpen)}
                  className="relative w-9 h-9 rounded-full flex items-center justify-center text-neutral-700 dark:text-neutral-300 hover:text-black dark:hover:text-white hover:bg-white/60 dark:hover:bg-white/10 border border-transparent hover:border-white/60 dark:hover:border-white/10 transition-all shrink-0"
                  aria-label="Notifications"
                  title="Notifications"
                >
                  <Bell size={18} strokeWidth={1.75} />
                  {unreadCount > 0 && (
                    <span className="absolute -top-0.5 -right-0.5 bg-red-500 text-white text-[10px] w-4 h-4 rounded-full flex items-center justify-center font-bold animate-ping" />
                  )}
                  {unreadCount > 0 && (
                    <span className="absolute -top-0.5 -right-0.5 bg-red-500 text-white text-[10px] w-4 h-4 rounded-full flex items-center justify-center font-bold">
                      {unreadCount}
                    </span>
                  )}
                </button>

                {/* Notifications Popup - Liquid Glass Dropdown */}
                {notifDropdownOpen && (
                  <div className="absolute right-0 mt-3 w-80 sm:w-96 liquid-glass rounded-2xl shadow-2xl py-3 z-50 animate-in fade-in slide-in-from-top-2 duration-200">
                    <div className="px-4 py-2 border-b border-neutral-200/50 dark:border-neutral-800/60 flex items-center justify-between">
                      <span className="text-xs uppercase tracking-wider font-bold text-neutral-900 dark:text-neutral-100">
                        Atelier Notifications ({notifications.length})
                      </span>
                      {unreadCount > 0 && (
                        <button
                          onClick={markAllAsRead}
                          className="text-[11px] text-aura-gold hover:underline font-semibold"
                        >
                          Mark all as read
                        </button>
                      )}
                    </div>
                    <div className="max-h-72 overflow-y-auto divide-y divide-neutral-100/40 dark:divide-neutral-800/40">
                      {notifications.length === 0 ? (
                        <div className="p-6 text-center text-xs text-neutral-400">
                          No notifications yet
                        </div>
                      ) : (
                        notifications.slice(0, 5).map((notif) => (
                          <div
                            key={notif.id}
                            onClick={() => markAsRead(notif.id)}
                            className={`p-3.5 hover:bg-white/50 dark:hover:bg-white/5 transition-colors cursor-pointer ${
                              !notif.is_read ? 'bg-amber-500/10' : ''
                            }`}
                          >
                            <div className="flex items-start justify-between gap-2">
                              <span className="text-xs font-semibold text-neutral-900 dark:text-neutral-100">
                                {notif.title}
                              </span>
                              {!notif.is_read && (
                                <span className="w-2 h-2 rounded-full bg-aura-gold shrink-0 mt-1" />
                              )}
                            </div>
                            <p className="text-[12px] text-neutral-600 dark:text-neutral-300 mt-1 leading-snug">
                              {notif.message}
                            </p>
                            <span className="text-[10px] text-neutral-400 mt-1.5 block">
                              {new Date(notif.created_at).toLocaleDateString()}
                            </span>
                          </div>
                        ))
                      )}
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* User Account Menu - Prominent Gold Glass Pill */}
            <div className="relative shrink-0" ref={userRef}>
              {isAuthenticated ? (
                <div>
                  <button
                    onClick={() => setUserMenuOpen(!userMenuOpen)}
                    className="flex items-center gap-1.5 sm:gap-2 pl-1 pr-2 sm:pr-2.5 py-1 rounded-full bg-white/70 dark:bg-neutral-900/80 hover:bg-white dark:hover:bg-neutral-800 border border-neutral-300/80 dark:border-white/15 shadow-sm transition-all focus:outline-none select-none shrink-0"
                    title={`Signed in as ${user?.full_name}`}
                  >
                    <div className="w-7 h-7 rounded-full bg-gradient-to-tr from-aura-gold to-aura-goldLight text-neutral-950 flex items-center justify-center text-xs font-bold shadow-sm shrink-0">
                      {user?.full_name?.charAt(0).toUpperCase() || 'U'}
                    </div>
                    <span className="hidden sm:inline font-semibold text-neutral-800 dark:text-neutral-200 text-[11px] max-w-[85px] truncate">
                      {user?.full_name?.split(' ')[0]}
                    </span>
                    <ChevronDown size={13} className="text-neutral-400 shrink-0" />
                  </button>

                  {userMenuOpen && (
                    <div className="absolute right-0 mt-3 w-60 liquid-glass rounded-2xl shadow-2xl py-3 z-50 animate-in fade-in slide-in-from-top-2 duration-150">
                      <div className="px-4 py-2 border-b border-neutral-200/50 dark:border-neutral-800/60">
                        <p className="text-xs font-bold text-neutral-900 dark:text-neutral-100 truncate">{user?.full_name}</p>
                        <p className="text-[10px] text-neutral-400 truncate">{user?.email}</p>
                        <span className="inline-block mt-1 text-[9px] uppercase tracking-wider font-mono text-aura-gold font-bold">
                          {isAdmin ? 'ATELIER ADMIN' : user?.customer_code || 'PATRON'}
                        </span>
                      </div>

                      {isAdmin && (
                        <Link
                          to="/admin"
                          onClick={() => setUserMenuOpen(false)}
                          className="flex items-center gap-2 px-4 py-2.5 text-xs font-semibold text-aura-gold hover:bg-aura-gold/10 transition-colors border-b border-neutral-200/40 dark:border-neutral-800/40"
                        >
                          <Shield size={14} />
                          Admin Console
                        </Link>
                      )}

                      <Link
                        to="/profile"
                        onClick={() => setUserMenuOpen(false)}
                        className="block px-4 py-2 text-xs text-neutral-700 dark:text-neutral-300 hover:bg-white/50 dark:hover:bg-white/5 transition-colors"
                      >
                        Client Profile & Addresses
                      </Link>

                      <Link
                        to="/orders"
                        onClick={() => setUserMenuOpen(false)}
                        className="block px-4 py-2 text-xs text-neutral-700 dark:text-neutral-300 hover:bg-white/50 dark:hover:bg-white/5 transition-colors"
                      >
                        Order History & Returns
                      </Link>

                      <div className="border-t border-neutral-200/50 dark:border-neutral-800/50 mt-1.5 pt-1.5">
                        <button
                          onClick={handleLogout}
                          className="w-full text-left flex items-center gap-2 px-4 py-2 text-xs text-red-500 hover:bg-red-500/10 transition-colors rounded-b-xl"
                        >
                          <LogOut size={13} />
                          Sign Out
                        </button>
                      </div>
                    </div>
                  )}
                </div>
              ) : (
                <Link
                  to="/auth"
                  className="inline-flex items-center gap-1.5 px-3 sm:px-3.5 py-1.5 rounded-full bg-gradient-to-r from-aura-gold/20 via-aura-goldLight/20 to-aura-gold/20 hover:from-aura-gold/35 hover:to-aura-goldLight/35 text-neutral-900 dark:text-neutral-100 border border-aura-gold/50 hover:border-aura-gold shadow-sm transition-all duration-200 select-none shrink-0 group"
                  title="Sign in to your Atelier Account"
                >
                  <UserIcon size={14} className="text-aura-gold group-hover:scale-110 transition-transform" strokeWidth={2.2} />
                  <span className="text-[11px] sm:text-xs uppercase tracking-wider font-bold">Sign In</span>
                </Link>
              )}
            </div>

            {/* Top Right Dark / Light Mode Switch */}
            <div className="pl-1 sm:pl-2 ml-0.5 sm:ml-1 border-l border-neutral-300 dark:border-neutral-700/80 flex items-center shrink-0">
              <ThemeToggle />
            </div>

          </div>
        </div>

        {/* Expandable Liquid Glass Search Bar */}
        {searchOpen && (
          <div className="py-3 px-2 border-t border-white/20 dark:border-white/5 animate-in fade-in duration-200">
            <form onSubmit={handleSearchSubmit} className="relative max-w-xl mx-auto flex items-center">
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search cashmere, silk dresses, linen shirts, selvedge denim..."
                className="w-full pl-11 pr-24 py-2.5 text-sm liquid-input text-neutral-900 dark:text-white rounded-full placeholder-neutral-400 font-medium"
                autoFocus
              />
              <Search size={18} className="absolute left-4 text-aura-gold" />
              <button
                type="submit"
                className="absolute right-1.5 px-4 py-1.5 liquid-btn-gold text-neutral-950 text-[11px] uppercase tracking-wider font-bold rounded-full transition-all"
              >
                Search
              </button>
            </form>
          </div>
        )}
      </div>

      {/* Mobile Drawer Menu - Frosted Glass Sheet */}
      {mobileMenuOpen && (
        <div className="lg:hidden fixed inset-0 top-[112px] bg-black/60 z-40 backdrop-blur-md animate-in fade-in">
          <div className="liquid-glass w-4/5 max-w-sm h-full shadow-2xl p-6 overflow-y-auto border-r border-white/30 dark:border-white/10 rounded-r-3xl">
            <div className="flex flex-col space-y-4">
              
              {/* User Profile / Auth Section at top of mobile drawer */}
              {isAuthenticated ? (
                <div className="pb-3 border-b border-white/20 dark:border-white/10 flex items-center justify-between">
                  <div className="flex items-center gap-2.5">
                    <div className="w-10 h-10 rounded-full bg-gradient-to-tr from-aura-gold to-aura-goldLight text-neutral-950 flex items-center justify-center text-sm font-bold shadow-sm">
                      {user?.full_name?.charAt(0).toUpperCase() || 'U'}
                    </div>
                    <div>
                      <p className="text-sm font-bold text-neutral-900 dark:text-neutral-100">{user?.full_name}</p>
                      <span className="text-[10px] text-aura-gold uppercase font-mono tracking-wider font-semibold">
                        {isAdmin ? 'Atelier Administrator' : 'Client Patron'}
                      </span>
                    </div>
                  </div>
                </div>
              ) : (
                <Link
                  to="/auth"
                  onClick={() => setMobileMenuOpen(false)}
                  className="w-full text-center py-2.5 bg-gradient-to-r from-aura-gold to-aura-goldLight text-neutral-950 text-xs uppercase tracking-widest font-bold rounded-full shadow-md flex items-center justify-center gap-2"
                >
                  <UserIcon size={15} />
                  <span>Sign In / Atelier Account</span>
                </Link>
              )}

              {/* Theme Toggle in Mobile Drawer */}
              <div className="py-2.5 px-3 rounded-2xl bg-white/40 dark:bg-white/5 border border-white/30 dark:border-white/10 flex items-center justify-between">
                <span className="text-xs uppercase tracking-wider font-semibold text-neutral-700 dark:text-neutral-300">
                  Day / Night Mode
                </span>
                <ThemeToggle />
              </div>

              {/* Atelier Collections Header */}
              <span className="text-[10px] uppercase tracking-widest text-aura-gold font-bold pt-1 border-b border-white/20 dark:border-white/10 pb-1">
                Atelier Collections
              </span>
              {navLinks.map((link) => (
                <Link
                  key={link.path}
                  to={link.path}
                  onClick={() => setMobileMenuOpen(false)}
                  className="text-sm font-semibold uppercase tracking-wider text-neutral-800 dark:text-neutral-200 hover:text-aura-gold py-1.5 px-2 rounded-lg hover:bg-white/40 dark:hover:bg-white/5 transition-all"
                >
                  {link.label}
                </Link>
              ))}

              {/* Additional Mobile Navigation Links */}
              <div className="pt-3 border-t border-white/20 dark:border-white/10 flex flex-col space-y-2.5">
                <Link
                  to="/wishlist"
                  onClick={() => setMobileMenuOpen(false)}
                  className="flex items-center justify-between text-xs font-semibold uppercase tracking-wider text-neutral-700 dark:text-neutral-300 hover:text-aura-gold py-1"
                >
                  <span className="flex items-center gap-2"><Heart size={15} /> Wishlist</span>
                  {wishlist.length > 0 && (
                    <span className="px-2 py-0.5 rounded-full bg-aura-gold/20 text-aura-gold text-[10px] font-bold">
                      {wishlist.length}
                    </span>
                  )}
                </Link>
                {isAuthenticated && (
                  <>
                    {isAdmin && (
                      <Link to="/admin" onClick={() => setMobileMenuOpen(false)} className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-aura-gold py-1">
                        <Shield size={15} /> Admin Console
                      </Link>
                    )}
                    <Link to="/profile" onClick={() => setMobileMenuOpen(false)} className="text-xs uppercase tracking-wider text-neutral-700 dark:text-neutral-300 py-1">
                      Client Profile & Addresses
                    </Link>
                    <Link to="/orders" onClick={() => setMobileMenuOpen(false)} className="text-xs uppercase tracking-wider text-neutral-700 dark:text-neutral-300 py-1">
                      Order History & Returns
                    </Link>
                    <button onClick={() => { handleLogout(); setMobileMenuOpen(false); }} className="text-xs uppercase tracking-wider text-red-500 text-left py-1 flex items-center gap-2">
                      <LogOut size={14} /> Sign Out
                    </button>
                  </>
                )}
              </div>
            </div>
          </div>
        </div>
      )}
    </header>
  );
};
