export interface User {
  id: number;
  customer_code?: string;
  email: string;
  full_name: string;
  phone?: string;
  role: 'customer' | 'admin';
  is_active: boolean;
  created_at?: string;
}

export interface Address {
  id: number;
  user_id: number;
  full_name: string;
  phone: string;
  address_line1: string;
  address_line2?: string;
  city: string;
  state: string;
  postal_code: string;
  country: string;
  is_default: boolean;
  created_at?: string;
}

export interface Category {
  id: number;
  name: string;
  slug: string;
  description?: string;
  image_url?: string;
  is_featured: boolean;
  product_count?: number;
}

export interface ProductVariant {
  id: number;
  product_id: number;
  size: string;
  color: string;
  color_hex: string;
  sku: string;
  stock_quantity: number;
  additional_price: number;
  in_stock: boolean;
}

export interface ProductImage {
  id: number;
  product_id: number;
  image_url: string;
  color?: string;
  is_primary: boolean;
  display_order: number;
}

export interface Review {
  id: number;
  product_id: number;
  user_id: number;
  user_name: string;
  rating: number;
  title: string;
  comment: string;
  is_verified_purchase: boolean;
  created_at: string;
}

export interface Product {
  id: number;
  name: string;
  slug: string;
  description: string;
  category_id: number;
  category_name?: string;
  category_slug?: string;
  base_price: number;
  discount_price?: number | null;
  effective_price: number;
  brand: string;
  material?: string;
  fit_type?: string;
  care_instructions?: string;
  is_featured: boolean;
  is_active: boolean;
  average_rating: number;
  review_count: number;
  sales_count: number;
  total_stock: number;
  in_stock: boolean;
  primary_image: string;
  images?: ProductImage[];
  variants?: ProductVariant[];
  available_sizes: string[];
  available_colors: Array<{ color: string; color_hex: string; image_url?: string } | string>;
  rating_breakdown?: Record<number, number>;
  recent_reviews?: Review[];
  created_at?: string;
}

export interface CartItem {
  id: number;
  user_id: number;
  variant_id: number;
  quantity: number;
  product_id: number;
  product_name: string;
  product_slug: string;
  primary_image: string;
  size: string;
  color: string;
  color_hex: string;
  sku: string;
  unit_price: number;
  total_price: number;
  stock_available: number;
}

export interface CartSummary {
  item_count: number;
  subtotal: number;
  tax: number;
  shipping: number;
  free_shipping_threshold: number;
  qualifies_for_free_shipping: boolean;
  total: number;
}

export interface WishlistItem {
  id: number;
  user_id: number;
  product_id: number;
  product: Product;
  created_at: string;
}

export interface Coupon {
  id: number;
  code: string;
  discount_type: 'percentage' | 'fixed';
  discount_value: number;
  min_order_amount: number;
  max_discount_amount?: number;
  usage_limit: number;
  times_used: number;
  valid_from?: string;
  valid_to?: string;
  is_active: boolean;
}

export interface OrderItem {
  id: number;
  order_id: number;
  product_id?: number;
  variant_id?: number;
  product_name: string;
  variant_size: string;
  variant_color: string;
  sku?: string;
  image_url?: string;
  unit_price: number;
  quantity: number;
  total_price: number;
}

export interface ReturnRequest {
  id: number;
  order_id: number;
  order_number?: string;
  user_id: number;
  customer_name?: string;
  customer_email?: string;
  customer_code?: string;
  request_type: 'cancellation' | 'return' | 'refund';
  reason: string;
  customer_notes?: string;
  status: 'pending' | 'approved' | 'rejected';
  admin_notes?: string;
  created_at: string;
  updated_at?: string;
}

export interface Order {
  id: number;
  order_number: string;
  user_id: number;
  customer_name?: string;
  customer_email?: string;
  customer_code?: string;
  address_id?: number;
  delivery_address?: Address;
  coupon_code?: string;
  subtotal: number;
  discount_amount: number;
  shipping_amount: number;
  tax_amount: number;
  total_amount: number;
  status: 'pending' | 'processing' | 'shipped' | 'delivered' | 'cancelled';
  payment_status: 'pending' | 'paid' | 'failed' | 'refunded';
  payment_method: string;
  tracking_number?: string;
  carrier_name?: string;
  notes?: string;
  created_at: string;
  updated_at?: string;
  item_count?: number;
  items?: OrderItem[];
  return_requests?: ReturnRequest[];
}

export interface Notification {
  id: number;
  user_id: number;
  title: string;
  message: string;
  type: 'order' | 'promo' | 'account' | 'system';
  is_read: boolean;
  link_url?: string;
  created_at: string;
}

export interface RecommendationResult {
  product: Product;
  score: number;
  breakdown?: {
    category_score?: number;
    price_score?: number;
    rating_score?: number;
    popularity_score?: number;
  };
}

export interface AdminMetrics {
  overview: {
    total_revenue: number;
    total_orders: number;
    total_customers: number;
    total_products: number;
    low_stock_count: number;
    pending_requests_count: number;
  };
  status_breakdown: Record<string, number>;
  recent_orders: Order[];
}
