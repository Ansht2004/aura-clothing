import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { 
  Package, Truck, Clock, CheckCircle, XCircle, 
  RefreshCw, AlertCircle, Eye, Printer, X, Sparkles 
} from 'lucide-react';
import { api } from '../services/api';
import { Order } from '../types';
import { useAuth } from '../context/AuthContext';
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import { EmptyState } from '../components/common/EmptyState';
import { ImageWithFallback } from '../components/common/ImageWithFallback';
import { formatPrice } from '../utils/formatters';

export const OrderHistoryPage: React.FC = () => {
  const { isAuthenticated, isLoading: authLoading } = useAuth();
  const navigate = useNavigate();
  const [orders, setOrders] = useState<Order[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  // Cancellation Modal State
  const [cancelModalOrder, setCancelModalOrder] = useState<Order | null>(null);
  const [cancelReason, setCancelReason] = useState<string>('Changed mind before shipment');
  const [isCancelling, setIsCancelling] = useState<boolean>(false);

  // Return/Refund Modal State
  const [returnModalOrder, setReturnModalOrder] = useState<Order | null>(null);
  const [requestType, setRequestType] = useState<'return' | 'refund'>('return');
  const [returnReason, setReturnReason] = useState<string>('Size does not fit as expected');
  const [customerNotes, setCustomerNotes] = useState<string>('');
  const [isSubmittingReturn, setIsSubmittingReturn] = useState<boolean>(false);

  // Feedback notifications
  const [feedback, setFeedback] = useState<{ type: 'success' | 'error'; message: string } | null>(null);

  const fetchOrders = async () => {
    setIsLoading(true);
    try {
      const res = await api.getOrders();
      setOrders(res.orders || []);
    } catch (err) {
      console.error("Failed to load customer orders:", err);
      setOrders([]);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      setOrders([]);
      navigate('/auth', { replace: true });
      return;
    }

    if (isAuthenticated) {
      fetchOrders();
    } else {
      setOrders([]);
    }
  }, [isAuthenticated, authLoading, navigate]);

  if (authLoading) {
    return <LoadingSpinner fullPage message="Accessing Order History..." />;
  }

  if (!isAuthenticated) {
    return null;
  }

  const handleConfirmCancel = async () => {
    if (!cancelModalOrder) return;
    setIsCancelling(true);
    try {
      await api.cancelOrder(cancelModalOrder.id, cancelReason);
      setFeedback({ type: 'success', message: `Order ${cancelModalOrder.order_number} cancelled successfully. Full refund initiated.` });
      setCancelModalOrder(null);
      await fetchOrders();
    } catch (err: any) {
      setFeedback({ type: 'error', message: err.message || 'Failed to cancel order.' });
    } finally {
      setIsCancelling(false);
    }
  };

  const handleConfirmReturn = async () => {
    if (!returnModalOrder) return;
    setIsSubmittingReturn(true);
    try {
      await api.submitReturnRequest(returnModalOrder.id, {
        request_type: requestType,
        reason: returnReason,
        customer_notes: customerNotes
      });
      setFeedback({ 
        type: 'success', 
        message: `Your ${requestType} request for ${returnModalOrder.order_number} has been logged. Our concierge will review it within 24 hours.` 
      });
      setReturnModalOrder(null);
      setCustomerNotes('');
      await fetchOrders();
    } catch (err: any) {
      setFeedback({ type: 'error', message: err.message || 'Failed to submit return request.' });
    } finally {
      setIsSubmittingReturn(false);
    }
  };

  if (isLoading && orders.length === 0) {
    return <LoadingSpinner fullPage message="Retrieving Order Records..." />;
  }

  if (orders.length === 0) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-20">
        <div className="liquid-glass rounded-3xl p-12 text-center border border-white/70 dark:border-white/10 shadow-2xl">
          <EmptyState
            icon={Package}
            title="No orders found"
            description="You haven't placed any apparel orders yet. Browse our collections to begin curating your wardrobe."
            actionText="Browse Apparel"
            actionLink="/products"
          />
        </div>
      </div>
    );
  }

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'delivered':
        return <span className="px-3 py-1 bg-emerald-500/15 border border-emerald-500/30 text-emerald-700 dark:text-emerald-300 text-[10px] font-bold uppercase tracking-wider rounded-full">Delivered</span>;
      case 'shipped':
        return <span className="px-3 py-1 bg-sky-500/15 border border-sky-500/30 text-sky-700 dark:text-sky-300 text-[10px] font-bold uppercase tracking-wider rounded-full">In Transit</span>;
      case 'processing':
        return <span className="px-3 py-1 bg-amber-500/15 border border-amber-500/30 text-amber-700 dark:text-amber-300 text-[10px] font-bold uppercase tracking-wider rounded-full animate-pulse">Processing</span>;
      case 'cancelled':
        return <span className="px-3 py-1 bg-neutral-500/15 border border-neutral-500/30 text-neutral-500 text-[10px] font-bold uppercase tracking-wider rounded-full">Cancelled</span>;
      default:
        return <span className="px-3 py-1 liquid-pill text-neutral-700 dark:text-neutral-300 text-[10px] font-bold uppercase tracking-wider">{status}</span>;
    }
  };

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12 space-y-8">
      {/* Header Banner */}
      <div className="liquid-glass rounded-3xl p-6 sm:p-8 border border-white/70 dark:border-white/10 shadow-xl">
        <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full liquid-pill text-[10px] uppercase tracking-[0.2em] text-aura-gold font-bold">
          <Sparkles size={12} /> Client Atelier History
        </span>
        <h1 className="text-2xl sm:text-4xl font-serif font-bold text-neutral-900 dark:text-neutral-100 mt-2">
          Purchase History & Returns
        </h1>
        <p className="text-xs text-neutral-500 dark:text-neutral-400 mt-1 font-medium">
          Review, track, and manage your past garments and return authorizations.
        </p>
      </div>

      {feedback && (
        <div className={`p-4 rounded-2xl text-xs flex items-center justify-between font-semibold ${
          feedback.type === 'success' 
            ? 'bg-emerald-500/15 text-emerald-700 dark:text-emerald-300 border border-emerald-500/30' 
            : 'bg-rose-500/15 text-rose-700 dark:text-rose-300 border border-rose-500/30'
        }`}>
          <span>{feedback.message}</span>
          <button onClick={() => setFeedback(null)}><X size={15} /></button>
        </div>
      )}

      {/* Orders List */}
      <div className="space-y-6">
        {orders.map((order) => {
          const canCancel = ['pending', 'processing'].includes(order.status);
          const canReturn = order.status === 'delivered';

          return (
            <div key={order.id} className="liquid-glass rounded-3xl border border-white/70 dark:border-white/10 shadow-xl overflow-hidden">
              
              {/* Order Card Header */}
              <div className="p-5 sm:p-6 border-b border-neutral-200/50 dark:border-neutral-800/60 flex flex-wrap items-center justify-between gap-4 text-xs">
                <div className="flex flex-wrap items-center gap-6">
                  <div>
                    <span className="text-neutral-400 block text-[10px] uppercase tracking-wider font-bold">Order Identifier</span>
                    <span className="font-mono font-bold text-neutral-900 dark:text-neutral-100 text-sm">{order.order_number}</span>
                  </div>
                  <div>
                    <span className="text-neutral-400 block text-[10px] uppercase tracking-wider font-bold">Date Placed</span>
                    <span className="text-neutral-700 dark:text-neutral-300 font-medium">{new Date(order.created_at).toLocaleDateString()}</span>
                  </div>
                  <div>
                    <span className="text-neutral-400 block text-[10px] uppercase tracking-wider font-bold">Total Amount</span>
                    <span className="text-neutral-900 dark:text-neutral-100 font-bold font-mono">{formatPrice(order.total_amount)}</span>
                  </div>
                </div>

                <div className="flex items-center gap-3">
                  {getStatusBadge(order.status)}
                  <Link
                    to={`/order-confirmation/${order.id}`}
                    className="w-8 h-8 rounded-full liquid-pill flex items-center justify-center text-neutral-600 dark:text-neutral-300 hover:text-aura-gold transition-colors"
                    title="View Receipt"
                  >
                    <Eye size={15} />
                  </Link>
                </div>
              </div>

              {/* Order Items Body */}
              <div className="p-5 sm:p-6 divide-y divide-neutral-200/40 dark:divide-neutral-800/40">
                {order.items?.map((item) => (
                  <div key={item.id} className="py-3.5 first:pt-0 last:pb-0 flex items-center justify-between gap-4 text-xs">
                    <div className="flex items-center gap-4">
                      {item.image_url && (
                        <div className="w-14 aspect-[3/4] liquid-glass rounded-xl overflow-hidden p-0.5 shrink-0 border border-white/60">
                          <ImageWithFallback src={item.image_url} alt={item.product_name} className="w-full h-full object-cover rounded-lg" />
                        </div>
                      )}
                      <div>
                        <h4 className="font-bold text-neutral-900 dark:text-neutral-100 text-sm">{item.product_name}</h4>
                        <p className="text-neutral-500 dark:text-neutral-400 mt-0.5 text-xs">
                          Size: <strong>{item.variant_size}</strong> • Color: <strong>{item.variant_color}</strong> • Quantity: <strong>{item.quantity}</strong>
                        </p>
                        <p className="text-[10px] text-neutral-400 font-mono mt-0.5">SKU: {item.sku}</p>
                      </div>
                    </div>
                    <span className="font-bold text-neutral-900 dark:text-neutral-100 font-mono">{formatPrice(item.total_price)}</span>
                  </div>
                ))}
              </div>

              {/* Order Tracking & Action Footer */}
              <div className="p-4 sm:p-5 border-t border-neutral-200/50 dark:border-neutral-800/60 flex flex-wrap items-center justify-between gap-3 text-xs bg-white/20 dark:bg-black/20">
                <div className="flex items-center gap-2 text-neutral-600 dark:text-neutral-400">
                  <Truck size={15} className="text-aura-gold" />
                  <span>Courier: <strong className="text-neutral-900 dark:text-neutral-100">{order.carrier_name || 'Aura Express Logistics'}</strong></span>
                  <span>•</span>
                  <span className="font-mono">Tracking: <strong className="text-aura-gold">{order.tracking_number || 'TRK-PENDING'}</strong></span>
                </div>

                <div className="flex items-center gap-2">
                  {canCancel && (
                    <button
                      onClick={() => setCancelModalOrder(order)}
                      className="px-4 py-2 rounded-xl border border-rose-300 dark:border-rose-900/60 text-rose-600 dark:text-rose-400 hover:bg-rose-500/10 text-xs uppercase tracking-wider font-bold transition-all shadow-sm"
                    >
                      Cancel Order
                    </button>
                  )}

                  {canReturn && (
                    <button
                      onClick={() => setReturnModalOrder(order)}
                      className="px-4 py-2 liquid-pill text-neutral-800 dark:text-neutral-200 hover:border-aura-gold text-xs uppercase tracking-wider font-bold transition-all flex items-center gap-1.5 shadow-sm"
                    >
                      <RefreshCw size={13} />
                      Request Return / Refund
                    </button>
                  )}
                </div>
              </div>

            </div>
          );
        })}
      </div>

      {/* Cancellation Modal Dialog - Liquid Glass */}
      {cancelModalOrder && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-md p-4 animate-in fade-in">
          <div className="liquid-glass border border-white/80 dark:border-white/10 max-w-md w-full rounded-3xl shadow-2xl p-6 sm:p-8 space-y-4">
            <div className="flex items-center justify-between pb-3 border-b border-neutral-200/50 dark:border-neutral-800/60">
              <h3 className="font-serif font-bold text-lg text-neutral-900 dark:text-neutral-100">
                Cancel Order {cancelModalOrder.order_number}
              </h3>
              <button onClick={() => setCancelModalOrder(null)} className="w-8 h-8 rounded-full liquid-pill flex items-center justify-center text-neutral-500 hover:text-neutral-900 dark:hover:text-neutral-100"><X size={16} /></button>
            </div>

            <p className="text-xs text-neutral-600 dark:text-neutral-300 leading-relaxed font-normal">
              Are you sure you wish to cancel this order? Garment stock will be immediately restored to our inventory and your full payment of <strong>{formatPrice(cancelModalOrder.total_amount)}</strong> will be refunded within 3 business days.
            </p>

            <div>
              <label className="text-[11px] uppercase tracking-wider font-bold text-neutral-700 dark:text-neutral-300 block mb-1">
                Reason for Cancellation
              </label>
              <select
                value={cancelReason}
                onChange={(e) => setCancelReason(e.target.value)}
                className="w-full px-3.5 py-2.5 text-xs liquid-input text-neutral-900 dark:text-white rounded-xl font-medium"
              >
                <option className="bg-white dark:bg-neutral-900">Changed mind before shipment</option>
                <option className="bg-white dark:bg-neutral-900">Ordered incorrect size or color</option>
                <option className="bg-white dark:bg-neutral-900">Found alternate wardrobe piece</option>
                <option className="bg-white dark:bg-neutral-900">Shipping address error</option>
                <option className="bg-white dark:bg-neutral-900">Other reason</option>
              </select>
            </div>

            <div className="flex justify-end gap-3 pt-3 border-t border-neutral-200/50 dark:border-neutral-800/60">
              <button
                onClick={() => setCancelModalOrder(null)}
                className="px-5 py-2.5 liquid-pill text-xs font-bold text-neutral-700 dark:text-neutral-300"
              >
                Keep Order
              </button>
              <button
                disabled={isCancelling}
                onClick={handleConfirmCancel}
                className="px-6 py-2.5 bg-rose-600 hover:bg-rose-700 text-white text-xs uppercase tracking-wider font-bold rounded-xl shadow-md transition-colors"
              >
                {isCancelling ? 'Cancelling...' : 'Confirm Cancellation'}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Return / Refund Request Modal Dialog - Liquid Glass */}
      {returnModalOrder && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-md p-4 animate-in fade-in">
          <div className="liquid-glass border border-white/80 dark:border-white/10 max-w-lg w-full rounded-3xl shadow-2xl p-6 sm:p-8 space-y-4">
            <div className="flex items-center justify-between pb-3 border-b border-neutral-200/50 dark:border-neutral-800/60">
              <h3 className="font-serif font-bold text-lg text-neutral-900 dark:text-neutral-100">
                Return Authorization: {returnModalOrder.order_number}
              </h3>
              <button onClick={() => setReturnModalOrder(null)} className="w-8 h-8 rounded-full liquid-pill flex items-center justify-center text-neutral-500 hover:text-neutral-900 dark:hover:text-neutral-100"><X size={16} /></button>
            </div>

            <p className="text-xs text-neutral-600 dark:text-neutral-300 leading-relaxed font-normal">
              We offer 30-day effortless returns. Garments must be unworn with original designer tags intact.
            </p>

            <div className="space-y-4">
              <div>
                <label className="text-[11px] uppercase tracking-wider font-bold text-neutral-700 dark:text-neutral-300 block mb-1">
                  Request Type
                </label>
                <div className="flex gap-4 text-xs">
                  <label className="flex items-center gap-2 cursor-pointer text-neutral-800 dark:text-neutral-200 font-medium">
                    <input
                      type="radio"
                      name="req_type"
                      checked={requestType === 'return'}
                      onChange={() => setRequestType('return')}
                      className="text-aura-gold focus:ring-aura-gold"
                    />
                    <span>Return for Exchange</span>
                  </label>
                  <label className="flex items-center gap-2 cursor-pointer text-neutral-800 dark:text-neutral-200 font-medium">
                    <input
                      type="radio"
                      name="req_type"
                      checked={requestType === 'refund'}
                      onChange={() => setRequestType('refund')}
                      className="text-aura-gold focus:ring-aura-gold"
                    />
                    <span>Full Monetary Refund</span>
                  </label>
                </div>
              </div>

              <div>
                <label className="text-[11px] uppercase tracking-wider font-bold text-neutral-700 dark:text-neutral-300 block mb-1">
                  Primary Reason *
                </label>
                <select
                  value={returnReason}
                  onChange={(e) => setReturnReason(e.target.value)}
                  className="w-full px-3.5 py-2.5 text-xs liquid-input text-neutral-900 dark:text-white rounded-xl font-medium"
                >
                  <option className="bg-white dark:bg-neutral-900">Size does not fit as expected</option>
                  <option className="bg-white dark:bg-neutral-900">Fabric drape or color differs from expectation</option>
                  <option className="bg-white dark:bg-neutral-900">Damaged or defective upon arrival</option>
                  <option className="bg-white dark:bg-neutral-900">Received incorrect item</option>
                  <option className="bg-white dark:bg-neutral-900">Other / personal preference</option>
                </select>
              </div>

              <div>
                <label className="text-[11px] uppercase tracking-wider font-bold text-neutral-700 dark:text-neutral-300 block mb-1">
                  Additional Notes (Optional)
                </label>
                <textarea
                  rows={3}
                  value={customerNotes}
                  onChange={(e) => setCustomerNotes(e.target.value)}
                  placeholder="Provide sizing observations or reason for exchange..."
                  className="w-full px-3.5 py-2.5 text-xs liquid-input text-neutral-900 dark:text-white rounded-xl font-medium"
                />
              </div>
            </div>

            <div className="flex justify-end gap-3 pt-3 border-t border-neutral-200/50 dark:border-neutral-800/60">
              <button
                onClick={() => setReturnModalOrder(null)}
                className="px-5 py-2.5 liquid-pill text-xs font-bold text-neutral-700 dark:text-neutral-300"
              >
                Cancel
              </button>
              <button
                disabled={isSubmittingReturn}
                onClick={handleConfirmReturn}
                className="px-6 py-2.5 liquid-btn-gold text-neutral-950 text-xs uppercase tracking-wider font-bold rounded-xl shadow-md transition-all"
              >
                {isSubmittingReturn ? 'Submitting...' : 'Submit Authorization'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
