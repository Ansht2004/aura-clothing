import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { CheckCircle, Truck, Package, Printer, ArrowRight, ShieldCheck, Sparkles } from 'lucide-react';
import { api } from '../services/api';
import { Order } from '../types';
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import { ImageWithFallback } from '../components/common/ImageWithFallback';
import { formatPrice } from '../utils/formatters';

export const OrderConfirmationPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [order, setOrder] = useState<Order | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  useEffect(() => {
    const fetchOrder = async () => {
      if (!id) return;
      try {
        const res = await api.getOrder(id);
        setOrder(res.order);
      } catch (err) {
        console.error("Failed to load confirmed order:", err);
      } finally {
        setIsLoading(false);
      }
    };
    fetchOrder();
  }, [id]);

  if (isLoading || !order) {
    return <LoadingSpinner fullPage message="Finalizing Order Confirmation..." />;
  }

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12 sm:py-16 space-y-8">
      {/* Success Hero Header - Liquid Glass Card */}
      <div className="liquid-glass rounded-3xl p-8 sm:p-12 text-center space-y-3 border border-white/80 dark:border-white/10 shadow-2xl">
        <div className="w-16 h-16 bg-emerald-500/15 border border-emerald-500/30 text-emerald-600 dark:text-emerald-400 rounded-full flex items-center justify-center mx-auto mb-3 shadow-lg animate-in zoom-in duration-300">
          <CheckCircle size={34} strokeWidth={2.2} />
        </div>
        <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full liquid-pill text-[10px] uppercase tracking-[0.2em] text-aura-gold font-bold">
          <Sparkles size={12} /> Acquisition Confirmed
        </span>
        <h1 className="text-3xl sm:text-5xl font-serif font-bold text-neutral-900 dark:text-neutral-100">
          Thank you for choosing Aura.
        </h1>
        <p className="text-sm text-neutral-600 dark:text-neutral-300 max-w-md mx-auto leading-relaxed">
          Your garments have been authorized and dispatched to our atelier artisans for finishing and presentation packing.
        </p>
        <div className="inline-block mt-3 liquid-pill text-neutral-800 dark:text-neutral-200 px-5 py-2 text-xs font-mono font-bold tracking-widest border border-white/80 dark:border-white/10">
          Order Identifier: {order.order_number}
        </div>
      </div>

      {/* Visual Tracking Progress Stepper - Liquid Glass */}
      <div className="liquid-glass rounded-3xl p-6 sm:p-8 border border-white/70 dark:border-white/10 shadow-xl">
        <div className="flex items-center justify-between text-xs text-neutral-500 dark:text-neutral-400 mb-6 font-semibold">
          <span className="flex items-center gap-2 text-neutral-900 dark:text-neutral-100">
            <Package size={16} className="text-aura-gold" />
            Courier: {order.carrier_name || 'Aura Express Logistics'}
          </span>
          <span className="font-mono text-aura-gold font-bold">AWB: {order.tracking_number}</span>
        </div>

        <div className="grid grid-cols-4 gap-2 text-center text-xs">
          <div className="flex flex-col items-center">
            <div className="w-9 h-9 rounded-full bg-emerald-500 text-white flex items-center justify-center text-xs font-bold mb-1 shadow-md">
              ✓
            </div>
            <span className="font-bold text-neutral-900 dark:text-neutral-100">Placed</span>
            <span className="text-[10px] text-neutral-400">Confirmed</span>
          </div>

          <div className="flex flex-col items-center">
            <div className="w-9 h-9 rounded-full bg-aura-gold text-neutral-950 flex items-center justify-center text-xs font-bold mb-1 shadow-md animate-pulse">
              2
            </div>
            <span className="font-bold text-neutral-900 dark:text-neutral-100">Processing</span>
            <span className="text-[10px] text-neutral-400">Atelier finishing</span>
          </div>

          <div className="flex flex-col items-center">
            <div className="w-9 h-9 rounded-full liquid-pill text-neutral-400 flex items-center justify-center text-xs font-bold mb-1">
              3
            </div>
            <span className="text-neutral-400 font-medium">Shipped</span>
            <span className="text-[10px] text-neutral-400">Air Transit</span>
          </div>

          <div className="flex flex-col items-center">
            <div className="w-9 h-9 rounded-full liquid-pill text-neutral-400 flex items-center justify-center text-xs font-bold mb-1">
              4
            </div>
            <span className="text-neutral-400 font-medium">Delivered</span>
            <span className="text-[10px] text-neutral-400">Client Door</span>
          </div>
        </div>
      </div>

      {/* Order Details & Summary Card - Liquid Glass */}
      <div className="liquid-glass rounded-3xl shadow-2xl p-6 sm:p-10 border border-white/80 dark:border-white/10 space-y-6">
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 pb-6 border-b border-neutral-200/50 dark:border-neutral-800/60 text-xs">
          <div>
            <h3 className="font-bold text-neutral-900 dark:text-neutral-100 uppercase tracking-widest text-[11px] mb-2 text-aura-gold">
              Delivery Destination
            </h3>
            {order.delivery_address ? (
              <p className="text-neutral-600 dark:text-neutral-300 leading-relaxed font-normal">
                <strong className="text-neutral-900 dark:text-white font-bold">{order.delivery_address.full_name}</strong><br />
                {order.delivery_address.address_line1} {order.delivery_address.address_line2 && `, ${order.delivery_address.address_line2}`}<br />
                {order.delivery_address.city}, {order.delivery_address.state} {order.delivery_address.postal_code}<br />
                Phone: {order.delivery_address.phone}
              </p>
            ) : (
              <p className="text-neutral-400">Client address on file</p>
            )}
          </div>

          <div>
            <h3 className="font-bold text-neutral-900 dark:text-neutral-100 uppercase tracking-widest text-[11px] mb-2 text-aura-gold">
              Payment & Dispatch
            </h3>
            <p className="text-neutral-600 dark:text-neutral-300 leading-relaxed font-normal">
              Payment Method: <strong className="text-neutral-900 dark:text-white font-bold">{order.payment_method.toUpperCase()}</strong><br />
              Status: <span className="text-emerald-600 dark:text-emerald-400 font-bold">{order.payment_status.toUpperCase()}</span><br />
              Order Date: {new Date(order.created_at).toLocaleDateString()}
            </p>
          </div>
        </div>

        {/* Items List */}
        <div>
          <h3 className="font-serif font-bold text-lg text-neutral-900 dark:text-neutral-100 mb-4">
            Order Pieces ({order.items?.length || 0})
          </h3>
          <div className="divide-y divide-neutral-200/40 dark:divide-neutral-800/40">
            {order.items?.map((item) => (
              <div key={item.id} className="py-3.5 flex items-center justify-between text-xs">
                <div className="flex items-center gap-3.5">
                  {item.image_url && (
                    <div className="w-12 aspect-[3/4] liquid-glass rounded-xl overflow-hidden p-0.5 shrink-0 border border-white/60">
                      <ImageWithFallback src={item.image_url} alt={item.product_name} className="w-full h-full object-cover rounded-lg" />
                    </div>
                  )}
                  <div>
                    <h4 className="font-bold text-neutral-900 dark:text-neutral-100">{item.product_name}</h4>
                    <p className="text-neutral-500 dark:text-neutral-400 text-[11px] mt-0.5">
                      Size: {item.variant_size} • Color: {item.variant_color} • Qty: {item.quantity}
                    </p>
                  </div>
                </div>
                <span className="font-bold text-neutral-900 dark:text-neutral-100 font-mono">{formatPrice(item.total_price)}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Totals */}
        <div className="pt-4 border-t border-neutral-200/50 dark:border-neutral-800/60 text-xs space-y-2 max-w-xs ml-auto">
          <div className="flex justify-between text-neutral-600 dark:text-neutral-400">
            <span>Subtotal</span>
            <span className="font-mono">{formatPrice(order.subtotal)}</span>
          </div>
          {order.discount_amount > 0 && (
            <div className="flex justify-between text-emerald-600 dark:text-emerald-400 font-semibold">
              <span>Invitation Discount ({order.coupon_code})</span>
              <span className="font-mono">-{formatPrice(order.discount_amount)}</span>
            </div>
          )}
          <div className="flex justify-between text-neutral-600 dark:text-neutral-400">
            <span>GST (12%)</span>
            <span className="font-mono">{formatPrice(order.tax_amount)}</span>
          </div>
          <div className="flex justify-between text-neutral-600 dark:text-neutral-400">
            <span>Courier Logistics</span>
            <span>{order.shipping_amount === 0 ? 'COMPLIMENTARY' : formatPrice(order.shipping_amount)}</span>
          </div>
          <div className="flex justify-between text-neutral-900 dark:text-neutral-100 font-bold text-base pt-3 border-t border-neutral-200/50 dark:border-neutral-800/60">
            <span>Total Authorized</span>
            <span className="font-mono text-aura-gold">{formatPrice(order.total_amount)}</span>
          </div>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        <button
          onClick={handlePrint}
          className="px-5 py-3 liquid-btn-glass rounded-2xl text-xs uppercase tracking-wider font-bold flex items-center gap-2 shadow-md"
        >
          <Printer size={15} /> Print / Save Tax Invoice
        </button>

        <div className="flex gap-3">
          <Link
            to="/orders"
            className="px-5 py-3 liquid-btn-glass rounded-2xl text-xs uppercase tracking-wider font-bold shadow-md"
          >
            Order History
          </Link>
          <Link
            to="/products"
            className="px-7 py-3 liquid-btn-gold text-neutral-950 text-xs uppercase tracking-wider font-bold rounded-2xl shadow-xl flex items-center gap-2 group"
          >
            <span>Continue Shopping</span>
            <ArrowRight size={14} className="group-hover:translate-x-1 transition-transform" />
          </Link>
        </div>
      </div>
    </div>
  );
};
