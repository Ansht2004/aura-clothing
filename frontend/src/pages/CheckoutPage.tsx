import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { 
  CheckCircle2, CreditCard, ShieldCheck, MapPin, 
  Truck, ArrowRight, AlertCircle, Plus, ChevronRight, Sparkles 
} from 'lucide-react';
import { api } from '../services/api';
import { Address } from '../types';
import { useCart } from '../context/CartContext';
import { useAuth } from '../context/AuthContext';
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import { ImageWithFallback } from '../components/common/ImageWithFallback';
import { formatPrice } from '../utils/formatters';

export const CheckoutPage: React.FC = () => {
  const { items, summary, appliedCoupon, refreshCart } = useCart();
  const { isAuthenticated, user } = useAuth();
  const navigate = useNavigate();

  const [addresses, setAddresses] = useState<Address[]>([]);
  const [selectedAddressId, setSelectedAddressId] = useState<number | null>(null);
  const [paymentMethod, setPaymentMethod] = useState<'card' | 'upi' | 'netbanking' | 'cod'>('card');
  const [orderNotes, setOrderNotes] = useState<string>('');

  // Payment form simulation
  const [cardNumber, setCardNumber] = useState('4242 •••• •••• 4242');
  const [cardExpiry, setCardExpiry] = useState('12/28');
  const [cardCvv, setCardCvv] = useState('888');
  const [upiId, setUpiId] = useState('');

  // New address modal / inline form
  const [showNewAddress, setShowNewAddress] = useState(false);
  const [newAddress, setNewAddress] = useState({
    full_name: user?.full_name || '',
    phone: user?.phone || '',
    address_line1: '',
    address_line2: '',
    city: '',
    state: '',
    postal_code: '',
    country: 'India',
    is_default: false
  });

  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [errorMessage, setErrorMessage] = useState<string>('');

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/auth?redirect=/checkout');
      return;
    }

    const loadAddresses = async () => {
      try {
        const res = await api.getAddresses();
        const addrs: Address[] = res.addresses || [];
        setAddresses(addrs);
        if (addrs.length > 0) {
          const defaultAddr = addrs.find(a => a.is_default) || addrs[0];
          setSelectedAddressId(defaultAddr.id);
        } else {
          setShowNewAddress(true);
        }
      } catch (err) {
        console.error("Failed to load addresses:", err);
      } finally {
        setIsLoading(false);
      }
    };

    loadAddresses();
  }, [isAuthenticated, navigate]);

  const handleCreateAddress = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await api.addAddress(newAddress);
      const created = res.address;
      setAddresses([created, ...addresses]);
      setSelectedAddressId(created.id);
      setShowNewAddress(false);
      setNewAddress({
        full_name: '',
        phone: '',
        address_line1: '',
        address_line2: '',
        city: '',
        state: '',
        postal_code: '',
        country: 'India',
        is_default: false
      });
    } catch (err: any) {
      setErrorMessage(err.message || 'Failed to add address');
    }
  };

  const handlePlaceOrder = async () => {
    if (!selectedAddressId) {
      setErrorMessage("Please select or add a delivery address.");
      return;
    }

    setIsSubmitting(true);
    setErrorMessage('');

    try {
      const res = await api.createOrder({
        address_id: selectedAddressId,
        payment_method: paymentMethod,
        coupon_code: appliedCoupon?.code,
        notes: orderNotes
      });

      await refreshCart();
      navigate(`/order-confirmation/${res.order.id}`);
    } catch (err: any) {
      setErrorMessage(err.message || 'Order placement failed. Please verify your details.');
      setIsSubmitting(false);
    }
  };

  if (isLoading) {
    return <LoadingSpinner fullPage message="Preparing Secure Checkout..." />;
  }

  if (items.length === 0) {
    return (
      <div className="max-w-2xl mx-auto px-4 py-20 text-center">
        <div className="liquid-glass rounded-3xl p-10 border border-white/70 dark:border-white/10 shadow-2xl">
          <h2 className="text-xl font-serif font-bold text-neutral-900 dark:text-neutral-100 mb-2">No Items in Checkout</h2>
          <p className="text-xs text-neutral-500 dark:text-neutral-400 mb-6 font-medium">Your shopping bag is empty. Please add items before checking out.</p>
          <Link to="/products" className="px-6 py-2.5 liquid-btn-gold text-neutral-950 text-xs uppercase tracking-wider font-bold rounded-full shadow-md">
            Return to Atelier
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12 space-y-8">
      {/* Checkout Breadcrumb */}
      <div className="flex items-center space-x-2 text-xs text-neutral-400 font-medium">
        <Link to="/cart" className="hover:text-aura-gold transition-colors">Shopping Bag</Link>
        <ChevronRight size={12} />
        <span className="text-neutral-900 dark:text-neutral-100 font-bold">Secure Atelier Checkout</span>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 sm:gap-10">
        
        {/* Left 2 Cols: Step-by-Step Checkout Flow */}
        <div className="lg:col-span-2 space-y-8">
          
          {/* STEP 1: Delivery Address */}
          <div className="liquid-glass rounded-3xl p-6 sm:p-8 border border-white/70 dark:border-white/10 shadow-xl">
            <div className="flex items-center justify-between pb-4 border-b border-neutral-200/50 dark:border-neutral-800/60">
              <div className="flex items-center gap-3">
                <div className="w-7 h-7 rounded-full liquid-btn-gold text-neutral-950 flex items-center justify-center text-xs font-bold shadow-sm">
                  1
                </div>
                <h3 className="font-serif font-bold text-lg text-neutral-900 dark:text-neutral-100">
                  Delivery Destination
                </h3>
              </div>
              {!showNewAddress && (
                <button
                  onClick={() => setShowNewAddress(true)}
                  className="text-xs text-aura-gold hover:underline font-bold flex items-center gap-1"
                >
                  <Plus size={13} /> Add Destination
                </button>
              )}
            </div>

            {/* Existing Address Selection */}
            {!showNewAddress ? (
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mt-5">
                {addresses.map((addr) => {
                  const isSelected = selectedAddressId === addr.id;
                  return (
                    <div
                      key={addr.id}
                      onClick={() => setSelectedAddressId(addr.id)}
                      className={`p-5 rounded-2xl liquid-glass border cursor-pointer transition-all ${
                        isSelected 
                          ? 'border-aura-gold ring-2 ring-aura-gold/50 shadow-md scale-102' 
                          : 'border-white/60 dark:border-white/10 hover:border-aura-gold/50'
                      }`}
                    >
                      <div className="flex items-start justify-between">
                        <span className="text-sm font-bold text-neutral-900 dark:text-neutral-100">{addr.full_name}</span>
                        {addr.is_default && (
                          <span className="text-[10px] bg-gradient-to-r from-aura-gold to-aura-goldLight text-neutral-950 font-bold px-2 py-0.5 rounded-full">
                            Default
                          </span>
                        )}
                      </div>
                      <p className="text-xs text-neutral-600 dark:text-neutral-300 mt-2 leading-relaxed">
                        {addr.address_line1} {addr.address_line2 && `, ${addr.address_line2}`}<br />
                        {addr.city}, {addr.state} {addr.postal_code}<br />
                        {addr.country}
                      </p>
                      <p className="text-[11px] text-neutral-400 font-mono mt-2.5">
                        Phone: {addr.phone}
                      </p>
                    </div>
                  );
                })}
              </div>
            ) : (
              /* New Address Form */
              <form onSubmit={handleCreateAddress} className="mt-5 space-y-4 text-xs">
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
                    <label className="text-[11px] uppercase tracking-wider font-bold text-neutral-700 dark:text-neutral-300 block mb-1">
                      Recipient Full Name *
                    </label>
                    <input
                      type="text"
                      required
                      value={newAddress.full_name}
                      onChange={(e) => setNewAddress({ ...newAddress, full_name: e.target.value })}
                      className="w-full px-4 py-2.5 liquid-input text-neutral-900 dark:text-white rounded-xl"
                    />
                  </div>
                  <div>
                    <label className="text-[11px] uppercase tracking-wider font-bold text-neutral-700 dark:text-neutral-300 block mb-1">
                      Contact Phone *
                    </label>
                    <input
                      type="tel"
                      required
                      value={newAddress.phone}
                      onChange={(e) => setNewAddress({ ...newAddress, phone: e.target.value })}
                      className="w-full px-4 py-2.5 liquid-input text-neutral-900 dark:text-white rounded-xl"
                    />
                  </div>
                </div>

                <div>
                  <label className="text-[11px] uppercase tracking-wider font-bold text-neutral-700 dark:text-neutral-300 block mb-1">
                    Street Address *
                  </label>
                  <input
                    type="text"
                    required
                    placeholder="Apartment, building, road name"
                    value={newAddress.address_line1}
                    onChange={(e) => setNewAddress({ ...newAddress, address_line1: e.target.value })}
                    className="w-full px-4 py-2.5 liquid-input text-neutral-900 dark:text-white rounded-xl"
                  />
                </div>

                <div className="grid grid-cols-3 gap-3">
                  <div>
                    <label className="text-[11px] uppercase tracking-wider font-bold text-neutral-700 dark:text-neutral-300 block mb-1">
                      City *
                    </label>
                    <input
                      type="text"
                      required
                      value={newAddress.city}
                      onChange={(e) => setNewAddress({ ...newAddress, city: e.target.value })}
                      className="w-full px-4 py-2.5 liquid-input text-neutral-900 dark:text-white rounded-xl"
                    />
                  </div>
                  <div>
                    <label className="text-[11px] uppercase tracking-wider font-bold text-neutral-700 dark:text-neutral-300 block mb-1">
                      State *
                    </label>
                    <input
                      type="text"
                      required
                      value={newAddress.state}
                      onChange={(e) => setNewAddress({ ...newAddress, state: e.target.value })}
                      className="w-full px-4 py-2.5 liquid-input text-neutral-900 dark:text-white rounded-xl"
                    />
                  </div>
                  <div>
                    <label className="text-[11px] uppercase tracking-wider font-bold text-neutral-700 dark:text-neutral-300 block mb-1">
                      Postal Code *
                    </label>
                    <input
                      type="text"
                      required
                      value={newAddress.postal_code}
                      onChange={(e) => setNewAddress({ ...newAddress, postal_code: e.target.value })}
                      className="w-full px-4 py-2.5 liquid-input text-neutral-900 dark:text-white rounded-xl"
                    />
                  </div>
                </div>

                <div className="flex items-center justify-end gap-3 pt-3 border-t border-neutral-200/50 dark:border-neutral-800/60">
                  {addresses.length > 0 && (
                    <button
                      type="button"
                      onClick={() => setShowNewAddress(false)}
                      className="px-5 py-2.5 liquid-pill text-neutral-700 dark:text-neutral-300 text-xs font-bold"
                    >
                      Cancel
                    </button>
                  )}
                  <button
                    type="submit"
                    className="px-6 py-2.5 liquid-btn-gold text-neutral-950 text-xs uppercase tracking-wider font-bold rounded-xl shadow-md"
                  >
                    Save Destination
                  </button>
                </div>
              </form>
            )}
          </div>

          {/* STEP 2: Shipping Method */}
          <div className="liquid-glass rounded-3xl p-6 sm:p-8 border border-white/70 dark:border-white/10 shadow-xl">
            <div className="flex items-center gap-3 pb-4 border-b border-neutral-200/50 dark:border-neutral-800/60">
              <div className="w-7 h-7 rounded-full liquid-btn-gold text-neutral-950 flex items-center justify-center text-xs font-bold shadow-sm">
                2
              </div>
              <h3 className="font-serif font-bold text-lg text-neutral-900 dark:text-neutral-100">
                Courier Service
              </h3>
            </div>

            <div className="mt-4 p-5 rounded-2xl liquid-glass border border-aura-gold/50 flex items-center justify-between">
              <div className="flex items-center gap-3.5">
                <div className="w-10 h-10 rounded-full liquid-pill flex items-center justify-center text-aura-gold">
                  <Truck size={20} />
                </div>
                <div>
                  <h4 className="text-xs font-bold text-neutral-900 dark:text-neutral-100">Aura Express Air Logistics</h4>
                  <p className="text-[11px] text-neutral-500 dark:text-neutral-400">Tracked Courier Delivery (3-5 business days)</p>
                </div>
              </div>
              <span className="text-xs font-bold text-emerald-600 dark:text-emerald-400">
                {summary.shipping === 0 ? 'COMPLIMENTARY' : formatPrice(summary.shipping)}
              </span>
            </div>
          </div>

          {/* STEP 3: Payment Simulation */}
          <div className="liquid-glass rounded-3xl p-6 sm:p-8 border border-white/70 dark:border-white/10 shadow-xl">
            <div className="flex items-center gap-3 pb-4 border-b border-neutral-200/50 dark:border-neutral-800/60">
              <div className="w-7 h-7 rounded-full liquid-btn-gold text-neutral-950 flex items-center justify-center text-xs font-bold shadow-sm">
                3
              </div>
              <h3 className="font-serif font-bold text-lg text-neutral-900 dark:text-neutral-100">
                Payment Simulation
              </h3>
            </div>

            {/* Payment Method Selector Tabs */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5 mt-5">
              {[
                { id: 'card', label: 'Credit Card' },
                { id: 'upi', label: 'UPI / QR' },
                { id: 'netbanking', label: 'Net Banking' },
                { id: 'cod', label: 'Cash On Delivery' },
              ].map((m) => (
                <button
                  key={m.id}
                  type="button"
                  onClick={() => setPaymentMethod(m.id as any)}
                  className={`py-3 px-3 text-xs font-bold uppercase tracking-wider rounded-2xl border transition-all ${
                    paymentMethod === m.id
                      ? 'liquid-btn-gold text-neutral-950 shadow-md font-bold'
                      : 'liquid-pill text-neutral-700 dark:text-neutral-300'
                  }`}
                >
                  {m.label}
                </button>
              ))}
            </div>

            {/* Payment Details Container */}
            <div className="mt-5 p-5 liquid-glass rounded-2xl border border-white/60 dark:border-white/10">
              {paymentMethod === 'card' && (
                <div className="space-y-3.5">
                  <div>
                    <label className="text-[11px] uppercase tracking-wider font-bold text-neutral-600 dark:text-neutral-300 block mb-1">
                      Card Number
                    </label>
                    <input
                      type="text"
                      value={cardNumber}
                      onChange={(e) => setCardNumber(e.target.value)}
                      className="w-full px-4 py-2.5 text-xs liquid-input text-neutral-900 dark:text-white rounded-xl font-mono"
                    />
                  </div>
                  <div className="grid grid-cols-2 gap-3">
                    <div>
                      <label className="text-[11px] uppercase tracking-wider font-bold text-neutral-600 dark:text-neutral-300 block mb-1">
                        Expiry Date
                      </label>
                      <input
                        type="text"
                        value={cardExpiry}
                        onChange={(e) => setCardExpiry(e.target.value)}
                        className="w-full px-4 py-2.5 text-xs liquid-input text-neutral-900 dark:text-white rounded-xl font-mono"
                      />
                    </div>
                    <div>
                      <label className="text-[11px] uppercase tracking-wider font-bold text-neutral-600 dark:text-neutral-300 block mb-1">
                        CVV / CVC
                      </label>
                      <input
                        type="password"
                        value={cardCvv}
                        onChange={(e) => setCardCvv(e.target.value)}
                        className="w-full px-4 py-2.5 text-xs liquid-input text-neutral-900 dark:text-white rounded-xl font-mono"
                      />
                    </div>
                  </div>
                  <p className="text-[10px] text-neutral-400">
                    Simulated Sandbox Payment: Test credentials loaded for instant authorization.
                  </p>
                </div>
              )}

              {paymentMethod === 'upi' && (
                <div className="space-y-2">
                  <label className="text-[11px] uppercase tracking-wider font-bold text-neutral-600 dark:text-neutral-300 block">
                    Virtual Payment Address (VPA) / UPI ID
                  </label>
                  <input
                    type="text"
                    value={upiId}
                    onChange={(e) => setUpiId(e.target.value)}
                    className="w-full px-4 py-2.5 text-xs liquid-input text-neutral-900 dark:text-white rounded-xl font-mono"
                  />
                  <p className="text-[10px] text-neutral-400">
                    Instant verification with Google Pay, PhonePe, Paytm, or BHIM.
                  </p>
                </div>
              )}

              {paymentMethod === 'netbanking' && (
                <div className="text-xs text-neutral-600 dark:text-neutral-400">
                  <label className="text-[11px] uppercase tracking-wider font-bold text-neutral-600 dark:text-neutral-300 block mb-1">
                    Select Financial Institution
                  </label>
                  <select className="w-full px-4 py-2.5 liquid-input text-neutral-900 dark:text-white rounded-xl text-xs font-semibold">
                    <option className="bg-white dark:bg-neutral-900">HDFC Bank</option>
                    <option className="bg-white dark:bg-neutral-900">ICICI Bank</option>
                    <option className="bg-white dark:bg-neutral-900">State Bank of India</option>
                    <option className="bg-white dark:bg-neutral-900">Axis Bank</option>
                    <option className="bg-white dark:bg-neutral-900">Kotak Mahindra Bank</option>
                  </select>
                </div>
              )}

              {paymentMethod === 'cod' && (
                <div className="text-xs text-neutral-600 dark:text-neutral-300 space-y-1">
                  <p className="font-bold text-neutral-900 dark:text-neutral-100">Cash on Delivery</p>
                  <p>Pay upon delivery to our Aura logistics courier representative in cash or QR scan.</p>
                </div>
              )}
            </div>

            {/* Special Instructions */}
            <div className="mt-4">
              <label className="text-[11px] uppercase tracking-wider font-bold text-neutral-700 dark:text-neutral-300 block mb-1">
                Order Notes / Delivery Instructions (Optional)
              </label>
              <textarea
                rows={2}
                value={orderNotes}
                onChange={(e) => setOrderNotes(e.target.value)}
                placeholder="Gate code, concierge instructions, special gift packaging..."
                className="w-full px-4 py-2.5 text-xs liquid-input text-neutral-900 dark:text-white rounded-xl"
              />
            </div>
          </div>

        </div>

        {/* Right Col: Order Summary & Place Order Button - Sticky Liquid Glass */}
        <div>
          <div className="liquid-glass rounded-3xl p-6 sm:p-8 border border-white/80 dark:border-white/10 shadow-2xl sticky top-28 space-y-6">
            <h3 className="font-serif font-bold text-xl text-neutral-900 dark:text-neutral-100 pb-3 border-b border-neutral-200/50 dark:border-neutral-800/60">
              Review & Place Order
            </h3>

            {/* Items Mini List */}
            <div className="max-h-48 overflow-y-auto divide-y divide-neutral-200/40 dark:divide-neutral-800/40 pr-1">
              {items.map((item) => (
                <div key={item.id} className="py-2.5 flex items-center justify-between text-xs">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-12 liquid-glass rounded-lg overflow-hidden p-0.5 shrink-0 border border-white/60">
                      <ImageWithFallback src={item.primary_image} alt={item.product_name} className="w-full h-full object-cover rounded-md" />
                    </div>
                    <div>
                      <p className="font-bold text-neutral-900 dark:text-neutral-100 truncate max-w-[150px]">{item.product_name}</p>
                      <p className="text-[10px] text-neutral-400">{item.size} • Qty {item.quantity}</p>
                    </div>
                  </div>
                  <span className="font-bold text-neutral-900 dark:text-neutral-100 font-mono">{formatPrice(item.total_price)}</span>
                </div>
              ))}
            </div>

            {/* Cost Breakdown */}
            <div className="pt-3 border-t border-neutral-200/50 dark:border-neutral-800/60 space-y-2 text-xs text-neutral-600 dark:text-neutral-400">
              <div className="flex justify-between">
                <span>Subtotal</span>
                <span className="font-mono">{formatPrice(summary.subtotal)}</span>
              </div>
              {appliedCoupon && (
                <div className="flex justify-between text-emerald-600 dark:text-emerald-400 font-semibold">
                  <span>Coupon ({appliedCoupon.code})</span>
                  <span className="font-mono">-{formatPrice(appliedCoupon.discount_amount)}</span>
                </div>
              )}
              <div className="flex justify-between">
                <span>Estimated GST (12%)</span>
                <span className="font-mono">{formatPrice(summary.tax)}</span>
              </div>
              <div className="flex justify-between">
                <span>Courier Logistics</span>
                <span>{summary.shipping === 0 ? 'FREE' : formatPrice(summary.shipping)}</span>
              </div>
              <div className="pt-3 border-t border-neutral-200/50 dark:border-neutral-800/60 flex justify-between items-baseline">
                <span className="font-bold text-sm text-neutral-900 dark:text-neutral-100">Total Payable</span>
                <span className="font-serif font-bold text-2xl text-neutral-900 dark:text-neutral-100 font-mono text-aura-gold">{formatPrice(summary.total)}</span>
              </div>
            </div>

            {errorMessage && (
              <div className="p-3.5 bg-rose-500/15 border border-rose-500/30 text-rose-700 dark:text-rose-300 text-xs rounded-2xl flex items-center gap-2 animate-in fade-in">
                <AlertCircle size={16} />
                <span>{errorMessage}</span>
              </div>
            )}

            <button
              disabled={isSubmitting || !selectedAddressId}
              onClick={handlePlaceOrder}
              className="w-full py-4 liquid-btn-gold text-neutral-950 text-xs uppercase tracking-widest font-bold rounded-2xl shadow-xl transition-all flex items-center justify-center gap-2 group disabled:opacity-40"
            >
              {isSubmitting ? (
                <span>Authorizing Order...</span>
              ) : (
                <>
                  <span>Place Order • {formatPrice(summary.total)}</span>
                  <ArrowRight size={15} className="group-hover:translate-x-1 transition-transform" />
                </>
              )}
            </button>

            <div className="flex items-center justify-center gap-2 text-[11px] text-neutral-400 pt-1">
              <ShieldCheck size={14} className="text-aura-gold" />
              <span>Zero-Risk Guarantee & Instant Order Tracking</span>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
};
