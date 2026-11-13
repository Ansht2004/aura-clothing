import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight, CheckCircle2, Shield, Sparkles } from 'lucide-react';
import { AuraLogo } from './AuraLogo';

export const Footer: React.FC = () => {
  const [email, setEmail] = useState('');
  const [subscribed, setSubscribed] = useState(false);

  const handleSubscribe = (e: React.FormEvent) => {
    e.preventDefault();
    if (email) {
      setSubscribed(true);
      setEmail('');
    }
  };

  return (
    <footer className="liquid-glass rounded-t-3xl border-t border-white/70 dark:border-white/10 mt-24 shadow-2xl relative z-10">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="grid grid-cols-1 md:grid-cols-5 gap-10">
          
          {/* Brand Identity */}
          <div className="md:col-span-2 space-y-4">
            <AuraLogo variant="footer" />
            <p className="text-xs text-neutral-600 dark:text-neutral-300 leading-relaxed max-w-sm font-normal">
              Aura Apparel is dedicated to the art of architectural wardrobe curation. We weave certified mulberry silk, unspun Mongolian cashmere, and artisanal selvedge denim into timeless pieces designed to transcend fleeting seasons.
            </p>
            <div className="pt-2 text-xs text-neutral-500 dark:text-neutral-400 space-y-1">
              <p>Atelier Studio: 742 Fifth Avenue, Suite 100, New York & Mumbai</p>
              <p>Private Concierge: <span className="text-aura-gold font-semibold">concierge@auraapparel.com</span></p>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="text-xs uppercase tracking-widest font-bold text-neutral-900 dark:text-neutral-100 mb-4 flex items-center gap-1.5">
              <Sparkles size={12} className="text-aura-gold" /> Collections
            </h4>
            <ul className="space-y-2.5 text-xs text-neutral-600 dark:text-neutral-400 font-medium">
              <li><Link to="/products?category=womens-dresses" className="hover:text-aura-gold transition-colors">Mulberry Silk Dresses</Link></li>
              <li><Link to="/products?category=mens-shirts" className="hover:text-aura-gold transition-colors">Japanese Twill Shirts</Link></li>
              <li><Link to="/products?category=blazers-coats" className="hover:text-aura-gold transition-colors">Hand-Tailored Blazers</Link></li>
              <li><Link to="/products?category=knitwear-sweaters" className="hover:text-aura-gold transition-colors">Mongolian Cashmere</Link></li>
              <li><Link to="/products?category=summer-linen" className="hover:text-aura-gold transition-colors">Normandy Flax Linen</Link></li>
              <li><Link to="/products?category=denim-jeans" className="hover:text-aura-gold transition-colors">Okayama Selvedge Denim</Link></li>
            </ul>
          </div>

          {/* Customer Care */}
          <div>
            <h4 className="text-xs uppercase tracking-widest font-bold text-neutral-900 dark:text-neutral-100 mb-4 flex items-center gap-1.5">
              <Shield size={12} className="text-aura-gold" /> Client Care
            </h4>
            <ul className="space-y-2.5 text-xs text-neutral-600 dark:text-neutral-400 font-medium">
              <li><Link to="/orders" className="hover:text-aura-gold transition-colors">Order Tracking Stepper</Link></li>
              <li><Link to="/orders" className="hover:text-aura-gold transition-colors">Returns & Restock</Link></li>
              <li><Link to="/profile" className="hover:text-aura-gold transition-colors">Delivery Destinations</Link></li>
              <li><Link to="/cart" className="hover:text-aura-gold transition-colors">Atelier Shopping Bag</Link></li>
              <li><Link to="/wishlist" className="hover:text-aura-gold transition-colors">Saved Wishlist</Link></li>
              <li><Link to="/auth" className="hover:text-aura-gold transition-colors">Patron Account Sign In</Link></li>
            </ul>
          </div>

          {/* Newsletter Dispatch */}
          <div>
            <h4 className="text-xs uppercase tracking-widest font-bold text-neutral-900 dark:text-neutral-100 mb-4">
              The Aura Dispatch
            </h4>
            <p className="text-xs text-neutral-600 dark:text-neutral-400 leading-relaxed mb-4 font-normal">
              Receive private invitations to seasonal private sales, new capsule collections, and fabric stories.
            </p>
            {subscribed ? (
              <div className="flex items-center gap-2 text-xs text-emerald-600 dark:text-emerald-400 bg-emerald-500/10 p-3 rounded-2xl border border-emerald-500/20 font-semibold">
                <CheckCircle2 size={16} />
                <span>You are subscribed to The Aura Dispatch.</span>
              </div>
            ) : (
              <form onSubmit={handleSubscribe} className="space-y-2">
                <div className="relative flex items-center">
                  <input
                    type="email"
                    required
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="Enter your email"
                    className="w-full liquid-input text-neutral-900 dark:text-white placeholder-neutral-400 text-xs px-4 py-2.5 rounded-full pr-12 font-medium"
                  />
                  <button
                    type="submit"
                    aria-label="Subscribe to newsletter"
                    className="absolute right-1 w-8 h-8 liquid-btn-gold rounded-full flex items-center justify-center text-neutral-950 shadow-sm"
                  >
                    <ArrowRight size={14} />
                  </button>
                </div>
                <span className="text-[10px] text-neutral-400 block">
                  By subscribing you agree with our Privacy Terms.
                </span>
              </form>
            )}
          </div>

        </div>

        {/* Bottom Credits & Payment Badges */}
        <div className="mt-14 pt-8 border-t border-neutral-200/50 dark:border-neutral-800/60 flex flex-col sm:flex-row items-center justify-between text-xs text-neutral-500 dark:text-neutral-400 gap-4">
          <p>© {new Date().getFullYear()} Aura Apparel Haute Co. All rights reserved. MCA Master Project Implementation.</p>
          <div className="flex items-center gap-2 text-neutral-600 dark:text-neutral-400 text-[11px] font-mono">
            <span className="liquid-pill px-2.5 py-0.5 font-bold">VISA</span>
            <span className="liquid-pill px-2.5 py-0.5 font-bold">MASTERCARD</span>
            <span className="liquid-pill px-2.5 py-0.5 font-bold">AMEX</span>
            <span className="liquid-pill px-2.5 py-0.5 font-bold">UPI</span>
            <span className="liquid-pill px-2.5 py-0.5 font-bold">COD</span>
          </div>
        </div>
      </div>
    </footer>
  );
};
