import React, { useState, useEffect } from 'react';
import { 
  BarChart3, Package, Layers, Ticket, ShoppingCart, 
  RotateCcw, Users, AlertTriangle, Plus, Search, 
  Check, X, Edit, Trash2, ArrowUpRight, ShieldCheck, 
  Truck, DollarSign, Filter, RefreshCw, Sparkles
} from 'lucide-react';
import { api } from '../services/api';
import { 
  AdminMetrics, Product, Order, ReturnRequest, 
  Category, Coupon 
} from '../types';
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import { ImageWithFallback } from '../components/common/ImageWithFallback';
import { formatPrice } from '../utils/formatters';

export const AdminDashboard: React.FC = () => {
  const [activeTab, setActiveTab] = useState<
    'overview' | 'products' | 'inventory' | 'orders' | 'requests' | 'coupons' | 'categories' | 'customers'
  >('overview');

  const [metrics, setMetrics] = useState<AdminMetrics | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [feedback, setFeedback] = useState<{ type: 'success' | 'error'; message: string } | null>(null);

  // Products Tab State
  const [products, setProducts] = useState<Product[]>([]);
  const [productSearch, setProductSearch] = useState('');
  const [showProductModal, setShowProductModal] = useState(false);
  const [editingProduct, setEditingProduct] = useState<Product | null>(null);
  const [productForm, setProductForm] = useState({
    name: '',
    category_id: 1,
    base_price: 100,
    discount_price: '',
    description: '',
    brand: 'Aura Apparel',
    material: '100% Mulberry Silk',
    fit_type: 'Regular',
    is_featured: false,
    image_url: 'https://images.unsplash.com/photo-1595777457583-95e059d581b8?auto=format&fit=crop&w=800&q=80'
  });

  // AI Editorial Copilot State
  const [isGeneratingCopy, setIsGeneratingCopy] = useState<boolean>(false);

  const handleGenerateEditorialCopy = async () => {
    if (!productForm.name) {
      setFeedback({ type: 'error', message: 'Please provide a Garment Name before generating editorial copy.' });
      return;
    }
    setIsGeneratingCopy(true);
    try {
      const selectedCat = categories.find(c => c.id === Number(productForm.category_id));
      const categoryName = selectedCat ? selectedCat.name : 'Haute Couture';
      const res = await api.generateEditorialCopy(
        productForm.name,
        productForm.material || 'Natural Luxury Fibers',
        categoryName
      );
      if (res && res.description) {
        setProductForm(prev => ({ ...prev, description: res.description }));
        setFeedback({ type: 'success', message: 'Editorial copy drafted by Gemini AI Copilot.' });
      }
    } catch (err: any) {
      setFeedback({ type: 'error', message: err.message || 'Failed to craft editorial copy.' });
    } finally {
      setIsGeneratingCopy(false);
    }
  };

  // Inventory Tab State
  const [inventoryList, setInventoryList] = useState<any[]>([]);
  const [stockEditVariant, setStockEditVariant] = useState<any | null>(null);
  const [stockInput, setStockInput] = useState<number>(0);

  // Orders Tab State
  const [orders, setOrders] = useState<Order[]>([]);
  const [orderStatusFilter, setOrderStatusFilter] = useState('');
  const [selectedOrderForStatus, setSelectedOrderForStatus] = useState<Order | null>(null);
  const [newStatus, setNewStatus] = useState<string>('shipped');
  const [trackingNumber, setTrackingNumber] = useState<string>('');
  const [carrierName, setCarrierName] = useState<string>('Aura Express Logistics');

  // Return Requests State
  const [returnRequests, setReturnRequests] = useState<ReturnRequest[]>([]);
  const [processingReq, setProcessingReq] = useState<ReturnRequest | null>(null);
  const [adminNotes, setAdminNotes] = useState<string>('');

  // Coupons State
  const [coupons, setCoupons] = useState<Coupon[]>([]);
  const [showCouponModal, setShowCouponModal] = useState(false);
  const [couponForm, setCouponForm] = useState({
    code: '',
    discount_type: 'percentage',
    discount_value: 15,
    min_order_amount: 50,
    max_discount_amount: '',
    usage_limit: 500
  });

  // Categories State
  const [categories, setCategories] = useState<Category[]>([]);
  const [showCategoryModal, setShowCategoryModal] = useState(false);
  const [categoryForm, setCategoryForm] = useState({
    name: '',
    description: '',
    image_url: 'https://images.unsplash.com/photo-1595777457583-95e059d581b8?auto=format&fit=crop&w=800&q=80',
    is_featured: false
  });

  // Customers State
  const [customers, setCustomers] = useState<any[]>([]);

  // Load Main Metrics
  const loadDashboardData = async () => {
    setIsLoading(true);
    try {
      const [metricRes, catRes] = await Promise.all([
        api.getAdminMetrics(),
        api.getCategories()
      ]);
      setMetrics(metricRes);
      setCategories(catRes.categories || []);
    } catch (err) {
      console.error("Failed to load admin metrics:", err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadDashboardData();
  }, []);

  // Lazy-load Tab Data
  useEffect(() => {
    const loadTabData = async () => {
      try {
        if (activeTab === 'products') {
          const res = await api.getAdminProducts();
          setProducts(res.products || []);
        } else if (activeTab === 'inventory') {
          const res = await api.getAdminInventory();
          setInventoryList(res.inventory || []);
        } else if (activeTab === 'orders') {
          const res = await api.getAdminOrders(orderStatusFilter ? `status=${orderStatusFilter}` : '');
          setOrders(res.orders || []);
        } else if (activeTab === 'requests') {
          const res = await api.getAdminRequests();
          setReturnRequests(res.requests || []);
        } else if (activeTab === 'coupons') {
          const res = await api.getAdminCoupons();
          setCoupons(res.coupons || []);
        } else if (activeTab === 'customers') {
          const res = await api.getAdminCustomers();
          setCustomers(res.customers || []);
        }
      } catch (err: any) {
        setFeedback({ type: 'error', message: err.message || 'Failed to fetch tab data' });
      }
    };

    loadTabData();
  }, [activeTab, orderStatusFilter]);

  // Product CRUD
  const handleSaveProduct = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const payload: any = {
        ...productForm,
        category_id: Number(productForm.category_id),
        base_price: Number(productForm.base_price),
        discount_price: productForm.discount_price ? Number(productForm.discount_price) : null
      };

      if (editingProduct) {
        await api.updateAdminProduct(editingProduct.id, payload);
        setFeedback({ type: 'success', message: 'Product updated successfully' });
      } else {
        await api.createAdminProduct(payload);
        setFeedback({ type: 'success', message: 'New product added to catalogue' });
      }
      setShowProductModal(false);
      setEditingProduct(null);
      const res = await api.getAdminProducts();
      setProducts(res.products || []);
      loadDashboardData();
    } catch (err: any) {
      setFeedback({ type: 'error', message: err.message || 'Failed to save product' });
    }
  };

  const handleDeleteProduct = async (id: number) => {
    if (window.confirm("Are you sure you want to delete this product? All related variants will be removed.")) {
      try {
        await api.deleteAdminProduct(id);
        setFeedback({ type: 'success', message: 'Product deleted from catalogue' });
        setProducts(products.filter(p => p.id !== id));
        loadDashboardData();
      } catch (err: any) {
        setFeedback({ type: 'error', message: err.message || 'Failed to delete product' });
      }
    }
  };

  // Stock Update
  const handleUpdateStock = async () => {
    if (!stockEditVariant) return;
    try {
      await api.updateAdminStock(stockEditVariant.id, { stock_quantity: stockInput });
      setFeedback({ type: 'success', message: `Stock for ${stockEditVariant.sku} updated to ${stockInput}` });
      setStockEditVariant(null);
      const res = await api.getAdminInventory();
      setInventoryList(res.inventory || []);
      loadDashboardData();
    } catch (err: any) {
      setFeedback({ type: 'error', message: err.message || 'Failed to update stock' });
    }
  };

  // Order Status Update
  const handleUpdateOrderStatus = async () => {
    if (!selectedOrderForStatus) return;
    try {
      await api.updateAdminOrderStatus(selectedOrderForStatus.id, {
        status: newStatus,
        tracking_number: trackingNumber,
        carrier_name: carrierName
      });
      setFeedback({ type: 'success', message: `Order ${selectedOrderForStatus.order_number} marked as ${newStatus}` });
      setSelectedOrderForStatus(null);
      const res = await api.getAdminOrders(orderStatusFilter ? `status=${orderStatusFilter}` : '');
      setOrders(res.orders || []);
      loadDashboardData();
    } catch (err: any) {
      setFeedback({ type: 'error', message: err.message || 'Failed to update order status' });
    }
  };

  // Process Return/Refund Request
  const handleProcessRequest = async (action: 'approve' | 'reject') => {
    if (!processingReq) return;
    try {
      await api.processAdminRequest(processingReq.id, {
        action,
        admin_notes: adminNotes
      });
      setFeedback({ type: 'success', message: `Request has been ${action}d.` });
      setProcessingReq(null);
      setAdminNotes('');
      const res = await api.getAdminRequests();
      setReturnRequests(res.requests || []);
      loadDashboardData();
    } catch (err: any) {
      setFeedback({ type: 'error', message: err.message || 'Failed to process request' });
    }
  };

  // Coupon Creation
  const handleCreateCoupon = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await api.createAdminCoupon({
        ...couponForm,
        discount_value: Number(couponForm.discount_value),
        min_order_amount: Number(couponForm.min_order_amount),
        max_discount_amount: couponForm.max_discount_amount ? Number(couponForm.max_discount_amount) : null,
        usage_limit: Number(couponForm.usage_limit)
      });
      setFeedback({ type: 'success', message: `Coupon code '${couponForm.code}' published` });
      setShowCouponModal(false);
      setCouponForm({
        code: '',
        discount_type: 'percentage',
        discount_value: 15,
        min_order_amount: 50,
        max_discount_amount: '',
        usage_limit: 500
      });
      const res = await api.getAdminCoupons();
      setCoupons(res.coupons || []);
    } catch (err: any) {
      setFeedback({ type: 'error', message: err.message || 'Failed to create coupon' });
    }
  };

  // Category Creation
  const handleCreateCategory = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await api.createAdminCategory(categoryForm);
      setFeedback({ type: 'success', message: `Category '${categoryForm.name}' created` });
      setShowCategoryModal(false);
      const res = await api.getCategories();
      setCategories(res.categories || []);
    } catch (err: any) {
      setFeedback({ type: 'error', message: err.message || 'Failed to create category' });
    }
  };

  if (isLoading && !metrics) {
    return <LoadingSpinner fullPage message="Loading Atelier Administration Center..." />;
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12">
      {/* Admin Title Bar */}
      <div className="flex flex-col md:flex-row md:items-center justify-between pb-6 border-b border-neutral-200/60 dark:border-neutral-800/60 gap-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-xs uppercase tracking-widest text-aura-gold font-bold flex items-center gap-1">
              <ShieldCheck size={14} /> Aura Master Control
            </span>
            <span className="text-neutral-300 dark:text-neutral-700">•</span>
            <span className="text-xs text-neutral-400">Atelier Administration</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-serif font-bold text-neutral-900 dark:text-neutral-100 mt-1">
            Catalogue, Inventory & Order Management
          </h1>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={() => { loadDashboardData(); }}
            className="px-4 py-2 liquid-pill text-xs font-bold text-neutral-800 dark:text-neutral-200 flex items-center gap-1.5 transition-all shadow-sm"
          >
            <RefreshCw size={13} />
            <span>Sync Stats</span>
          </button>
        </div>
      </div>

      {/* Global Feedback Banner */}
      {feedback && (
        <div className={`my-4 p-4 rounded-xl text-xs flex items-center justify-between ${
          feedback.type === 'success' 
            ? 'bg-emerald-50 dark:bg-emerald-950/60 text-emerald-800 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-900/50' 
            : 'bg-red-50 dark:bg-red-950/60 text-red-800 dark:text-red-300 border border-red-200 dark:border-red-900/50'
        }`}>
          <span className="font-medium">{feedback.message}</span>
          <button onClick={() => setFeedback(null)} className="text-neutral-500 hover:text-neutral-900 dark:hover:text-white"><X size={14} /></button>
        </div>
      )}

      {/* Tab Navigation Ribbon */}
      <div className="flex overflow-x-auto border-b border-neutral-200 dark:border-neutral-800 mt-6 text-xs font-bold uppercase tracking-wider space-x-1">
        {[
          { id: 'overview', label: 'Metrics & KPI', icon: BarChart3 },
          { id: 'products', label: 'Catalogue', icon: Package },
          { id: 'inventory', label: 'Inventory Stock', icon: Layers, badge: metrics?.overview?.low_stock_count },
          { id: 'orders', label: 'Customer Orders', icon: ShoppingCart },
          { id: 'requests', label: 'Returns & Cancellations', icon: RotateCcw, badge: metrics?.overview?.pending_requests_count },
          { id: 'coupons', label: 'Vouchers & Promos', icon: Ticket },
          { id: 'categories', label: 'Categories', icon: Layers },
          { id: 'customers', label: 'Patrons Directory', icon: Users },
        ].map((tab) => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`py-3 px-4 border-b-2 font-semibold flex items-center gap-2 whitespace-nowrap transition-all rounded-t-xl ${
                isActive 
                  ? 'border-neutral-900 dark:border-aura-gold text-neutral-900 dark:text-aura-gold bg-neutral-100/80 dark:bg-neutral-900/80 shadow-xs' 
                  : 'border-transparent text-neutral-500 dark:text-neutral-400 hover:text-neutral-800 dark:hover:text-neutral-200 hover:border-neutral-300 dark:hover:border-neutral-700'
              }`}
            >
              <Icon size={14} />
              <span>{tab.label}</span>
              {tab.badge !== undefined && tab.badge > 0 && (
                <span className="px-1.5 py-0.2 bg-red-500 text-white text-[10px] rounded-full font-bold">
                  {tab.badge}
                </span>
              )}
            </button>
          );
        })}
      </div>

      {/* TAB CONTENT AREA */}
      <div className="mt-8">
        
        {/* ========================================================= */}
        {/* TAB 1: OVERVIEW & KPIS */}
        {/* ========================================================= */}
        {activeTab === 'overview' && metrics && (
          <div className="space-y-8">
            {/* 6 Key Metric Cards */}
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
              <div className="liquid-glass p-5 rounded-2xl border border-white/70 dark:border-white/10 shadow-md">
                <span className="text-[10px] uppercase tracking-wider text-neutral-400 font-bold">Total Revenue</span>
                <p className="text-2xl font-serif font-bold text-neutral-900 dark:text-neutral-100 mt-1">
                  {formatPrice(metrics.overview.total_revenue)}
                </p>
                <span className="text-[11px] text-emerald-600 dark:text-emerald-400 font-medium">Delivered / Active</span>
              </div>

              <div className="liquid-glass p-5 rounded-2xl border border-white/70 dark:border-white/10 shadow-md">
                <span className="text-[10px] uppercase tracking-wider text-neutral-400 font-bold">Total Orders</span>
                <p className="text-2xl font-serif font-bold text-neutral-900 dark:text-neutral-100 mt-1">
                  {metrics.overview.total_orders}
                </p>
                <span className="text-[11px] text-neutral-500 dark:text-neutral-400">Across all statuses</span>
              </div>

              <div className="liquid-glass p-5 rounded-2xl border border-white/70 dark:border-white/10 shadow-md">
                <span className="text-[10px] uppercase tracking-wider text-neutral-400 font-bold">Total Customers</span>
                <p className="text-2xl font-serif font-bold text-neutral-900 dark:text-neutral-100 mt-1">
                  {metrics.overview.total_customers}
                </p>
                <span className="text-[11px] text-neutral-500 dark:text-neutral-400">Registered Patrons</span>
              </div>

              <div className="liquid-glass p-5 rounded-2xl border border-white/70 dark:border-white/10 shadow-md">
                <span className="text-[10px] uppercase tracking-wider text-neutral-400 font-bold">Catalogue Items</span>
                <p className="text-2xl font-serif font-bold text-neutral-900 dark:text-neutral-100 mt-1">
                  {metrics.overview.total_products}
                </p>
                <span className="text-[11px] text-neutral-500 dark:text-neutral-400">Garment Designs</span>
              </div>

              <div className="liquid-glass p-5 rounded-2xl border border-white/70 dark:border-white/10 shadow-md">
                <span className="text-[10px] uppercase tracking-wider text-neutral-400 font-bold">Low Stock Alert</span>
                <p className="text-2xl font-serif font-bold text-red-600 dark:text-red-400 mt-1">
                  {metrics.overview.low_stock_count}
                </p>
                <span className="text-[11px] text-red-500 dark:text-red-400">Under 10 units</span>
              </div>

              <div className="liquid-glass p-5 rounded-2xl border border-white/70 dark:border-white/10 shadow-md">
                <span className="text-[10px] uppercase tracking-wider text-neutral-400 font-bold">Pending Returns</span>
                <p className="text-2xl font-serif font-bold text-amber-600 dark:text-amber-400 mt-1">
                  {metrics.overview.pending_requests_count}
                </p>
                <span className="text-[11px] text-amber-600 dark:text-amber-400">Awaiting Approval</span>
              </div>
            </div>

            {/* Order Status Distribution Bar */}
            <div className="liquid-glass p-6 sm:p-8 rounded-3xl border border-white/70 dark:border-white/10 shadow-xl space-y-4">
              <h3 className="font-serif font-bold text-base text-neutral-900 dark:text-neutral-100">
                Order Pipeline & Status Distribution
              </h3>
              <div className="grid grid-cols-2 sm:grid-cols-5 gap-3 pt-2 text-xs">
                {Object.entries(metrics.status_breakdown).map(([status, count]) => (
                  <div key={status} className="p-3 bg-neutral-50/70 dark:bg-neutral-900/80 rounded-xl border border-neutral-200/60 dark:border-neutral-800">
                    <span className="uppercase text-[10px] font-bold tracking-wider text-neutral-500 dark:text-neutral-400 block">
                      {status}
                    </span>
                    <span className="text-xl font-serif font-bold text-neutral-900 dark:text-neutral-100 mt-0.5 block">
                      {count}
                    </span>
                  </div>
                ))}
              </div>
            </div>

            {/* Recent Orders Preview */}
            <div className="liquid-glass rounded-2xl border border-white/70 dark:border-white/10 shadow-lg p-6 space-y-4">
              <div className="flex items-center justify-between pb-3 border-b border-neutral-200/60 dark:border-neutral-800">
                <h3 className="font-serif font-bold text-base text-neutral-900 dark:text-neutral-100">
                  Recent Customer Orders
                </h3>
                <button
                  onClick={() => setActiveTab('orders')}
                  className="text-xs text-aura-gold hover:underline font-semibold"
                >
                  View All Orders →
                </button>
              </div>

              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs">
                  <thead className="bg-neutral-50/70 dark:bg-neutral-900/80 text-neutral-500 dark:text-neutral-400 uppercase tracking-wider text-[10px] border-b border-neutral-200/60 dark:border-neutral-800">
                    <tr>
                      <th className="p-3">Order Number</th>
                      <th className="p-3">Customer</th>
                      <th className="p-3">Total</th>
                      <th className="p-3">Payment</th>
                      <th className="p-3">Status</th>
                      <th className="p-3">Date</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-neutral-100 dark:divide-neutral-800/60">
                    {metrics.recent_orders.map((o) => (
                      <tr key={o.id} className="hover:bg-neutral-50/60 dark:hover:bg-white/[0.03] transition-colors">
                        <td className="p-3 font-mono font-bold text-neutral-900 dark:text-neutral-100">{o.order_number}</td>
                        <td className="p-3">
                          <div className="flex items-center space-x-1.5 mb-0.5">
                            <span className="font-semibold text-neutral-900 dark:text-neutral-100">{o.customer_name}</span>
                            <span className="text-[9px] font-mono px-1.5 py-0.2 rounded-xs bg-neutral-100 dark:bg-neutral-800 text-neutral-700 dark:text-neutral-300 border border-neutral-200 dark:border-neutral-700">
                              {o.customer_code || `AUR-CUST-${String(o.user_id || o.id).padStart(4, '0')}`}
                            </span>
                          </div>
                          <span className="text-[10px] text-neutral-400 dark:text-neutral-500 font-mono block">{o.customer_email}</span>
                        </td>
                        <td className="p-3 font-bold text-neutral-900 dark:text-neutral-100">{formatPrice(o.total_amount)}</td>
                        <td className="p-3 uppercase text-[11px] text-neutral-700 dark:text-neutral-300">{o.payment_method}</td>
                        <td className="p-3">
                          <span className={`px-2 py-0.5 text-[10px] font-bold uppercase rounded-xs ${
                            o.status === 'delivered' ? 'bg-emerald-100 dark:bg-emerald-950/60 text-emerald-800 dark:text-emerald-400 border border-emerald-200 dark:border-emerald-900/50' :
                            o.status === 'shipped' ? 'bg-blue-100 dark:bg-blue-950/60 text-blue-800 dark:text-blue-400 border border-blue-200 dark:border-blue-900/50' :
                            o.status === 'cancelled' ? 'bg-neutral-200 dark:bg-neutral-800 text-neutral-700 dark:text-neutral-300' : 'bg-amber-100 dark:bg-amber-950/60 text-amber-800 dark:text-amber-400 border border-amber-200 dark:border-amber-900/50'
                          }`}>
                            {o.status}
                          </span>
                        </td>
                        <td className="p-3 text-neutral-400 dark:text-neutral-500">{new Date(o.created_at).toLocaleDateString()}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {/* ========================================================= */}
        {/* TAB 2: PRODUCTS CATALOGUE CRUD */}
        {/* ========================================================= */}
        {activeTab === 'products' && (
          <div className="space-y-6">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <div className="relative max-w-sm w-full">
                <input
                  type="text"
                  placeholder="Filter catalogue by title..."
                  value={productSearch}
                  onChange={(e) => setProductSearch(e.target.value)}
                  className="w-full pl-9 pr-3 py-2 text-xs liquid-input rounded-xl text-neutral-900 dark:text-neutral-100 placeholder-neutral-400 dark:placeholder-neutral-500"
                />
                <Search size={14} className="absolute left-3 top-2.5 text-neutral-400 dark:text-neutral-500" />
              </div>

              <button
                onClick={() => {
                  setEditingProduct(null);
                  setProductForm({
                    name: '',
                    category_id: categories[0]?.id || 1,
                    base_price: 120,
                    discount_price: '',
                    description: '',
                    brand: 'Aura Apparel',
                    material: '100% French Flax Linen',
                    fit_type: 'Regular',
                    is_featured: false,
                    image_url: 'https://images.unsplash.com/photo-1595777457583-95e059d581b8?auto=format&fit=crop&w=800&q=80'
                  });
                  setShowProductModal(true);
                }}
                className="px-4 py-2 liquid-btn-gold text-neutral-950 text-xs uppercase tracking-wider font-bold rounded-xl flex items-center gap-1.5 shadow-md transition-all"
              >
                <Plus size={14} /> Add Product
              </button>
            </div>

            <div className="liquid-glass rounded-2xl border border-white/70 dark:border-white/10 shadow-lg overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead className="bg-neutral-50/70 dark:bg-neutral-900/80 text-neutral-500 dark:text-neutral-400 uppercase tracking-wider text-[10px] border-b border-neutral-200/60 dark:border-neutral-800">
                  <tr>
                    <th className="p-3.5">Piece</th>
                    <th className="p-3.5">Category</th>
                    <th className="p-3.5">Base Price</th>
                    <th className="p-3.5">Sale Price</th>
                    <th className="p-3.5">Total Stock</th>
                    <th className="p-3.5">Rating</th>
                    <th className="p-3.5">Sales</th>
                    <th className="p-3.5 text-right">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-neutral-100 dark:divide-neutral-800/60">
                  {products
                    .filter(p => !productSearch || p.name.toLowerCase().includes(productSearch.toLowerCase()))
                    .map((p) => (
                      <tr key={p.id} className="hover:bg-neutral-50/60 dark:hover:bg-white/[0.03] transition-colors">
                        <td className="p-3.5 flex items-center gap-3">
                          <ImageWithFallback src={p.primary_image} alt={p.name} categoryName={p.category_name} className="w-10 h-12 object-cover rounded-md" />
                          <div>
                            <span className="font-bold text-neutral-900 dark:text-neutral-100 block truncate max-w-xs">{p.name}</span>
                            <span className="text-[10px] text-neutral-400 dark:text-neutral-500 font-mono">ID: #{p.id}</span>
                          </div>
                        </td>
                        <td className="p-3.5 text-neutral-600 dark:text-neutral-300">{p.category_name}</td>
                        <td className="p-3.5 font-bold text-neutral-900 dark:text-neutral-100">{formatPrice(p.base_price)}</td>
                        <td className="p-3.5 text-neutral-500 dark:text-neutral-400">
                          {p.discount_price ? formatPrice(p.discount_price) : '—'}
                        </td>
                        <td className="p-3.5">
                          <span className={`font-semibold ${p.total_stock <= 10 ? 'text-red-500 dark:text-red-400 font-bold' : 'text-neutral-800 dark:text-neutral-200'}`}>
                            {p.total_stock}
                          </span>
                        </td>
                        <td className="p-3.5 font-semibold text-amber-500 dark:text-amber-400">★ {p.average_rating.toFixed(1)}</td>
                        <td className="p-3.5 text-neutral-600 dark:text-neutral-400">{p.sales_count}</td>
                        <td className="p-3.5 text-right space-x-2">
                          <button
                            onClick={() => {
                              setEditingProduct(p);
                              setProductForm({
                                name: p.name,
                                category_id: p.category_id,
                                base_price: p.base_price,
                                discount_price: p.discount_price ? String(p.discount_price) : '',
                                description: p.description,
                                brand: p.brand,
                                material: p.material || '',
                                fit_type: p.fit_type || 'Regular',
                                is_featured: p.is_featured,
                                image_url: p.primary_image
                              });
                              setShowProductModal(true);
                            }}
                            className="p-1 text-neutral-400 hover:text-neutral-900 dark:hover:text-aura-gold transition-colors"
                            title="Edit"
                          >
                            <Edit size={14} />
                          </button>
                          <button
                            onClick={() => handleDeleteProduct(p.id)}
                            className="p-1 text-neutral-400 hover:text-red-500 dark:hover:text-red-400 transition-colors"
                            title="Delete"
                          >
                            <Trash2 size={14} />
                          </button>
                        </td>
                      </tr>
                    ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* ========================================================= */}
        {/* TAB 3: INVENTORY STOCK MANAGEMENT */}
        {/* ========================================================= */}
        {activeTab === 'inventory' && (
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="font-serif font-bold text-lg text-neutral-900 dark:text-neutral-100">
                  Real-Time Variant Inventory & Stock Alerts
                </h3>
                <p className="text-xs text-neutral-500 dark:text-neutral-400">
                  Monitor stock levels across all garment sizes and colors. Variants under 10 units are highlighted.
                </p>
              </div>
            </div>

            <div className="liquid-glass rounded-2xl border border-white/70 dark:border-white/10 shadow-lg overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead className="bg-neutral-50/70 dark:bg-neutral-900/80 text-neutral-500 dark:text-neutral-400 uppercase tracking-wider text-[10px] border-b border-neutral-200/60 dark:border-neutral-800">
                  <tr>
                    <th className="p-3.5">SKU</th>
                    <th className="p-3.5">Garment Name</th>
                    <th className="p-3.5">Size</th>
                    <th className="p-3.5">Color</th>
                    <th className="p-3.5">Current Stock</th>
                    <th className="p-3.5">Stock Status</th>
                    <th className="p-3.5 text-right">Quick Restock</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-neutral-100 dark:divide-neutral-800/60">
                  {inventoryList.map((item) => (
                    <tr key={item.id} className="hover:bg-neutral-50/60 dark:hover:bg-white/[0.03] transition-colors">
                      <td className="p-3.5 font-mono font-bold text-neutral-900 dark:text-neutral-100">{item.sku}</td>
                      <td className="p-3.5 font-medium text-neutral-800 dark:text-neutral-200">{item.product_name}</td>
                      <td className="p-3.5 font-semibold text-neutral-900 dark:text-neutral-100">{item.size}</td>
                      <td className="p-3.5 flex items-center gap-1.5 text-neutral-700 dark:text-neutral-300">
                        <span className="w-2.5 h-2.5 rounded-full border border-black/10 dark:border-white/20" style={{ backgroundColor: item.color_hex }} />
                        <span>{item.color}</span>
                      </td>
                      <td className="p-3.5 font-bold text-neutral-900 dark:text-neutral-100">{item.stock_quantity} units</td>
                      <td className="p-3.5">
                        {item.stock_quantity <= 5 ? (
                          <span className="px-2 py-0.5 bg-red-100 dark:bg-red-950/60 text-red-800 dark:text-red-400 border border-red-200 dark:border-red-900/50 text-[10px] font-bold uppercase rounded-md">Critical Low</span>
                        ) : item.stock_quantity <= 10 ? (
                          <span className="px-2 py-0.5 bg-amber-100 dark:bg-amber-950/60 text-amber-800 dark:text-amber-400 border border-amber-200 dark:border-amber-900/50 text-[10px] font-bold uppercase rounded-md">Low Stock</span>
                        ) : (
                          <span className="px-2 py-0.5 bg-emerald-100 dark:bg-emerald-950/60 text-emerald-800 dark:text-emerald-400 border border-emerald-200 dark:border-emerald-900/50 text-[10px] font-bold uppercase rounded-md">Adequate</span>
                        )}
                      </td>
                      <td className="p-3.5 text-right">
                        <button
                          onClick={() => {
                            setStockEditVariant(item);
                            setStockInput(item.stock_quantity);
                          }}
                          className="px-3 py-1.5 liquid-pill text-[11px] font-semibold text-neutral-800 dark:text-neutral-200 hover:text-aura-gold transition-colors"
                        >
                          Adjust Units
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* ========================================================= */}
        {/* TAB 4: ORDERS & STATUS DISPATCH */}
        {/* ========================================================= */}
        {activeTab === 'orders' && (
          <div className="space-y-4">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <h3 className="font-serif font-bold text-lg text-neutral-900 dark:text-neutral-100">
                Customer Orders Directory
              </h3>

              <div className="flex items-center gap-2">
                <span className="text-xs text-neutral-500 dark:text-neutral-400 uppercase tracking-wider font-semibold">Status:</span>
                <select
                  value={orderStatusFilter}
                  onChange={(e) => setOrderStatusFilter(e.target.value)}
                  className="px-3 py-1.5 text-xs liquid-input rounded-xl text-neutral-900 dark:text-neutral-100"
                >
                  <option value="" className="bg-white dark:bg-neutral-900">All Statuses</option>
                  <option value="pending" className="bg-white dark:bg-neutral-900">Pending</option>
                  <option value="processing" className="bg-white dark:bg-neutral-900">Processing</option>
                  <option value="shipped" className="bg-white dark:bg-neutral-900">Shipped</option>
                  <option value="delivered" className="bg-white dark:bg-neutral-900">Delivered</option>
                  <option value="cancelled" className="bg-white dark:bg-neutral-900">Cancelled</option>
                </select>
              </div>
            </div>

            <div className="liquid-glass rounded-2xl border border-white/70 dark:border-white/10 shadow-lg overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead className="bg-neutral-50/70 dark:bg-neutral-900/80 text-neutral-500 dark:text-neutral-400 uppercase tracking-wider text-[10px] border-b border-neutral-200/60 dark:border-neutral-800">
                  <tr>
                    <th className="p-3.5">Order Number</th>
                    <th className="p-3.5">Customer</th>
                    <th className="p-3.5">Total Amount</th>
                    <th className="p-3.5">Items</th>
                    <th className="p-3.5">Payment</th>
                    <th className="p-3.5">Order Status</th>
                    <th className="p-3.5">Tracking Number</th>
                    <th className="p-3.5 text-right">Update</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-neutral-100 dark:divide-neutral-800/60">
                  {orders.map((o) => (
                    <tr key={o.id} className="hover:bg-neutral-50/60 dark:hover:bg-white/[0.03] transition-colors">
                      <td className="p-3.5 font-mono font-bold text-neutral-900 dark:text-neutral-100">{o.order_number}</td>
                      <td className="p-3.5">
                        <div className="flex items-center space-x-1.5 mb-0.5">
                          <span className="font-semibold text-neutral-900 dark:text-neutral-100">{o.customer_name}</span>
                          <span className="text-[9px] font-mono font-medium px-1.5 py-0.2 rounded-xs bg-neutral-100 dark:bg-neutral-800 text-neutral-700 dark:text-neutral-300 border border-neutral-200 dark:border-neutral-700">
                            {o.customer_code || `AUR-CUST-${String(o.user_id || o.id).padStart(4, '0')}`}
                          </span>
                        </div>
                        <span className="text-[11px] text-neutral-500 dark:text-neutral-400 font-mono block">{o.customer_email}</span>
                      </td>
                      <td className="p-3.5 font-bold text-neutral-900 dark:text-neutral-100">{formatPrice(o.total_amount)}</td>
                      <td className="p-3.5 text-neutral-700 dark:text-neutral-300">{o.item_count} pieces</td>
                      <td className="p-3.5">
                        <span className="uppercase text-[11px] font-bold block text-neutral-900 dark:text-neutral-100">{o.payment_method}</span>
                        <span className="text-[10px] text-neutral-400 dark:text-neutral-500">{o.payment_status}</span>
                      </td>
                      <td className="p-3.5">
                        <span className={`px-2 py-0.5 text-[10px] font-bold uppercase rounded-xs ${
                          o.status === 'delivered' ? 'bg-emerald-100 dark:bg-emerald-950/60 text-emerald-800 dark:text-emerald-400 border border-emerald-200 dark:border-emerald-900/50' :
                          o.status === 'shipped' ? 'bg-blue-100 dark:bg-blue-950/60 text-blue-800 dark:text-blue-400 border border-blue-200 dark:border-blue-900/50' :
                          o.status === 'cancelled' ? 'bg-neutral-200 dark:bg-neutral-800 text-neutral-700 dark:text-neutral-300' : 'bg-amber-100 dark:bg-amber-950/60 text-amber-800 dark:text-amber-400 border border-amber-200 dark:border-amber-900/50'
                        }`}>
                          {o.status}
                        </span>
                      </td>
                      <td className="p-3.5 font-mono text-neutral-600 dark:text-neutral-400">{o.tracking_number || '—'}</td>
                      <td className="p-3.5 text-right">
                        <button
                          onClick={() => {
                            setSelectedOrderForStatus(o);
                            setNewStatus(o.status);
                            setTrackingNumber(o.tracking_number || '');
                            setCarrierName(o.carrier_name || 'Aura Express Logistics');
                          }}
                          className="px-3.5 py-1.5 liquid-pill text-[11px] font-bold uppercase tracking-wider text-neutral-900 dark:text-neutral-100 hover:text-aura-gold transition-colors"
                        >
                          Change Status
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* ========================================================= */}
        {/* TAB 5: RETURN & CANCELLATION REQUESTS */}
        {/* ========================================================= */}
        {activeTab === 'requests' && (
          <div className="space-y-4">
            <div>
              <h3 className="font-serif font-bold text-lg text-neutral-900 dark:text-neutral-100">
                Cancellation & Return Authorizations
              </h3>
              <p className="text-xs text-neutral-500 dark:text-neutral-400">
                Review client requests, approve full refunds with automatic stock restoration, or log rejection notes.
              </p>
            </div>

            <div className="liquid-glass rounded-2xl border border-white/70 dark:border-white/10 shadow-lg overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead className="bg-neutral-50/70 dark:bg-neutral-900/80 text-neutral-500 dark:text-neutral-400 uppercase tracking-wider text-[10px] border-b border-neutral-200/60 dark:border-neutral-800">
                  <tr>
                    <th className="p-3.5">Order Ref</th>
                    <th className="p-3.5">Patron</th>
                    <th className="p-3.5">Type</th>
                    <th className="p-3.5">Customer Reason</th>
                    <th className="p-3.5">Customer Notes</th>
                    <th className="p-3.5">Status</th>
                    <th className="p-3.5 text-right">Action</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-neutral-100 dark:divide-neutral-800/60">
                  {returnRequests.map((req) => (
                    <tr key={req.id} className="hover:bg-neutral-50/60 dark:hover:bg-white/[0.03] transition-colors">
                      <td className="p-3.5 font-mono font-bold text-neutral-900 dark:text-neutral-100">{req.order_number}</td>
                      <td className="p-3.5">
                        <div className="flex items-center space-x-1.5 mb-0.5">
                          <span className="font-semibold text-neutral-900 dark:text-neutral-100">{req.customer_name}</span>
                          <span className="text-[9px] font-mono px-1.5 py-0.2 rounded-xs bg-neutral-100 dark:bg-neutral-800 text-neutral-700 dark:text-neutral-300 border border-neutral-200 dark:border-neutral-700">
                            {req.customer_code || `AUR-CUST-${String(req.user_id || req.id).padStart(4, '0')}`}
                          </span>
                        </div>
                        {req.customer_email && (
                          <span className="text-[10px] text-neutral-400 dark:text-neutral-500 font-mono block">{req.customer_email}</span>
                        )}
                      </td>
                      <td className="p-3.5">
                        <span className="uppercase text-[10px] font-bold px-2 py-0.5 bg-neutral-100 dark:bg-neutral-800 text-neutral-800 dark:text-neutral-200 rounded-xs border border-neutral-200 dark:border-neutral-700">
                          {req.request_type}
                        </span>
                      </td>
                      <td className="p-3.5 text-neutral-700 dark:text-neutral-300">{req.reason}</td>
                      <td className="p-3.5 text-neutral-500 dark:text-neutral-400 max-w-xs truncate">{req.customer_notes || 'None'}</td>
                      <td className="p-3.5">
                        <span className={`px-2 py-0.5 text-[10px] font-bold uppercase rounded-xs ${
                          req.status === 'approved' ? 'bg-emerald-100 dark:bg-emerald-950/60 text-emerald-800 dark:text-emerald-400 border border-emerald-200 dark:border-emerald-900/50' :
                          req.status === 'rejected' ? 'bg-red-100 dark:bg-red-950/60 text-red-800 dark:text-red-400 border border-red-200 dark:border-red-900/50' : 'bg-amber-100 dark:bg-amber-950/60 text-amber-800 dark:text-amber-400 border border-amber-200 dark:border-amber-900/50'
                        }`}>
                          {req.status}
                        </span>
                      </td>
                      <td className="p-3.5 text-right">
                        {req.status === 'pending' ? (
                          <button
                            onClick={() => {
                              setProcessingReq(req);
                              setAdminNotes('');
                            }}
                            className="px-3.5 py-1.5 liquid-btn-gold text-neutral-950 text-[11px] font-bold uppercase tracking-wider rounded-xl shadow-sm transition-all"
                          >
                            Review
                          </button>
                        ) : (
                          <span className="text-[11px] text-neutral-400 dark:text-neutral-500">Processed</span>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* ========================================================= */}
        {/* TAB 6: COUPONS & VOUCHERS */}
        {/* ========================================================= */}
        {activeTab === 'coupons' && (
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="font-serif font-bold text-lg text-neutral-900 dark:text-neutral-100">
                  Promotional Vouchers & Coupons
                </h3>
                <p className="text-xs text-neutral-500 dark:text-neutral-400">
                  Create discount codes with minimum subtotal requirements and usage limits.
                </p>
              </div>

              <button
                onClick={() => setShowCouponModal(true)}
                className="px-4 py-2 liquid-btn-gold text-neutral-950 text-xs uppercase tracking-wider font-bold rounded-xl flex items-center gap-1.5 shadow-md transition-all"
              >
                <Plus size={14} /> New Voucher
              </button>
            </div>

            <div className="liquid-glass rounded-2xl border border-white/70 dark:border-white/10 shadow-lg overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead className="bg-neutral-50/70 dark:bg-neutral-900/80 text-neutral-500 dark:text-neutral-400 uppercase tracking-wider text-[10px] border-b border-neutral-200/60 dark:border-neutral-800">
                  <tr>
                    <th className="p-3.5">Voucher Code</th>
                    <th className="p-3.5">Discount</th>
                    <th className="p-3.5">Min Order</th>
                    <th className="p-3.5">Max Discount</th>
                    <th className="p-3.5">Times Used</th>
                    <th className="p-3.5">Limit</th>
                    <th className="p-3.5">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-neutral-100 dark:divide-neutral-800/60">
                  {coupons.map((c) => (
                    <tr key={c.id} className="hover:bg-neutral-50/60 dark:hover:bg-white/[0.03] transition-colors">
                      <td className="p-3.5 font-mono font-bold text-neutral-900 dark:text-neutral-100">{c.code}</td>
                      <td className="p-3.5 font-semibold text-emerald-600 dark:text-emerald-400">
                        {c.discount_type === 'percentage' ? `${c.discount_value}% OFF` : `${formatPrice(c.discount_value)} OFF`}
                      </td>
                      <td className="p-3.5 text-neutral-700 dark:text-neutral-300">{formatPrice(c.min_order_amount)}</td>
                      <td className="p-3.5 text-neutral-700 dark:text-neutral-300">{c.max_discount_amount ? formatPrice(c.max_discount_amount) : 'No Cap'}</td>
                      <td className="p-3.5 text-neutral-700 dark:text-neutral-300">{c.times_used}</td>
                      <td className="p-3.5 text-neutral-700 dark:text-neutral-300">{c.usage_limit}</td>
                      <td className="p-3.5">
                        <span className={`px-2 py-0.5 text-[10px] font-bold uppercase rounded-xs ${
                          c.is_active ? 'bg-emerald-100 dark:bg-emerald-950/60 text-emerald-800 dark:text-emerald-400 border border-emerald-200 dark:border-emerald-900/50' : 'bg-neutral-200 dark:bg-neutral-800 text-neutral-600 dark:text-neutral-400'
                        }`}>
                          {c.is_active ? 'Active' : 'Disabled'}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* ========================================================= */}
        {/* TAB 7: CATEGORIES */}
        {/* ========================================================= */}
        {activeTab === 'categories' && (
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="font-serif font-bold text-lg text-neutral-900 dark:text-neutral-100">
                  Wardrobe Collections & Categories
                </h3>
              </div>

              <button
                onClick={() => setShowCategoryModal(true)}
                className="px-4 py-2 liquid-btn-gold text-neutral-950 text-xs uppercase tracking-wider font-bold rounded-xl flex items-center gap-1.5 shadow-md transition-all"
              >
                <Plus size={14} /> Add Category
              </button>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {categories.map((cat) => (
                <div key={cat.id} className="liquid-glass rounded-2xl border border-white/70 dark:border-white/10 p-4 shadow-md flex items-center gap-4 hover:border-aura-gold/50 transition-all">
                  <ImageWithFallback src={cat.image_url} alt={cat.name} categoryName={cat.name} className="w-16 h-20 object-cover rounded-xl shrink-0" />
                  <div className="flex-1 min-w-0">
                    <h4 className="font-bold text-sm text-neutral-900 dark:text-neutral-100 truncate">{cat.name}</h4>
                    <p className="text-[11px] text-neutral-400 dark:text-neutral-500 font-mono">Slug: {cat.slug}</p>
                    <p className="text-xs text-neutral-600 dark:text-neutral-400 line-clamp-1 mt-1">{cat.description}</p>
                    <span className="text-[11px] text-aura-gold font-semibold mt-1 block">
                      {cat.product_count} Garments
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* ========================================================= */}
        {/* TAB 8: CUSTOMERS DIRECTORY */}
        {/* ========================================================= */}
        {activeTab === 'customers' && (
          <div className="space-y-4">
            <div>
              <h3 className="font-serif font-bold text-lg text-neutral-900 dark:text-neutral-100">
                Registered Patrons Directory
              </h3>
              <p className="text-xs text-neutral-500 dark:text-neutral-400">
                View customer account history, lifetime spending, and transaction activity.
              </p>
            </div>

            <div className="liquid-glass rounded-2xl border border-white/70 dark:border-white/10 shadow-lg overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead className="bg-neutral-50/70 dark:bg-neutral-900/80 text-neutral-500 dark:text-neutral-400 uppercase tracking-wider text-[10px] border-b border-neutral-200/60 dark:border-neutral-800">
                  <tr>
                    <th className="p-3.5">Customer Name</th>
                    <th className="p-3.5">Customer ID</th>
                    <th className="p-3.5">Email</th>
                    <th className="p-3.5">Phone</th>
                    <th className="p-3.5">Orders Placed</th>
                    <th className="p-3.5">Lifetime Spend</th>
                    <th className="p-3.5">Joined Date</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-neutral-100 dark:divide-neutral-800/60">
                  {customers.map((c) => (
                    <tr key={c.id} className="hover:bg-neutral-50/60 dark:hover:bg-white/[0.03] transition-colors">
                      <td className="p-3.5 font-bold text-neutral-900 dark:text-neutral-100">{c.full_name}</td>
                      <td className="p-3.5">
                        <span className="text-[10px] font-mono font-semibold px-2 py-0.5 rounded-xs bg-neutral-100 dark:bg-neutral-800 text-neutral-700 dark:text-neutral-300 border border-neutral-200 dark:border-neutral-700">
                          {c.customer_code || `AUR-CUST-${String(c.id).padStart(4, '0')}`}
                        </span>
                      </td>
                      <td className="p-3.5 text-neutral-600 dark:text-neutral-400 font-mono text-[11px]">{c.email}</td>
                      <td className="p-3.5 text-neutral-500 dark:text-neutral-400 font-mono">{c.phone || '—'}</td>
                      <td className="p-3.5 font-semibold text-neutral-900 dark:text-neutral-100">{c.order_count} orders</td>
                      <td className="p-3.5 font-bold text-neutral-900 dark:text-neutral-100">{formatPrice(c.total_spent)}</td>
                      <td className="p-3.5 text-neutral-400 dark:text-neutral-500">{new Date(c.created_at).toLocaleDateString()}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

      </div>

      {/* ========================================================= */}
      {/* MODAL 1: ADD/EDIT PRODUCT */}
      {/* ========================================================= */}
      {showProductModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-md p-4 animate-in fade-in overflow-y-auto">
          <div className="liquid-glass bg-white dark:bg-[#141312] border border-white/80 dark:border-white/10 max-w-xl w-full rounded-2xl shadow-2xl p-6 sm:p-8 my-8 space-y-4">
            <div className="flex items-center justify-between pb-3 border-b border-neutral-200/60 dark:border-neutral-800">
              <h3 className="font-serif font-bold text-base sm:text-lg text-neutral-900 dark:text-neutral-100">
                {editingProduct ? 'Edit Catalogue Product' : 'Add New Garment Piece'}
              </h3>
              <button onClick={() => setShowProductModal(false)} className="text-neutral-400 hover:text-neutral-900 dark:hover:text-white transition-colors">
                <X size={18} />
              </button>
            </div>

            <form onSubmit={handleSaveProduct} className="space-y-3.5 text-xs">
              <div>
                <label className="text-[11px] font-semibold text-neutral-700 dark:text-neutral-300 block mb-1 uppercase tracking-wider">Product Title *</label>
                <input
                  type="text"
                  required
                  value={productForm.name}
                  onChange={(e) => setProductForm({ ...productForm, name: e.target.value })}
                  placeholder="e.g. Mulberry Silk Slip Dress"
                  className="w-full px-3.5 py-2 liquid-input rounded-xl text-neutral-900 dark:text-neutral-100 placeholder-neutral-400 dark:placeholder-neutral-500"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-[11px] font-semibold text-neutral-700 dark:text-neutral-300 block mb-1 uppercase tracking-wider">Category *</label>
                  <select
                    value={productForm.category_id}
                    onChange={(e) => setProductForm({ ...productForm, category_id: Number(e.target.value) })}
                    className="w-full px-3.5 py-2 liquid-input rounded-xl text-neutral-900 dark:text-neutral-100"
                  >
                    {categories.map((c) => (
                      <option key={c.id} value={c.id} className="bg-white dark:bg-neutral-900">{c.name}</option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="text-[11px] font-semibold text-neutral-700 dark:text-neutral-300 block mb-1 uppercase tracking-wider">Base Price (₹) *</label>
                  <input
                    type="number"
                    step="0.01"
                    required
                    value={productForm.base_price}
                    onChange={(e) => setProductForm({ ...productForm, base_price: Number(e.target.value) })}
                    className="w-full px-3.5 py-2 liquid-input rounded-xl text-neutral-900 dark:text-neutral-100"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-[11px] font-semibold text-neutral-700 dark:text-neutral-300 block mb-1 uppercase tracking-wider">Sale Discount Price (₹)</label>
                  <input
                    type="number"
                    step="0.01"
                    value={productForm.discount_price}
                    onChange={(e) => setProductForm({ ...productForm, discount_price: e.target.value })}
                    placeholder="Leave empty for regular price"
                    className="w-full px-3.5 py-2 liquid-input rounded-xl text-neutral-900 dark:text-neutral-100 placeholder-neutral-400 dark:placeholder-neutral-500"
                  />
                </div>
                <div>
                  <label className="text-[11px] font-semibold text-neutral-700 dark:text-neutral-300 block mb-1 uppercase tracking-wider">Fabric Material</label>
                  <input
                    type="text"
                    value={productForm.material}
                    onChange={(e) => setProductForm({ ...productForm, material: e.target.value })}
                    className="w-full px-3.5 py-2 liquid-input rounded-xl text-neutral-900 dark:text-neutral-100"
                  />
                </div>
              </div>

              <div>
                <label className="text-[11px] font-semibold text-neutral-700 dark:text-neutral-300 block mb-1 uppercase tracking-wider">Primary Image URL *</label>
                <input
                  type="url"
                  required
                  value={productForm.image_url}
                  onChange={(e) => setProductForm({ ...productForm, image_url: e.target.value })}
                  className="w-full px-3.5 py-2 liquid-input rounded-xl text-neutral-900 dark:text-neutral-100 font-mono text-[11px]"
                />
              </div>

              <div>
                <div className="flex items-center justify-between mb-1.5">
                  <label className="text-[11px] font-semibold text-neutral-700 dark:text-neutral-300 uppercase tracking-wider">Garment Description *</label>
                  <button
                    type="button"
                    onClick={handleGenerateEditorialCopy}
                    disabled={isGeneratingCopy || !productForm.name}
                    className="inline-flex items-center gap-1.5 px-2.5 py-1 text-[10.5px] rounded-lg liquid-btn-gold text-neutral-950 font-bold uppercase tracking-wider transition-all disabled:opacity-50 shadow-xs"
                    title="Draft Vogue-level editorial copy using Gemini AI"
                  >
                    <Sparkles size={12} className={isGeneratingCopy ? "animate-spin" : "animate-pulse"} />
                    <span>{isGeneratingCopy ? 'Drafting Copy...' : '✨ AI Generate Copy'}</span>
                  </button>
                </div>
                <textarea
                  rows={3}
                  required
                  placeholder="Atmospheric prose describing fabric weave, silhouette drape, and bespoke craftsmanship..."
                  value={productForm.description}
                  onChange={(e) => setProductForm({ ...productForm, description: e.target.value })}
                  className="w-full px-3.5 py-2 liquid-input rounded-xl text-neutral-900 dark:text-neutral-100"
                />
              </div>

              <div className="pt-1">
                <label className="flex items-center gap-2 cursor-pointer text-neutral-700 dark:text-neutral-300">
                  <input
                    type="checkbox"
                    checked={productForm.is_featured}
                    onChange={(e) => setProductForm({ ...productForm, is_featured: e.target.checked })}
                    className="rounded text-aura-gold focus:ring-aura-gold bg-white dark:bg-neutral-900 border-neutral-300 dark:border-neutral-700"
                  />
                  <span>Highlight on Featured Home page carousel</span>
                </label>
              </div>

              <div className="flex justify-end gap-3 pt-3 border-t border-neutral-200/60 dark:border-neutral-800">
                <button
                  type="button"
                  onClick={() => setShowProductModal(false)}
                  className="px-4 py-2 liquid-pill text-xs font-semibold text-neutral-700 dark:text-neutral-300 hover:text-neutral-900 dark:hover:text-white transition-colors"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-5 py-2 liquid-btn-gold text-neutral-950 uppercase tracking-wider font-bold rounded-xl shadow-md transition-all"
                >
                  {editingProduct ? 'Save Edits' : 'Publish Product'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* ========================================================= */}
      {/* MODAL 2: INLINE STOCK ADJUSTER */}
      {/* ========================================================= */}
      {stockEditVariant && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-md p-4 animate-in fade-in">
          <div className="liquid-glass bg-white dark:bg-[#141312] border border-white/80 dark:border-white/10 max-w-sm w-full rounded-2xl shadow-2xl p-6 space-y-4 text-xs">
            <div className="flex items-center justify-between pb-3 border-b border-neutral-200/60 dark:border-neutral-800">
              <h3 className="font-serif font-bold text-base text-neutral-900 dark:text-neutral-100">
                Adjust Stock Quantity
              </h3>
              <button onClick={() => setStockEditVariant(null)} className="text-neutral-400 hover:text-neutral-900 dark:hover:text-white transition-colors">
                <X size={18} />
              </button>
            </div>

            <div className="p-3 bg-neutral-100/70 dark:bg-neutral-900/80 rounded-xl border border-neutral-200/60 dark:border-neutral-800 text-neutral-600 dark:text-neutral-300">
              Editing SKU: <strong className="font-mono text-neutral-900 dark:text-neutral-100">{stockEditVariant.sku}</strong><br />
              {stockEditVariant.product_name} ({stockEditVariant.color}, {stockEditVariant.size})
            </div>

            <div>
              <label className="text-[11px] font-semibold text-neutral-700 dark:text-neutral-300 block mb-1 uppercase tracking-wider">
                Units in Atelier Stock
              </label>
              <input
                type="number"
                min="0"
                value={stockInput}
                onChange={(e) => setStockInput(parseInt(e.target.value, 10) || 0)}
                className="w-full px-3.5 py-2.5 liquid-input rounded-xl text-base font-bold text-neutral-900 dark:text-neutral-100"
              />
            </div>

            <div className="flex justify-end gap-3 pt-3 border-t border-neutral-200/60 dark:border-neutral-800">
              <button
                onClick={() => setStockEditVariant(null)}
                className="px-4 py-2 liquid-pill text-xs font-semibold text-neutral-700 dark:text-neutral-300 hover:text-neutral-900 dark:hover:text-white transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={handleUpdateStock}
                className="px-5 py-2 liquid-btn-gold text-neutral-950 uppercase tracking-wider font-bold rounded-xl shadow-md transition-all"
              >
                Save Stock
              </button>
            </div>
          </div>
        </div>
      )}

      {/* ========================================================= */}
      {/* MODAL 3: ORDER STATUS & TRACKING UPDATE */}
      {/* ========================================================= */}
      {selectedOrderForStatus && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-md p-4 animate-in fade-in">
          <div className="liquid-glass bg-white dark:bg-[#141312] border border-white/80 dark:border-white/10 max-w-md w-full rounded-2xl shadow-2xl p-6 space-y-4 text-xs">
            <div className="flex items-center justify-between pb-3 border-b border-neutral-200/60 dark:border-neutral-800">
              <h3 className="font-serif font-bold text-base text-neutral-900 dark:text-neutral-100">
                Update Order #{selectedOrderForStatus.order_number}
              </h3>
              <button onClick={() => setSelectedOrderForStatus(null)} className="text-neutral-400 hover:text-neutral-900 dark:hover:text-white transition-colors">
                <X size={18} />
              </button>
            </div>

            <div className="space-y-3">
              <div>
                <label className="text-[11px] font-semibold text-neutral-700 dark:text-neutral-300 block mb-1 uppercase tracking-wider">
                  Lifecycle Status
                </label>
                <select
                  value={newStatus}
                  onChange={(e) => setNewStatus(e.target.value)}
                  className="w-full px-3.5 py-2 liquid-input rounded-xl text-neutral-900 dark:text-neutral-100"
                >
                  <option value="pending" className="bg-white dark:bg-neutral-900">Pending</option>
                  <option value="processing" className="bg-white dark:bg-neutral-900">Processing</option>
                  <option value="shipped" className="bg-white dark:bg-neutral-900">Shipped</option>
                  <option value="delivered" className="bg-white dark:bg-neutral-900">Delivered</option>
                  <option value="cancelled" className="bg-white dark:bg-neutral-900">Cancelled</option>
                </select>
              </div>

              <div>
                <label className="text-[11px] font-semibold text-neutral-700 dark:text-neutral-300 block mb-1 uppercase tracking-wider">
                  Air Courier Partner
                </label>
                <input
                  type="text"
                  value={carrierName}
                  onChange={(e) => setCarrierName(e.target.value)}
                  className="w-full px-3.5 py-2 liquid-input rounded-xl text-neutral-900 dark:text-neutral-100"
                />
              </div>

              <div>
                <label className="text-[11px] font-semibold text-neutral-700 dark:text-neutral-300 block mb-1 uppercase tracking-wider">
                  Waybill / Tracking Number
                </label>
                <input
                  type="text"
                  value={trackingNumber}
                  onChange={(e) => setTrackingNumber(e.target.value)}
                  placeholder="e.g. TRK-892301984"
                  className="w-full px-3.5 py-2 liquid-input rounded-xl text-neutral-900 dark:text-neutral-100 font-mono"
                />
              </div>
            </div>

            <div className="flex justify-end gap-3 pt-3 border-t border-neutral-200/60 dark:border-neutral-800">
              <button
                onClick={() => setSelectedOrderForStatus(null)}
                className="px-4 py-2 liquid-pill text-xs font-semibold text-neutral-700 dark:text-neutral-300 hover:text-neutral-900 dark:hover:text-white transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={handleUpdateOrderStatus}
                className="px-5 py-2 liquid-btn-gold text-neutral-950 uppercase tracking-wider font-bold rounded-xl shadow-md transition-all"
              >
                Apply Update
              </button>
            </div>
          </div>
        </div>
      )}

      {/* ========================================================= */}
      {/* MODAL 4: RETURN / REFUND PROCESSING */}
      {/* ========================================================= */}
      {processingReq && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-md p-4 animate-in fade-in">
          <div className="liquid-glass bg-white dark:bg-[#141312] border border-white/80 dark:border-white/10 max-w-md w-full rounded-2xl shadow-2xl p-6 space-y-4 text-xs">
            <div className="flex items-center justify-between pb-3 border-b border-neutral-200/60 dark:border-neutral-800">
              <h3 className="font-serif font-bold text-base text-neutral-900 dark:text-neutral-100">
                Process {processingReq.request_type.toUpperCase()} Request
              </h3>
              <button onClick={() => setProcessingReq(null)} className="text-neutral-400 hover:text-neutral-900 dark:hover:text-white transition-colors">
                <X size={18} />
              </button>
            </div>

            <div className="p-3.5 bg-neutral-100/70 dark:bg-neutral-900/80 rounded-xl border border-neutral-200/60 dark:border-neutral-800 space-y-1.5 text-neutral-700 dark:text-neutral-300">
              <p><strong className="text-neutral-900 dark:text-neutral-100">Order:</strong> {processingReq.order_number}</p>
              <p><strong className="text-neutral-900 dark:text-neutral-100">Customer:</strong> {processingReq.customer_name}</p>
              <p><strong className="text-neutral-900 dark:text-neutral-100">Reason:</strong> {processingReq.reason}</p>
              <p><strong className="text-neutral-900 dark:text-neutral-100">Notes:</strong> {processingReq.customer_notes || 'None'}</p>
            </div>

            <div>
              <label className="text-[11px] font-semibold text-neutral-700 dark:text-neutral-300 block mb-1 uppercase tracking-wider">
                Concierge Administrative Notes
              </label>
              <textarea
                rows={2}
                value={adminNotes}
                onChange={(e) => setAdminNotes(e.target.value)}
                placeholder="Return authorization code, exchange shipment reference..."
                className="w-full px-3.5 py-2 liquid-input rounded-xl text-neutral-900 dark:text-neutral-100"
              />
            </div>

            <div className="flex justify-end gap-3 pt-3 border-t border-neutral-200/60 dark:border-neutral-800">
              <button
                onClick={() => handleProcessRequest('reject')}
                className="px-4 py-2 border border-red-500/50 text-red-600 dark:text-red-400 hover:bg-red-500/10 font-bold uppercase rounded-xl text-[11px] transition-colors"
              >
                Reject Request
              </button>
              <button
                onClick={() => handleProcessRequest('approve')}
                className="px-5 py-2 bg-emerald-600 hover:bg-emerald-700 text-white font-bold uppercase rounded-xl text-[11px] shadow transition-colors"
              >
                Approve & Refund
              </button>
            </div>
          </div>
        </div>
      )}

      {/* ========================================================= */}
      {/* MODAL 5: ADD VOUCHER */}
      {/* ========================================================= */}
      {showCouponModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-md p-4 animate-in fade-in">
          <div className="liquid-glass bg-white dark:bg-[#141312] border border-white/80 dark:border-white/10 max-w-md w-full rounded-2xl shadow-2xl p-6 space-y-4 text-xs">
            <div className="flex items-center justify-between pb-3 border-b border-neutral-200/60 dark:border-neutral-800">
              <h3 className="font-serif font-bold text-base text-neutral-900 dark:text-neutral-100">
                Publish Promotional Voucher
              </h3>
              <button onClick={() => setShowCouponModal(false)} className="text-neutral-400 hover:text-neutral-900 dark:hover:text-white transition-colors">
                <X size={18} />
              </button>
            </div>

            <form onSubmit={handleCreateCoupon} className="space-y-3">
              <div>
                <label className="text-[11px] font-semibold text-neutral-700 dark:text-neutral-300 block mb-1 uppercase tracking-wider">Coupon Code *</label>
                <input
                  type="text"
                  required
                  placeholder="e.g. VIP25"
                  value={couponForm.code}
                  onChange={(e) => setCouponForm({ ...couponForm, code: e.target.value.toUpperCase() })}
                  className="w-full px-3.5 py-2 liquid-input rounded-xl uppercase font-mono text-neutral-900 dark:text-neutral-100"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-[11px] font-semibold text-neutral-700 dark:text-neutral-300 block mb-1 uppercase tracking-wider">Discount Type</label>
                  <select
                    value={couponForm.discount_type}
                    onChange={(e) => setCouponForm({ ...couponForm, discount_type: e.target.value })}
                    className="w-full px-3.5 py-2 liquid-input rounded-xl text-neutral-900 dark:text-neutral-100"
                  >
                    <option value="percentage" className="bg-white dark:bg-neutral-900">Percentage (%)</option>
                    <option value="fixed" className="bg-white dark:bg-neutral-900">Fixed Amount (₹)</option>
                  </select>
                </div>
                <div>
                  <label className="text-[11px] font-semibold text-neutral-700 dark:text-neutral-300 block mb-1 uppercase tracking-wider">Discount Value *</label>
                  <input
                    type="number"
                    step="0.01"
                    required
                    value={couponForm.discount_value}
                    onChange={(e) => setCouponForm({ ...couponForm, discount_value: Number(e.target.value) })}
                    className="w-full px-3.5 py-2 liquid-input rounded-xl text-neutral-900 dark:text-neutral-100"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-[11px] font-semibold text-neutral-700 dark:text-neutral-300 block mb-1 uppercase tracking-wider">Min Order Amount (₹)</label>
                  <input
                    type="number"
                    value={couponForm.min_order_amount}
                    onChange={(e) => setCouponForm({ ...couponForm, min_order_amount: Number(e.target.value) })}
                    className="w-full px-3.5 py-2 liquid-input rounded-xl text-neutral-900 dark:text-neutral-100"
                  />
                </div>
                <div>
                  <label className="text-[11px] font-semibold text-neutral-700 dark:text-neutral-300 block mb-1 uppercase tracking-wider">Usage Limit</label>
                  <input
                    type="number"
                    value={couponForm.usage_limit}
                    onChange={(e) => setCouponForm({ ...couponForm, usage_limit: Number(e.target.value) })}
                    className="w-full px-3.5 py-2 liquid-input rounded-xl text-neutral-900 dark:text-neutral-100"
                  />
                </div>
              </div>

              <div className="flex justify-end gap-3 pt-3 border-t border-neutral-200/60 dark:border-neutral-800">
                <button
                  type="button"
                  onClick={() => setShowCouponModal(false)}
                  className="px-4 py-2 liquid-pill text-xs font-semibold text-neutral-700 dark:text-neutral-300 hover:text-neutral-900 dark:hover:text-white transition-colors"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-5 py-2 liquid-btn-gold text-neutral-950 uppercase tracking-wider font-bold rounded-xl shadow-md transition-all"
                >
                  Publish Code
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* ========================================================= */}
      {/* MODAL 6: ADD CATEGORY */}
      {/* ========================================================= */}
      {showCategoryModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-md p-4 animate-in fade-in">
          <div className="liquid-glass bg-white dark:bg-[#141312] border border-white/80 dark:border-white/10 max-w-md w-full rounded-2xl shadow-2xl p-6 space-y-4 text-xs">
            <div className="flex items-center justify-between pb-3 border-b border-neutral-200/60 dark:border-neutral-800">
              <h3 className="font-serif font-bold text-base text-neutral-900 dark:text-neutral-100">
                Create Category
              </h3>
              <button onClick={() => setShowCategoryModal(false)} className="text-neutral-400 hover:text-neutral-900 dark:hover:text-white transition-colors">
                <X size={18} />
              </button>
            </div>

            <form onSubmit={handleCreateCategory} className="space-y-3">
              <div>
                <label className="text-[11px] font-semibold text-neutral-700 dark:text-neutral-300 block mb-1 uppercase tracking-wider">Category Name *</label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Silk Loungewear"
                  value={categoryForm.name}
                  onChange={(e) => setCategoryForm({ ...categoryForm, name: e.target.value })}
                  className="w-full px-3.5 py-2 liquid-input rounded-xl text-neutral-900 dark:text-neutral-100"
                />
              </div>

              <div>
                <label className="text-[11px] font-semibold text-neutral-700 dark:text-neutral-300 block mb-1 uppercase tracking-wider">Banner Image URL *</label>
                <input
                  type="url"
                  required
                  value={categoryForm.image_url}
                  onChange={(e) => setCategoryForm({ ...categoryForm, image_url: e.target.value })}
                  className="w-full px-3.5 py-2 liquid-input rounded-xl text-neutral-900 dark:text-neutral-100 font-mono text-[11px]"
                />
              </div>

              <div>
                <label className="text-[11px] font-semibold text-neutral-700 dark:text-neutral-300 block mb-1 uppercase tracking-wider">Description</label>
                <textarea
                  rows={2}
                  value={categoryForm.description}
                  onChange={(e) => setCategoryForm({ ...categoryForm, description: e.target.value })}
                  className="w-full px-3.5 py-2 liquid-input rounded-xl text-neutral-900 dark:text-neutral-100"
                />
              </div>

              <div className="flex justify-end gap-3 pt-3 border-t border-neutral-200/60 dark:border-neutral-800">
                <button
                  type="button"
                  onClick={() => setShowCategoryModal(false)}
                  className="px-4 py-2 liquid-pill text-xs font-semibold text-neutral-700 dark:text-neutral-300 hover:text-neutral-900 dark:hover:text-white transition-colors"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-5 py-2 liquid-btn-gold text-neutral-950 uppercase tracking-wider font-bold rounded-xl shadow-md transition-all"
                >
                  Save Category
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

    </div>
  );
};
