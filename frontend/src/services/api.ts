const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || (import.meta.env.PROD ? '/api' : 'http://localhost:5000/api');

async function request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const token = localStorage.getItem('aura_token');
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...(options.headers || {})
  };

  // 6-second timeout to prevent requests from hanging indefinitely
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 6000);

  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers,
      signal: controller.signal
    });
    clearTimeout(timeoutId);

    const data = await response.json().catch(() => ({}));

    if (!response.ok) {
      const errorMsg = data.error || data.message || `Request failed with status ${response.status}`;
      throw new Error(errorMsg);
    }

    return data as T;
  } catch (err: any) {
    clearTimeout(timeoutId);
    if (err.name === 'AbortError') {
      throw new Error('Connection timed out. The backend server on port 5000 is not responding.');
    }
    if (err.message && (err.message.includes('Failed to fetch') || err.message.includes('NetworkError'))) {
      throw new Error('Cannot connect to backend API on port 5000. Please start the backend server.');
    }
    throw err;
  }
}

export const api = {
  // Auth
  register: (body: any) => request<any>('/auth/register', { method: 'POST', body: JSON.stringify(body) }),
  login: (body: any) => request<any>('/auth/login', { method: 'POST', body: JSON.stringify(body) }),
  getProfile: () => request<any>('/auth/profile'),
  updateProfile: (body: any) => request<any>('/auth/profile', { method: 'PUT', body: JSON.stringify(body) }),
  changePassword: (body: any) => request<any>('/auth/change-password', { method: 'PUT', body: JSON.stringify(body) }),

  // Products & Categories
  getCategories: () => request<{ categories: any[] }>('/categories'),
  getProducts: (params: string = '') => request<any>(`/products${params ? `?${params}` : ''}`),
  getProduct: (id: number | string) => request<{ product: any }>(`/products/${id}`),
  getProductRecommendations: (id: number | string) => request<any>(`/products/${id}/recommendations`),
  getPersonalizedRecommendations: () => request<any>('/recommendations/personalized'),
  getTrendingProducts: () => request<any>('/recommendations/trending'),

  // Cart
  getCart: () => request<{ items: any[]; summary: any }>('/cart'),
  addToCart: (variant_id: number, quantity: number = 1) => 
    request<any>('/cart', { method: 'POST', body: JSON.stringify({ variant_id, quantity }) }),
  updateCartItem: (id: number, quantity: number) => 
    request<any>(`/cart/${id}`, { method: 'PUT', body: JSON.stringify({ quantity }) }),
  removeCartItem: (id: number) => 
    request<any>(`/cart/${id}`, { method: 'DELETE' }),
  clearCart: () => request<any>('/cart', { method: 'DELETE' }),

  // Wishlist
  getWishlist: () => request<{ wishlist: any[] }>('/wishlist'),
  toggleWishlist: (product_id: number) => 
    request<any>('/wishlist/toggle', { method: 'POST', body: JSON.stringify({ product_id }) }),
  removeFromWishlist: (product_id: number) => 
    request<any>(`/wishlist/${product_id}`, { method: 'DELETE' }),

  // Delivery Addresses
  getAddresses: () => request<{ addresses: any[] }>('/addresses'),
  addAddress: (body: any) => request<any>('/addresses', { method: 'POST', body: JSON.stringify(body) }),
  updateAddress: (id: number, body: any) => request<any>(`/addresses/${id}`, { method: 'PUT', body: JSON.stringify(body) }),
  setDefaultAddress: (id: number) => request<any>(`/addresses/${id}/set-default`, { method: 'PUT' }),
  deleteAddress: (id: number) => request<any>(`/addresses/${id}`, { method: 'DELETE' }),

  // Coupons
  validateCoupon: (code: string, subtotal: number) => 
    request<any>('/coupons/validate', { method: 'POST', body: JSON.stringify({ code, subtotal }) }),
  getActiveCoupons: () => request<{ coupons: any[] }>('/coupons/active'),

  // Orders
  getOrders: () => request<{ orders: any[] }>('/orders'),
  getOrder: (id: number | string) => request<{ order: any }>(`/orders/${id}`),
  createOrder: (body: any) => request<any>('/orders', { method: 'POST', body: JSON.stringify(body) }),
  cancelOrder: (id: number, reason: string) => 
    request<any>(`/orders/${id}/cancel`, { method: 'POST', body: JSON.stringify({ reason }) }),
  submitReturnRequest: (id: number, body: { request_type: string; reason: string; customer_notes?: string }) => 
    request<any>(`/orders/${id}/return-request`, { method: 'POST', body: JSON.stringify(body) }),
  getOrderInvoice: (id: number) => request<any>(`/orders/${id}/invoice`),

  // Reviews
  getProductReviews: (product_id: number) => request<any>(`/products/${product_id}/reviews`),
  addProductReview: (product_id: number, body: { rating: number; title: string; comment: string }) => 
    request<any>(`/products/${product_id}/reviews`, { method: 'POST', body: JSON.stringify(body) }),

  // Notifications
  getNotifications: () => request<{ notifications: any[]; unread_count: number }>('/notifications'),
  markNotificationRead: (id: number) => request<any>(`/notifications/${id}/read`, { method: 'PUT' }),
  markAllNotificationsRead: () => request<any>('/notifications/read-all', { method: 'PUT' }),

  // Admin
  getAdminMetrics: () => request<any>('/admin/metrics'),
  getAdminProducts: (params: string = '') => request<any>(`/admin/products${params ? `?${params}` : ''}`),
  createAdminProduct: (body: any) => request<any>('/admin/products', { method: 'POST', body: JSON.stringify(body) }),
  updateAdminProduct: (id: number, body: any) => request<any>(`/admin/products/${id}`, { method: 'PUT', body: JSON.stringify(body) }),
  deleteAdminProduct: (id: number) => request<any>(`/admin/products/${id}`, { method: 'DELETE' }),
  getAdminInventory: () => request<any>('/admin/inventory'),
  updateAdminStock: (variantId: number, body: any) => request<any>(`/admin/inventory/${variantId}`, { method: 'PUT', body: JSON.stringify(body) }),
  addAdminVariant: (productId: number, body: any) => request<any>(`/admin/products/${productId}/variants`, { method: 'POST', body: JSON.stringify(body) }),
  createAdminCategory: (body: any) => request<any>('/admin/categories', { method: 'POST', body: JSON.stringify(body) }),
  getAdminCoupons: () => request<any>('/admin/coupons'),
  createAdminCoupon: (body: any) => request<any>('/admin/coupons', { method: 'POST', body: JSON.stringify(body) }),
  getAdminOrders: (params: string = '') => request<any>(`/admin/orders${params ? `?${params}` : ''}`),
  updateAdminOrderStatus: (id: number, body: any) => request<any>(`/admin/orders/${id}/status`, { method: 'PUT', body: JSON.stringify(body) }),
  getAdminRequests: () => request<any>('/admin/requests'),
  processAdminRequest: (id: number, body: any) => request<any>(`/admin/requests/${id}`, { method: 'PUT', body: JSON.stringify(body) }),
  getAdminCustomers: () => request<any>('/admin/customers'),

  // AI Atelier Suite
  askAIConcierge: (messages: { role: string; content: string }[], image?: string) =>
    request<{ reply: string; recommended_products: any[]; model?: string; status: string }>('/ai/concierge', {
      method: 'POST',
      body: JSON.stringify({ messages, image })
    }),
  generateEditorialCopy: (name: string, material: string, category_name: string) =>
    request<{ description: string; status: string }>('/ai/editorial-copy', {
      method: 'POST',
      body: JSON.stringify({ name, material, category_name })
    }),
  askFabricAdvisor: (product_id: number, question: string) =>
    request<{ answer: string; status: string }>('/ai/fabric-advisor', {
      method: 'POST',
      body: JSON.stringify({ product_id, question })
    })
};
