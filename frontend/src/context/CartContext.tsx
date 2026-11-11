import React, { createContext, useContext, useState, useEffect } from 'react';
import { CartItem, CartSummary } from '../types';
import { api } from '../services/api';
import { useAuth } from './AuthContext';

interface CartContextType {
  items: CartItem[];
  summary: CartSummary;
  isLoading: boolean;
  appliedCoupon: {
    code: string;
    discount_amount: number;
    discount_value: number;
    discount_type: string;
  } | null;
  addToCart: (variant_id: number, quantity?: number) => Promise<void>;
  updateQuantity: (id: number, quantity: number) => Promise<void>;
  removeItem: (id: number) => Promise<void>;
  clearCart: () => Promise<void>;
  applyCoupon: (code: string) => Promise<{ success: boolean; message: string }>;
  removeCoupon: () => void;
  refreshCart: () => Promise<void>;
}

const CartContext = createContext<CartContextType | undefined>(undefined);

const initialSummary: CartSummary = {
  item_count: 0,
  subtotal: 0,
  tax: 0,
  shipping: 0,
  free_shipping_threshold: 100,
  qualifies_for_free_shipping: false,
  total: 0
};

export const CartProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated } = useAuth();
  const [items, setItems] = useState<CartItem[]>([]);
  const [summary, setSummary] = useState<CartSummary>(initialSummary);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [appliedCoupon, setAppliedCoupon] = useState<{
    code: string;
    discount_amount: number;
    discount_value: number;
    discount_type: string;
  } | null>(null);

  const refreshCart = async () => {
    if (!isAuthenticated) {
      setItems([]);
      setSummary(initialSummary);
      setAppliedCoupon(null);
      return;
    }
    setIsLoading(true);
    try {
      const res = await api.getCart();
      setItems(res.items || []);
      let sum = res.summary || initialSummary;

      // Adjust total if coupon is active
      if (appliedCoupon && sum.subtotal > 0) {
        const discount = appliedCoupon.discount_type === 'percentage' 
          ? (appliedCoupon.discount_value / 100) * sum.subtotal 
          : Math.min(appliedCoupon.discount_value, sum.subtotal);
        const newTax = Math.round((Math.max(0, sum.subtotal - discount) * 0.08) * 100) / 100;
        const newTotal = Math.round((Math.max(0, sum.subtotal - discount) + newTax + sum.shipping) * 100) / 100;
        sum = {
          ...sum,
          tax: newTax,
          total: newTotal
        };
      }

      setSummary(sum);
    } catch (err) {
      console.error("Failed to fetch cart:", err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    refreshCart();
  }, [isAuthenticated]);

  const addToCart = async (variant_id: number, quantity: number = 1) => {
    if (!isAuthenticated) {
      throw new Error("Please log in to add items to your shopping bag.");
    }
    await api.addToCart(variant_id, quantity);
    await refreshCart();
  };

  const updateQuantity = async (id: number, quantity: number) => {
    await api.updateCartItem(id, quantity);
    await refreshCart();
  };

  const removeItem = async (id: number) => {
    await api.removeCartItem(id);
    await refreshCart();
  };

  const clearCart = async () => {
    await api.clearCart();
    setItems([]);
    setSummary(initialSummary);
    setAppliedCoupon(null);
  };

  const applyCoupon = async (code: string): Promise<{ success: boolean; message: string }> => {
    try {
      const res = await api.validateCoupon(code, summary.subtotal);
      if (res.valid) {
        setAppliedCoupon({
          code: res.coupon.code,
          discount_amount: res.coupon.discount_amount,
          discount_value: res.coupon.discount_value,
          discount_type: res.coupon.discount_type
        });
        // Recalculate
        const newTax = Math.round((Math.max(0, summary.subtotal - res.coupon.discount_amount) * 0.08) * 100) / 100;
        const newTotal = Math.round((Math.max(0, summary.subtotal - res.coupon.discount_amount) + newTax + summary.shipping) * 100) / 100;
        setSummary(prev => ({
          ...prev,
          tax: newTax,
          total: newTotal
        }));
        return { success: true, message: res.message };
      } else {
        return { success: false, message: res.message || 'Invalid coupon' };
      }
    } catch (err: any) {
      return { success: false, message: err.message || 'Failed to apply coupon' };
    }
  };

  const removeCoupon = () => {
    setAppliedCoupon(null);
    refreshCart();
  };

  return (
    <CartContext.Provider value={{
      items,
      summary,
      isLoading,
      appliedCoupon,
      addToCart,
      updateQuantity,
      removeItem,
      clearCart,
      applyCoupon,
      removeCoupon,
      refreshCart
    }}>
      {children}
    </CartContext.Provider>
  );
};

export const useCart = () => {
  const context = useContext(CartContext);
  if (!context) {
    throw new Error('useCart must be used within a CartProvider');
  }
  return context;
};
