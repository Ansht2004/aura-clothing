import React, { useState } from 'react';
import { useNavigate, useSearchParams, Link } from 'react-router-dom';
import { Shield, AlertCircle, ArrowRight } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export const AuthPage: React.FC = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const { login, register } = useAuth();

  const redirectPath = searchParams.get('redirect') || '/';
  const initialMode = searchParams.get('mode') === 'register' ? 'register' : 'login';

  const [mode, setMode] = useState<'login' | 'register'>(initialMode);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [fullName, setFullName] = useState('');
  const [phone, setPhone] = useState('');

  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setErrorMessage('');

    try {
      if (mode === 'login') {
        const user = await login(email, password);
        if (user.role === 'admin' && redirectPath === '/') {
          navigate('/admin');
        } else {
          navigate(redirectPath);
        }
      } else {
        await register(fullName, email, password, phone);
        navigate(redirectPath);
      }
    } catch (err: any) {
      setErrorMessage(err.message || 'Authentication failed. Please check your credentials.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-[85vh] flex items-center justify-center py-16 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full liquid-glass rounded-3xl border border-white/80 dark:border-white/10 shadow-2xl p-8 sm:p-10 space-y-6">
        
        {/* Brand Header */}
        <div className="text-center space-y-1">
          <Link to="/" className="inline-block group">
            <span className="font-serif text-3xl sm:text-4xl font-bold tracking-[0.25em] text-neutral-900 dark:text-neutral-100 group-hover:text-aura-gold transition-colors duration-300">
              AURA
            </span>
          </Link>
          <p className="text-[10px] uppercase tracking-[0.3em] text-aura-gold font-bold">
            Atelier Client Portal
          </p>
        </div>

        {/* Tab Switcher - Liquid Pill Toggle */}
        <div className="flex p-1.5 rounded-full liquid-pill text-xs font-bold uppercase tracking-wider">
          <button
            onClick={() => { setMode('login'); setErrorMessage(''); }}
            className={`flex-1 py-2 rounded-full text-center transition-all ${
              mode === 'login' 
                ? 'liquid-btn-gold text-neutral-950 shadow-md font-bold' 
                : 'text-neutral-500 hover:text-neutral-900 dark:hover:text-white'
            }`}
          >
            Sign In
          </button>
          <button
            onClick={() => { setMode('register'); setErrorMessage(''); }}
            className={`flex-1 py-2 rounded-full text-center transition-all ${
              mode === 'register' 
                ? 'liquid-btn-gold text-neutral-950 shadow-md font-bold' 
                : 'text-neutral-500 hover:text-neutral-900 dark:hover:text-white'
            }`}
          >
            Create Account
          </button>
        </div>

        {/* Error Alert */}
        {errorMessage && (
          <div className="p-3.5 bg-rose-500/15 border border-rose-500/30 text-rose-700 dark:text-rose-300 text-xs font-semibold rounded-2xl flex items-center gap-2 animate-in fade-in">
            <AlertCircle size={16} />
            <span>{errorMessage}</span>
          </div>
        )}

        {/* Auth Form */}
        <form onSubmit={handleSubmit} className="space-y-4 text-xs">
          {mode === 'register' && (
            <div>
              <label className="text-[11px] uppercase tracking-wider font-bold text-neutral-700 dark:text-neutral-300 block mb-1">
                Full Name *
              </label>
              <input
                type="text"
                required
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                placeholder="Your Full Name"
                className="w-full px-4 py-2.5 liquid-input text-neutral-900 dark:text-white rounded-2xl"
              />
            </div>
          )}

          <div>
            <label className="text-[11px] uppercase tracking-wider font-bold text-neutral-700 dark:text-neutral-300 block mb-1">
              Email Address *
            </label>
            <input
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="name@example.com"
              className="w-full px-4 py-2.5 liquid-input text-neutral-900 dark:text-white rounded-2xl"
            />
          </div>

          <div>
            <label className="text-[11px] uppercase tracking-wider font-bold text-neutral-700 dark:text-neutral-300 block mb-1">
              Password *
            </label>
            <input
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              className="w-full px-4 py-2.5 liquid-input text-neutral-900 dark:text-white rounded-2xl"
            />
            {mode === 'register' && (
              <span className="text-[10px] text-neutral-400 dark:text-neutral-500 mt-1 block">
                Minimum 6 characters with letters and numbers recommended.
              </span>
            )}
          </div>

          {mode === 'register' && (
            <div>
              <label className="text-[11px] uppercase tracking-wider font-bold text-neutral-700 dark:text-neutral-300 block mb-1">
                Contact Phone (Optional)
              </label>
              <input
                type="tel"
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
                placeholder="+91 98765 43210"
                className="w-full px-4 py-2.5 liquid-input text-neutral-900 dark:text-white rounded-2xl"
              />
            </div>
          )}

          <button
            type="submit"
            disabled={isLoading}
            className="w-full py-3.5 liquid-btn-gold text-neutral-950 text-xs uppercase tracking-widest font-bold rounded-2xl shadow-xl transition-all flex items-center justify-center gap-2 group mt-4 disabled:opacity-40"
          >
            <span>{isLoading ? 'Processing Credentials...' : (mode === 'login' ? 'Sign In to Atelier' : 'Create Patron Account')}</span>
            <ArrowRight size={14} className="group-hover:translate-x-1 transition-transform" />
          </button>
        </form>

        <div className="text-center text-[10px] text-neutral-400 pt-3 border-t border-neutral-200/50 dark:border-neutral-800/50 flex items-center justify-center gap-1.5">
          <Shield size={12} className="text-aura-gold" />
          <span>Role-based JWT access tokens & hashed bcrypt encryption.</span>
        </div>
      </div>
    </div>
  );
};
