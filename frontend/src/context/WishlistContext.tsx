import React, { createContext, useContext, useState, useEffect } from 'react';
import { WishlistItem } from '../types';
import { api } from '../services/api';
import { useAuth } from './AuthContext';

interface WishlistContextType {
  wishlist: WishlistItem[];
  isLoading: boolean;
  isInWishlist: (productId: number) => boolean;
  toggleWishlist: (productId: number) => Promise<boolean>;
  removeFromWishlist: (productId: number) => Promise<void>;
  refreshWishlist: () => Promise<void>;
}

const WishlistContext = createContext<WishlistContextType | undefined>(undefined);

export const WishlistProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated } = useAuth();
  const [wishlist, setWishlist] = useState<WishlistItem[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const refreshWishlist = async () => {
    if (!isAuthenticated) {
      setWishlist([]);
      return;
    }
    setIsLoading(true);
    try {
      const res = await api.getWishlist();
      setWishlist(res.wishlist || []);
    } catch (err) {
      console.error("Failed to load wishlist:", err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    refreshWishlist();
  }, [isAuthenticated]);

  const isInWishlist = (productId: number): boolean => {
    return wishlist.some(item => item.product_id === productId);
  };

  const toggleWishlist = async (productId: number): Promise<boolean> => {
    if (!isAuthenticated) {
      throw new Error("Please sign in to save items to your wishlist.");
    }
    const res = await api.toggleWishlist(productId);
    await refreshWishlist();
    return res.in_wishlist;
  };

  const removeFromWishlist = async (productId: number) => {
    await api.removeFromWishlist(productId);
    await refreshWishlist();
  };

  return (
    <WishlistContext.Provider value={{
      wishlist,
      isLoading,
      isInWishlist,
      toggleWishlist,
      removeFromWishlist,
      refreshWishlist
    }}>
      {children}
    </WishlistContext.Provider>
  );
};

export const useWishlist = () => {
  const context = useContext(WishlistContext);
  if (!context) {
    throw new Error('useWishlist must be used within a WishlistProvider');
  }
  return context;
};
