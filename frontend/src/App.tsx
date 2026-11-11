import React, { useEffect } from 'react';
import { BrowserRouter, Routes, Route, useLocation } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { ThemeProvider } from './context/ThemeContext';
import { CartProvider } from './context/CartContext';
import { WishlistProvider } from './context/WishlistContext';
import { NotificationProvider } from './context/NotificationContext';

import { Navbar } from './components/common/Navbar';
import { Footer } from './components/common/Footer';
import { HomePage } from './pages/HomePage';
import { ProductListPage } from './pages/ProductListPage';
import { ProductDetailPage } from './pages/ProductDetailPage';
import { CartPage } from './pages/CartPage';
import { CheckoutPage } from './pages/CheckoutPage';
import { OrderConfirmationPage } from './pages/OrderConfirmationPage';
import { OrderHistoryPage } from './pages/OrderHistoryPage';
import { WishlistPage } from './pages/WishlistPage';
import { ProfilePage } from './pages/ProfilePage';
import { AuthPage } from './pages/AuthPage';
import { AdminDashboard } from './pages/AdminDashboard';
import { AdminRoute } from './components/admin/AdminRoute';
import { ProtectedRoute } from './components/common/ProtectedRoute';
import { AIConciergeModal } from './components/ai/AIConciergeModal';

// Scroll to top helper
const ScrollToTop: React.FC = () => {
  const { pathname } = useLocation();
  useEffect(() => {
    window.scrollTo(0, 0);
  }, [pathname]);
  return null;
};

// Liquid Background Ambient Lighting
const LiquidAtmosphere: React.FC = () => {
  return (
    <div className="fixed inset-0 overflow-hidden pointer-events-none -z-10 select-none">
      {/* Orb 1: Champagne Gold Aura */}
      <div className="absolute -top-32 -right-32 w-[600px] h-[600px] rounded-full bg-gradient-to-br from-amber-300/20 via-aura-gold/25 to-yellow-100/10 dark:from-aura-gold/15 dark:via-amber-600/10 dark:to-transparent blur-[120px] animate-float-slow" />
      
      {/* Orb 2: Ethereal Sapphire & Iridescent Crystal */}
      <div className="absolute top-[35%] -left-40 w-[550px] h-[550px] rounded-full bg-gradient-to-tr from-sky-300/15 via-indigo-200/10 to-teal-100/10 dark:from-indigo-900/25 dark:via-sky-950/20 dark:to-transparent blur-[130px] animate-float-reverse" />
      
      {/* Orb 3: Soft Rose Champagne & Warm Amber */}
      <div className="absolute top-[70%] -right-24 w-[500px] h-[500px] rounded-full bg-gradient-to-tl from-rose-300/15 via-orange-200/15 to-amber-100/10 dark:from-rose-950/20 dark:via-amber-950/15 dark:to-transparent blur-[120px] animate-pulse-glow" />

      {/* Subtle Liquid Noise Texture Overlay */}
      <div className="absolute inset-0 opacity-[0.02] dark:opacity-[0.035] bg-[radial-gradient(#C5A059_1px,transparent_1px)] [background-size:24px_24px]" />
    </div>
  );
};

export const App: React.FC = () => {
  return (
    <ThemeProvider>
      <AuthProvider>
        <CartProvider>
          <WishlistProvider>
            <NotificationProvider>
              <BrowserRouter>
                <ScrollToTop />
                <div className="relative flex flex-col min-h-screen w-full max-w-full overflow-x-hidden bg-[#FAF7F2] dark:bg-[#0C0B0A] text-neutral-900 dark:text-neutral-100 transition-colors duration-300">
                  <LiquidAtmosphere />
                  <Navbar />
                  <main className="flex-1 relative z-10">
                    <Routes>
                      <Route path="/" element={<HomePage />} />
                      <Route path="/products" element={<ProductListPage />} />
                      <Route path="/products/:id" element={<ProductDetailPage />} />
                      <Route path="/cart" element={<CartPage />} />
                      <Route 
                        path="/checkout" 
                        element={
                          <ProtectedRoute>
                            <CheckoutPage />
                          </ProtectedRoute>
                        } 
                      />
                      <Route path="/order-confirmation/:id" element={<OrderConfirmationPage />} />
                      <Route 
                        path="/orders" 
                        element={
                          <ProtectedRoute>
                            <OrderHistoryPage />
                          </ProtectedRoute>
                        } 
                      />
                      <Route path="/wishlist" element={<WishlistPage />} />
                      <Route 
                        path="/profile" 
                        element={
                          <ProtectedRoute>
                            <ProfilePage />
                          </ProtectedRoute>
                        } 
                      />
                      <Route path="/auth" element={<AuthPage />} />
                      
                      {/* Access-Controlled Protected Admin Routes */}
                      <Route
                        path="/admin/*"
                        element={
                          <AdminRoute>
                            <AdminDashboard />
                          </AdminRoute>
                        }
                      />
                    </Routes>
                  </main>
                  <Footer />
                  <AIConciergeModal />
                </div>
              </BrowserRouter>
            </NotificationProvider>
          </WishlistProvider>
        </CartProvider>
      </AuthProvider>
    </ThemeProvider>
  );
};

export default App;
