import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Sparkles, X, Send, Image as ImageIcon, ShoppingBag, 
  ArrowRight, RefreshCw, Eye, Check, AlertCircle 
} from 'lucide-react';
import { api } from '../../services/api';
import { formatPrice } from '../../utils/formatters';
import { ImageWithFallback } from '../common/ImageWithFallback';
import { useCart } from '../../context/CartContext';

interface Message {
  id: string;
  sender: 'concierge' | 'client';
  text: string;
  image?: string;
  products?: any[];
  timestamp: Date;
}

export const AIConciergeModal: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedImage, setSelectedImage] = useState<string | null>(null);
  const [toast, setToast] = useState<{ message: string; type: 'success' | 'info' | 'error' } | null>(null);

  const showToast = (message: string, type: 'success' | 'info' | 'error' = 'info') => {
    setToast({ message, type });
    setTimeout(() => setToast(null), 3500);
  };

  const [messages, setMessages] = useState<Message[]>([
    {
      id: 'welcome',
      sender: 'concierge',
      text: "Good day, Patron. I am your Aura Concierge Privé—your personal wardrobe architect and styling director. Allow me to assemble a bespoke capsule for your next soiree, travel retreat, or boardroom engagement.\n\nWhat mood, destination, or silhouette can I curate for you today?",
      timestamp: new Date()
    }
  ]);

  const fileInputRef = useRef<HTMLInputElement>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const navigate = useNavigate();
  const { addToCart } = useCart();

  // Listen for global custom open event from Navbar or PDP
  useEffect(() => {
    const handleOpen = () => setIsOpen(true);
    window.addEventListener('open-aura-concierge', handleOpen);
    return () => window.removeEventListener('open-aura-concierge', handleOpen);
  }, []);

  // Auto-scroll to bottom of chat
  useEffect(() => {
    if (isOpen) {
      messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages, isOpen, isLoading]);

  const handleImageSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      if (file.size > 4 * 1024 * 1024) {
        showToast('Please upload an image smaller than 4MB.', 'error');
        return;
      }
      const reader = new FileReader();
      reader.onloadend = () => {
        setSelectedImage(reader.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSendMessage = async (textToSend?: string) => {
    const query = (textToSend || inputText).trim();
    if (!query && !selectedImage) return;

    const userMsg: Message = {
      id: String(Date.now()),
      sender: 'client',
      text: query || 'Inquiring styling recommendation for this piece...',
      image: selectedImage || undefined,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMsg]);
    setInputText('');
    const sentImage = selectedImage;
    setSelectedImage(null);
    setIsLoading(true);

    try {
      const history = messages.slice(-5).map(m => ({
        role: m.sender === 'client' ? 'user' : 'model',
        content: m.text
      }));
      history.push({ role: 'user', content: query || 'Style with this attached image' });

      const res = await api.askAIConcierge(history, sentImage || undefined);

      const aiMsg: Message = {
        id: String(Date.now() + 1),
        sender: 'concierge',
        text: res.reply,
        products: res.recommended_products || [],
        timestamp: new Date()
      };
      setMessages(prev => [...prev, aiMsg]);
    } catch (err: any) {
      const errorMsg: Message = {
        id: String(Date.now() + 1),
        sender: 'concierge',
        text: "Pardon me, Patron. Our archival connection was momentarily delayed. Allow me to offer our classic quiet luxury capsule while re-synchronizing with the atelier.",
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMsg]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleQuickAdd = async (product: any) => {
    try {
      // Find default variant or first variant
      const res = await api.getProduct(product.id);
      const variants = res.product?.variants || [];
      if (variants.length > 0) {
        await addToCart(variants[0].id, 1);
        showToast(`Added ${product.name} to your shopping bag.`, 'success');
      } else {
        navigate(`/products/${product.id}`);
        setIsOpen(false);
      }
    } catch (e: any) {
      showToast('Navigating to garment details for size selection.', 'info');
      navigate(`/products/${product.id}`);
      setIsOpen(false);
    }
  };

  const handleAddEntireCapsule = async (products: any[]) => {
    let count = 0;
    for (const p of products) {
      try {
        const res = await api.getProduct(p.id);
        const variants = res.product?.variants || [];
        if (variants.length > 0) {
          await addToCart(variants[0].id, 1);
          count++;
        }
      } catch (e) {
        // Continue adding others
      }
    }
    if (count > 0) {
      showToast(`Added complete ${count}-piece ensemble to your bag.`, 'success');
    } else {
      showToast('Capsule items viewed.', 'info');
    }
  };

  const quickPrompts = [
    "Sunset garden reception in Tuscany",
    "Quiet luxury old-money aesthetic",
    "Breathable linen summer capsule",
    "Black-tie winter gala soirée"
  ];

  return (
    <>
      {/* Discreet Luxury Floating Concierge Trigger Badge */}
      {!isOpen && (
        <button
          onClick={() => setIsOpen(true)}
          className="fixed bottom-6 right-6 z-40 p-3 sm:px-4 sm:py-3 liquid-glass rounded-full border border-aura-gold/40 shadow-2xl hover:border-aura-gold transition-all duration-300 flex items-center gap-2 group hover:scale-105"
          title="Consult Aura AI Concierge Privé"
        >
          <div className="relative">
            <div className="w-8 h-8 rounded-full bg-gradient-to-br from-[#DFBE7A] to-[#9E7D38] p-0.5 shadow-md flex items-center justify-center">
              <div className="w-full h-full bg-[#121110] rounded-full flex items-center justify-center">
                <Sparkles size={14} className="text-[#DFBE7A] group-hover:rotate-12 transition-transform" />
              </div>
            </div>
            <span className="absolute -top-0.5 -right-0.5 w-2.5 h-2.5 bg-emerald-400 rounded-full border-2 border-[#121110] animate-pulse"></span>
          </div>
          <div className="hidden sm:block text-left pr-1">
            <span className="text-[10px] uppercase font-bold tracking-widest text-aura-gold block leading-tight">
              AI Stylist
            </span>
            <span className="text-xs font-semibold text-neutral-800 dark:text-neutral-200 block leading-tight">
              Concierge Privé
            </span>
          </div>
        </button>
      )}

      {/* Haute Couture Venetian Liquid Glass Modal */}
      {isOpen && (
        <div className="fixed inset-0 z-50 flex items-end sm:items-center justify-center sm:justify-end p-0 sm:p-6 bg-black/60 backdrop-blur-md animate-in fade-in">
          <div className="w-full sm:max-w-xl h-[88vh] sm:h-[82vh] liquid-glass bg-white/95 dark:bg-[#0E0D0C]/95 border-t sm:border border-white/80 dark:border-white/10 sm:rounded-3xl shadow-2xl flex flex-col overflow-hidden">
            
            {/* Modal Header */}
            <div className="p-4 sm:p-5 border-b border-neutral-200/60 dark:border-neutral-800/80 flex items-center justify-between shrink-0 bg-neutral-100/50 dark:bg-black/30 backdrop-blur-xl">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-2xl bg-gradient-to-br from-[#DFBE7A] to-[#9E7D38] p-0.5 shadow-md flex items-center justify-center">
                  <div className="w-full h-full bg-[#121110] rounded-[14px] flex items-center justify-center">
                    <span className="font-serif font-bold text-base text-[#DFBE7A]">A</span>
                  </div>
                </div>
                <div>
                  <div className="flex items-center gap-2">
                    <h3 className="font-serif font-bold text-base text-neutral-900 dark:text-neutral-100">
                      Aura Concierge Privé
                    </h3>
                    <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-aura-gold/15 text-aura-gold border border-aura-gold/30 font-bold">
                      Gemini 3.8 Flash
                    </span>
                  </div>
                  <span className="text-xs text-neutral-500 dark:text-neutral-400 flex items-center gap-1.5 mt-0.5">
                    <span className="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
                    Atelier High-Fashion Wardrobe Architect
                  </span>
                </div>
              </div>

              <div className="flex items-center gap-1">
                <button
                  onClick={() => setMessages([messages[0]])}
                  className="p-2 text-neutral-400 hover:text-neutral-900 dark:hover:text-white rounded-xl hover:bg-neutral-100 dark:hover:bg-white/5 transition-colors"
                  title="Reset Dialogue"
                >
                  <RefreshCw size={15} />
                </button>
                <button
                  onClick={() => setIsOpen(false)}
                  className="p-2 text-neutral-400 hover:text-neutral-900 dark:hover:text-white rounded-xl hover:bg-neutral-100 dark:hover:bg-white/5 transition-colors"
                  title="Close Concierge"
                >
                  <X size={18} />
                </button>
              </div>
            </div>

            {/* Floating Toast Notification */}
            {toast && (
              <div className={`mx-4 mt-3 p-3 rounded-xl text-xs font-semibold flex items-center gap-2 animate-in fade-in transition-all ${
                toast.type === 'success' ? 'bg-emerald-500/20 text-emerald-800 dark:text-emerald-300 border border-emerald-500/30' :
                toast.type === 'error' ? 'bg-rose-500/20 text-rose-800 dark:text-rose-300 border border-rose-500/30' :
                'bg-aura-gold/20 text-neutral-900 dark:text-neutral-100 border border-aura-gold/30'
              }`}>
                <Sparkles size={13} className="text-aura-gold shrink-0 animate-pulse" />
                <span>{toast.message}</span>
              </div>
            )}

            {/* Chat Stream Body */}
            <div className="flex-1 overflow-y-auto p-4 sm:p-5 space-y-4">
              {messages.map((m) => (
                <div key={m.id} className={`flex gap-3 ${m.sender === 'client' ? 'justify-end' : 'justify-start'}`}>
                  {m.sender === 'concierge' && (
                    <div className="w-7 h-7 rounded-full bg-aura-gold/20 border border-aura-gold/40 flex items-center justify-center text-[10px] text-aura-gold shrink-0 font-serif font-bold">
                      A
                    </div>
                  )}

                  <div className={`space-y-3 max-w-[85%] ${
                    m.sender === 'client' 
                      ? 'bg-neutral-900 dark:bg-neutral-800 text-white rounded-2xl rounded-tr-sm p-4 text-xs' 
                      : 'liquid-glass rounded-2xl rounded-tl-sm p-4 text-xs text-neutral-800 dark:text-neutral-200 border-white/60 dark:border-white/10'
                  }`}>
                    {/* User Uploaded Image Preview */}
                    {m.image && (
                      <div className="mb-2 rounded-xl overflow-hidden border border-white/20 max-w-xs">
                        <img src={m.image} alt="Style Reference" className="w-full h-36 object-cover" />
                      </div>
                    )}

                    {/* Message Prose */}
                    <div className="whitespace-pre-wrap leading-relaxed">
                      {m.text}
                    </div>

                    {/* Embedded Recommended Garment Cards */}
                    {m.products && m.products.length > 0 && (
                      <div className="pt-2 space-y-2.5">
                        <span className="text-[10px] font-bold uppercase tracking-wider text-aura-gold block">
                          Curated Garments in Atelier Stock
                        </span>

                        <div className="space-y-2">
                          {m.products.map((prod) => (
                            <div 
                              key={prod.id} 
                              className="flex items-center gap-3 p-2.5 rounded-xl bg-neutral-100/80 dark:bg-black/50 border border-neutral-200/70 dark:border-white/10 hover:border-aura-gold/50 transition-colors"
                            >
                              <div className="w-12 h-14 rounded-lg overflow-hidden shrink-0 border border-black/10 dark:border-white/10">
                                <ImageWithFallback 
                                  src={prod.primary_image} 
                                  alt={prod.name} 
                                  categoryName={prod.category} 
                                  className="w-full h-full object-cover" 
                                />
                              </div>
                              <div className="flex-1 min-w-0">
                                <h4 className="font-bold text-xs text-neutral-900 dark:text-neutral-100 truncate">{prod.name}</h4>
                                <p className="text-[11px] text-neutral-500 dark:text-neutral-400">{prod.material}</p>
                                <span className="text-xs font-mono font-bold text-aura-gold">
                                  {formatPrice(prod.discount_price || prod.base_price)}
                                </span>
                              </div>
                              <div className="flex items-center gap-1.5 shrink-0">
                                <button
                                  onClick={() => {
                                    navigate(`/products/${prod.id}`);
                                    setIsOpen(false);
                                  }}
                                  className="p-1.5 text-neutral-500 hover:text-neutral-900 dark:hover:text-white rounded-lg bg-white/60 dark:bg-white/10 transition-colors"
                                  title="Inspect Garment Details"
                                >
                                  <Eye size={13} />
                                </button>
                                <button
                                  onClick={() => handleQuickAdd(prod)}
                                  className="px-2.5 py-1 text-xs font-bold rounded-lg liquid-btn-gold text-neutral-950 flex items-center gap-1 shadow-sm"
                                  title="Add to Shopping Bag"
                                >
                                  <ShoppingBag size={11} /> Bag
                                </button>
                              </div>
                            </div>
                          ))}
                        </div>

                        {/* Multi-Item Capsule Action */}
                        {m.products.length > 1 && (
                          <div className="pt-2 border-t border-neutral-200/60 dark:border-neutral-800/80 flex items-center justify-between gap-3">
                            <div>
                              <span className="text-[10px] text-neutral-400 block uppercase tracking-wider font-semibold">
                                Complete Capsule ({m.products.length} Pieces)
                              </span>
                              <span className="text-xs font-serif font-bold text-neutral-900 dark:text-neutral-100">
                                {formatPrice(m.products.reduce((acc, p) => acc + (p.discount_price || p.base_price), 0))}
                              </span>
                            </div>
                            <button
                              onClick={() => handleAddEntireCapsule(m.products || [])}
                              className="px-3 py-1.5 rounded-xl liquid-btn-gold text-neutral-950 text-xs font-bold uppercase tracking-wider shadow-md hover:scale-102 transition-transform"
                            >
                              Add Ensemble to Bag
                            </button>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                </div>
              ))}

              {/* Real-time Thinking Animation */}
              {isLoading && (
                <div className="flex gap-3 items-center">
                  <div className="w-7 h-7 rounded-full bg-aura-gold/20 border border-aura-gold/40 flex items-center justify-center text-[10px] text-aura-gold shrink-0 font-serif font-bold">
                    A
                  </div>
                  <div className="liquid-glass rounded-2xl rounded-tl-sm p-3.5 text-xs text-aura-gold flex items-center gap-2">
                    <span className="w-2 h-2 rounded-full bg-aura-gold animate-ping"></span>
                    <span>Consulting atelier inventory archives & drape physics...</span>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>

            {/* Quick Inspiration Pills */}
            <div className="px-4 py-2 border-t border-neutral-200/50 dark:border-neutral-800/60 flex gap-2 overflow-x-auto text-[11px]">
              {quickPrompts.map((p, i) => (
                <button
                  key={i}
                  onClick={() => handleSendMessage(p)}
                  disabled={isLoading}
                  className="px-3 py-1.5 rounded-full liquid-pill text-neutral-600 dark:text-neutral-300 hover:text-aura-gold whitespace-nowrap transition-colors flex items-center gap-1.5"
                >
                  <Sparkles size={11} className="text-aura-gold" />
                  <span>{p}</span>
                </button>
              ))}
            </div>

            {/* Input Bar & Multimodal Style Lens Attachments */}
            <div className="p-3 sm:p-4 border-t border-neutral-200/60 dark:border-neutral-800/80 bg-neutral-50/70 dark:bg-black/40 space-y-2">
              {/* Image Chip Preview */}
              {selectedImage && (
                <div className="flex items-center gap-2 p-1.5 bg-neutral-200/80 dark:bg-neutral-800 rounded-xl max-w-xs animate-in fade-in">
                  <img src={selectedImage} alt="Attachment" className="w-8 h-8 rounded-lg object-cover" />
                  <span className="text-xs text-neutral-800 dark:text-neutral-200 truncate flex-1 font-mono">Style Reference Attached</span>
                  <button onClick={() => setSelectedImage(null)} className="p-1 hover:text-red-500">
                    <X size={14} />
                  </button>
                </div>
              )}

              <div className="flex items-center gap-2">
                <input
                  type="file"
                  accept="image/*"
                  ref={fileInputRef}
                  onChange={handleImageSelect}
                  className="hidden"
                />
                <button
                  type="button"
                  onClick={() => fileInputRef.current?.click()}
                  className="p-2.5 rounded-xl liquid-pill text-neutral-500 hover:text-aura-gold transition-colors"
                  title="Upload Style Inspiration Photo (Multimodal Vision)"
                >
                  <ImageIcon size={16} />
                </button>

                <input
                  type="text"
                  value={inputText}
                  onChange={(e) => setInputText(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && !isLoading && handleSendMessage()}
                  placeholder="Inquire silhouette, occasion styling, or drape..."
                  className="flex-1 px-4 py-2.5 text-xs liquid-input rounded-xl text-neutral-900 dark:text-neutral-100 placeholder-neutral-400 dark:placeholder-neutral-500"
                />

                <button
                  onClick={() => handleSendMessage()}
                  disabled={isLoading || (!inputText.trim() && !selectedImage)}
                  className="p-2.5 sm:px-4 sm:py-2.5 rounded-xl liquid-btn-gold text-neutral-950 font-bold text-xs uppercase tracking-wider flex items-center gap-1.5 disabled:opacity-40 shadow-md transition-all"
                >
                  <span className="hidden sm:inline">Inquire</span>
                  <Send size={13} />
                </button>
              </div>
            </div>

          </div>
        </div>
      )}
    </>
  );
};
