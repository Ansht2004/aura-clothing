import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  User as UserIcon, MapPin, KeyRound, Plus, 
  Trash2, Edit3, Check, AlertCircle, X, Shield, Sparkles 
} from 'lucide-react';
import { api } from '../services/api';
import { Address, User } from '../types';
import { useAuth } from '../context/AuthContext';
import { LoadingSpinner } from '../components/common/LoadingSpinner';

export const ProfilePage: React.FC = () => {
  const { user, updateUser, isAuthenticated, isLoading } = useAuth();
  const navigate = useNavigate();

  // Tab State
  const [activeTab, setActiveTab] = useState<'profile' | 'addresses' | 'security'>('profile');

  // Profile Form
  const [fullName, setFullName] = useState('');
  const [phone, setPhone] = useState('');
  const [profileSaving, setProfileSaving] = useState(false);
  const [profileMsg, setProfileMsg] = useState<{ type: 'success' | 'error'; text: string } | null>(null);

  // Security Form
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [passwordSaving, setPasswordSaving] = useState(false);
  const [passwordMsg, setPasswordMsg] = useState<{ type: 'success' | 'error'; text: string } | null>(null);

  // Addresses State
  const [addresses, setAddresses] = useState<Address[]>([]);
  const [addressLoading, setAddressLoading] = useState(true);
  const [showAddressModal, setShowAddressModal] = useState(false);
  const [editingAddressId, setEditingAddressId] = useState<number | null>(null);
  const [addressForm, setAddressForm] = useState({
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

  const loadAddresses = async () => {
    try {
      const res = await api.getAddresses();
      setAddresses(res.addresses || []);
    } catch (err) {
      console.error("Failed to fetch addresses:", err);
      setAddresses([]);
    } finally {
      setAddressLoading(false);
    }
  };

  // Immediate protection & state synchronization
  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      setFullName('');
      setPhone('');
      setAddresses([]);
      navigate('/auth', { replace: true });
      return;
    }

    if (user) {
      setFullName(user.full_name || '');
      setPhone(user.phone || '');
      setAddressForm(prev => ({
        ...prev,
        full_name: user.full_name || '',
        phone: user.phone || ''
      }));
      loadAddresses();
    } else {
      setFullName('');
      setPhone('');
      setAddresses([]);
    }
  }, [user, isAuthenticated, isLoading, navigate]);

  if (isLoading) {
    return <LoadingSpinner fullPage message="Accessing Account Details..." />;
  }

  if (!isAuthenticated || !user) {
    return null;
  }

  const handleUpdateProfile = async (e: React.FormEvent) => {
    e.preventDefault();
    setProfileSaving(true);
    setProfileMsg(null);
    try {
      const res = await api.updateProfile({ full_name: fullName, phone });
      updateUser(res.user);
      setProfileMsg({ type: 'success', text: 'Personal information updated successfully.' });
    } catch (err: any) {
      setProfileMsg({ type: 'error', text: err.message || 'Failed to update profile.' });
    } finally {
      setProfileSaving(false);
    }
  };

  const handleChangePassword = async (e: React.FormEvent) => {
    e.preventDefault();
    if (newPassword !== confirmPassword) {
      setPasswordMsg({ type: 'error', text: 'New passwords do not match.' });
      return;
    }
    setPasswordSaving(true);
    setPasswordMsg(null);
    try {
      await api.changePassword({ current_password: currentPassword, new_password: newPassword });
      setPasswordMsg({ type: 'success', text: 'Password has been changed securely.' });
      setCurrentPassword('');
      setNewPassword('');
      setConfirmPassword('');
    } catch (err: any) {
      setPasswordMsg({ type: 'error', text: err.message || 'Failed to update password.' });
    } finally {
      setPasswordSaving(false);
    }
  };

  const handleSaveAddress = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (editingAddressId) {
        await api.updateAddress(editingAddressId, addressForm);
      } else {
        await api.addAddress(addressForm);
      }
      setShowAddressModal(false);
      loadAddresses();
    } catch (err: any) {
      alert(err.message || 'Failed to save address.');
    }
  };

  const handleSetDefault = async (addressId: number) => {
    try {
      await api.setDefaultAddress(addressId);
      loadAddresses();
    } catch (err) {
      console.error(err);
    }
  };

  const handleDeleteAddress = async (addressId: number) => {
    if (window.confirm('Are you sure you want to remove this delivery address?')) {
      try {
        await api.deleteAddress(addressId);
        loadAddresses();
      } catch (err) {
        console.error(err);
      }
    }
  };

  const handleEditAddress = (addr: Address) => {
    setEditingAddressId(addr.id);
    setAddressForm({
      full_name: addr.full_name,
      phone: addr.phone,
      address_line1: addr.address_line1,
      address_line2: addr.address_line2 || '',
      city: addr.city,
      state: addr.state,
      postal_code: addr.postal_code,
      country: addr.country,
      is_default: addr.is_default
    });
    setShowAddressModal(true);
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12 space-y-8">
      {/* Header Banner */}
      <div className="liquid-glass rounded-3xl p-6 sm:p-8 border border-white/70 dark:border-white/10 shadow-xl flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full liquid-pill text-[10px] uppercase tracking-[0.2em] text-aura-gold font-bold">
            <Sparkles size={12} /> Client Atelier Account
          </span>
          <h1 className="text-2xl sm:text-4xl font-serif font-bold text-neutral-900 dark:text-neutral-100 mt-2">
            Account & Profile Management
          </h1>
          <p className="text-xs text-neutral-500 dark:text-neutral-400 mt-1 font-medium">
            Manage your personal credentials, delivery destinations, and atelier security.
          </p>
        </div>

        <div className="liquid-pill px-4 py-2 border border-white/80 dark:border-white/10 text-right">
          <span className="text-[9px] uppercase tracking-wider text-neutral-400 block font-bold">Client ID</span>
          <span className="text-xs font-mono font-bold text-aura-gold">
            {user?.customer_code || `AUR-CUST-${String(user?.id || 1).padStart(4, '0')}`}
          </span>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
        
        {/* Sidebar Nav - Liquid Glass Pills */}
        <div className="space-y-2 text-xs">
          <button
            onClick={() => setActiveTab('profile')}
            className={`w-full text-left py-3 px-4 rounded-2xl flex items-center gap-3 font-bold transition-all ${
              activeTab === 'profile' 
                ? 'liquid-btn-gold text-neutral-950 shadow-md scale-102' 
                : 'liquid-pill text-neutral-700 dark:text-neutral-300'
            }`}
          >
            <UserIcon size={16} />
            <span>Personal Info</span>
          </button>

          <button
            onClick={() => setActiveTab('addresses')}
            className={`w-full text-left py-3 px-4 rounded-2xl flex items-center gap-3 font-bold transition-all ${
              activeTab === 'addresses' 
                ? 'liquid-btn-gold text-neutral-950 shadow-md scale-102' 
                : 'liquid-pill text-neutral-700 dark:text-neutral-300'
            }`}
          >
            <MapPin size={16} />
            <span>Saved Addresses ({addresses.length})</span>
          </button>

          <button
            onClick={() => setActiveTab('security')}
            className={`w-full text-left py-3 px-4 rounded-2xl flex items-center gap-3 font-bold transition-all ${
              activeTab === 'security' 
                ? 'liquid-btn-gold text-neutral-950 shadow-md scale-102' 
                : 'liquid-pill text-neutral-700 dark:text-neutral-300'
            }`}
          >
            <KeyRound size={16} />
            <span>Security & Password</span>
          </button>
        </div>

        {/* Tab Content Area - Liquid Glass Card */}
        <div className="md:col-span-3 liquid-glass rounded-3xl p-6 sm:p-10 border border-white/80 dark:border-white/10 shadow-2xl">
          
          {/* TAB 1: Profile Info */}
          {activeTab === 'profile' && (
            <form onSubmit={handleUpdateProfile} className="space-y-5 max-w-lg">
              <div className="pb-4 border-b border-neutral-200/50 dark:border-neutral-800/60">
                <h3 className="font-serif font-bold text-xl text-neutral-900 dark:text-neutral-100">
                  Personal Details
                </h3>
                <p className="text-xs text-neutral-500 dark:text-neutral-400 mt-0.5">Your atelier profile information and patron code.</p>
              </div>

              {profileMsg && (
                <div className={`p-3.5 text-xs rounded-2xl flex items-center gap-2 font-semibold ${
                  profileMsg.type === 'success' ? 'bg-emerald-500/15 text-emerald-700 dark:text-emerald-300 border border-emerald-500/30' : 'bg-rose-500/15 text-rose-700 dark:text-rose-300 border border-rose-500/30'
                }`}>
                  {profileMsg.type === 'success' ? <Check size={16} /> : <AlertCircle size={16} />}
                  <span>{profileMsg.text}</span>
                </div>
              )}

              <div>
                <label className="text-[11px] uppercase tracking-wider font-bold text-neutral-700 dark:text-neutral-300 block mb-1">
                  Full Name
                </label>
                <input
                  type="text"
                  required
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  className="w-full px-4 py-2.5 text-xs liquid-input text-neutral-900 dark:text-white rounded-xl"
                />
              </div>

              <div>
                <label className="text-[11px] uppercase tracking-wider font-bold text-neutral-700 dark:text-neutral-300 block mb-1">
                  Email Address
                </label>
                <input
                  type="email"
                  disabled
                  value={user?.email || ''}
                  className="w-full px-4 py-2.5 text-xs border border-white/10 bg-neutral-200/30 dark:bg-neutral-800/40 text-neutral-500 dark:text-neutral-400 rounded-xl cursor-not-allowed font-medium"
                />
                <span className="text-[10px] text-neutral-400 mt-1 block">
                  Primary client identity and cannot be edited.
                </span>
              </div>

              <div>
                <label className="text-[11px] uppercase tracking-wider font-bold text-neutral-700 dark:text-neutral-300 block mb-1">
                  Contact Phone
                </label>
                <input
                  type="tel"
                  value={phone}
                  onChange={(e) => setPhone(e.target.value)}
                  className="w-full px-4 py-2.5 text-xs liquid-input text-neutral-900 dark:text-white rounded-xl"
                />
              </div>

              <div className="pt-2">
                <button
                  type="submit"
                  disabled={profileSaving}
                  className="px-7 py-3 liquid-btn-gold text-neutral-950 text-xs uppercase tracking-wider font-bold rounded-xl shadow-lg transition-all"
                >
                  {profileSaving ? 'Saving Changes...' : 'Update Details'}
                </button>
              </div>
            </form>
          )}

          {/* TAB 2: Addresses Management */}
          {activeTab === 'addresses' && (
            <div className="space-y-6">
              <div className="flex items-center justify-between pb-4 border-b border-neutral-200/50 dark:border-neutral-800/60">
                <div>
                  <h3 className="font-serif font-bold text-xl text-neutral-900 dark:text-neutral-100">
                    Delivery Addresses
                  </h3>
                  <p className="text-xs text-neutral-500 dark:text-neutral-400 mt-0.5">Manage your primary shipping destinations.</p>
                </div>
                <button
                  onClick={() => {
                    setEditingAddressId(null);
                    setAddressForm({
                      full_name: user?.full_name || '',
                      phone: user?.phone || '',
                      address_line1: '',
                      address_line2: '',
                      city: '',
                      state: '',
                      postal_code: '',
                      country: 'India',
                      is_default: addresses.length === 0
                    });
                    setShowAddressModal(true);
                  }}
                  className="px-4 py-2 liquid-btn-gold text-neutral-950 text-xs uppercase tracking-wider font-bold rounded-xl flex items-center gap-1.5 shadow-md"
                >
                  <Plus size={14} />
                  <span>Add Address</span>
                </button>
              </div>

              {addressLoading ? (
                <LoadingSpinner message="Retrieving Address Book..." />
              ) : addresses.length === 0 ? (
                <p className="text-xs text-neutral-500 dark:text-neutral-400 py-8 text-center">
                  No addresses saved. Add your primary shipping address to expedite future checkouts.
                </p>
              ) : (
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  {addresses.map((addr) => (
                    <div
                      key={addr.id}
                      className={`p-5 rounded-2xl liquid-glass border flex flex-col justify-between text-xs transition-all ${
                        addr.is_default ? 'border-aura-gold ring-2 ring-aura-gold/40 shadow-md' : 'border-white/60 dark:border-white/10'
                      }`}
                    >
                      <div>
                        <div className="flex items-center justify-between">
                          <span className="font-bold text-neutral-900 dark:text-neutral-100 text-sm">{addr.full_name}</span>
                          {addr.is_default && (
                            <span className="text-[10px] bg-gradient-to-r from-aura-gold to-aura-goldLight text-neutral-950 font-bold px-2.5 py-0.5 rounded-full shadow-xs">
                              Default
                            </span>
                          )}
                        </div>

                        <p className="text-neutral-600 dark:text-neutral-300 mt-2.5 leading-relaxed">
                          {addr.address_line1} {addr.address_line2 && `, ${addr.address_line2}`}<br />
                          {addr.city}, {addr.state} {addr.postal_code}<br />
                          {addr.country}
                        </p>
                        <p className="text-[11px] text-neutral-400 font-mono mt-2.5">
                          Phone: {addr.phone}
                        </p>
                      </div>

                      <div className="flex items-center justify-between pt-3 mt-4 border-t border-neutral-200/40 dark:border-neutral-800/40">
                        {!addr.is_default ? (
                          <button
                            onClick={() => handleSetDefault(addr.id)}
                            className="text-[11px] text-aura-gold hover:underline font-bold"
                          >
                            Set as Default
                          </button>
                        ) : <div />}

                        <div className="flex items-center gap-3">
                          <button
                            onClick={() => handleEditAddress(addr)}
                            className="text-neutral-500 hover:text-neutral-900 dark:hover:text-white transition-colors"
                            title="Edit"
                          >
                            <Edit3 size={15} />
                          </button>
                          <button
                            onClick={() => handleDeleteAddress(addr.id)}
                            className="text-neutral-400 hover:text-rose-500 transition-colors"
                            title="Delete"
                          >
                            <Trash2 size={15} />
                          </button>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* TAB 3: Security & Password */}
          {activeTab === 'security' && (
            <form onSubmit={handleChangePassword} className="space-y-5 max-w-lg">
              <div className="pb-4 border-b border-neutral-200/50 dark:border-neutral-800/60">
                <h3 className="font-serif font-bold text-xl text-neutral-900 dark:text-neutral-100">
                  Password & Security
                </h3>
                <p className="text-xs text-neutral-500 dark:text-neutral-400 mt-0.5">Update your account authentication credentials.</p>
              </div>

              {passwordMsg && (
                <div className={`p-3.5 text-xs rounded-2xl flex items-center gap-2 font-semibold ${
                  passwordMsg.type === 'success' ? 'bg-emerald-500/15 text-emerald-700 dark:text-emerald-300 border border-emerald-500/30' : 'bg-rose-500/15 text-rose-700 dark:text-rose-300 border border-rose-500/30'
                }`}>
                  {passwordMsg.type === 'success' ? <Check size={16} /> : <AlertCircle size={16} />}
                  <span>{passwordMsg.text}</span>
                </div>
              )}

              <div>
                <label className="text-[11px] uppercase tracking-wider font-bold text-neutral-700 dark:text-neutral-300 block mb-1">
                  Current Password
                </label>
                <input
                  type="password"
                  required
                  value={currentPassword}
                  onChange={(e) => setCurrentPassword(e.target.value)}
                  className="w-full px-4 py-2.5 text-xs liquid-input text-neutral-900 dark:text-white rounded-xl"
                />
              </div>

              <div>
                <label className="text-[11px] uppercase tracking-wider font-bold text-neutral-700 dark:text-neutral-300 block mb-1">
                  New Password
                </label>
                <input
                  type="password"
                  required
                  value={newPassword}
                  onChange={(e) => setNewPassword(e.target.value)}
                  className="w-full px-4 py-2.5 text-xs liquid-input text-neutral-900 dark:text-white rounded-xl"
                />
              </div>

              <div>
                <label className="text-[11px] uppercase tracking-wider font-bold text-neutral-700 dark:text-neutral-300 block mb-1">
                  Confirm New Password
                </label>
                <input
                  type="password"
                  required
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  className="w-full px-4 py-2.5 text-xs liquid-input text-neutral-900 dark:text-white rounded-xl"
                />
              </div>

              <div className="pt-2">
                <button
                  type="submit"
                  disabled={passwordSaving}
                  className="px-7 py-3 liquid-btn-gold text-neutral-950 text-xs uppercase tracking-wider font-bold rounded-xl shadow-lg transition-all"
                >
                  {passwordSaving ? 'Updating Password...' : 'Save Password'}
                </button>
              </div>
            </form>
          )}

        </div>
      </div>

      {/* Address Edit/Add Modal - Liquid Glass Popup */}
      {showAddressModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-md p-4 animate-in fade-in">
          <div className="liquid-glass border border-white/80 dark:border-white/10 max-w-lg w-full rounded-3xl shadow-2xl p-6 sm:p-8 space-y-5">
            <div className="flex items-center justify-between pb-3 border-b border-neutral-200/50 dark:border-neutral-800/60">
              <h3 className="font-serif font-bold text-lg text-neutral-900 dark:text-neutral-100">
                {editingAddressId ? 'Edit Address' : 'Add New Delivery Address'}
              </h3>
              <button onClick={() => setShowAddressModal(false)} className="w-8 h-8 rounded-full liquid-pill flex items-center justify-center text-neutral-500 hover:text-neutral-900 dark:hover:text-neutral-100">
                <X size={16} />
              </button>
            </div>

            <form onSubmit={handleSaveAddress} className="space-y-4 text-xs">
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-[11px] font-bold text-neutral-700 dark:text-neutral-300 block mb-1">Full Name *</label>
                  <input
                    type="text"
                    required
                    value={addressForm.full_name}
                    onChange={(e) => setAddressForm({ ...addressForm, full_name: e.target.value })}
                    className="w-full px-3.5 py-2.5 liquid-input text-neutral-900 dark:text-white rounded-xl"
                  />
                </div>
                <div>
                  <label className="text-[11px] font-bold text-neutral-700 dark:text-neutral-300 block mb-1">Phone *</label>
                  <input
                    type="tel"
                    required
                    value={addressForm.phone}
                    onChange={(e) => setAddressForm({ ...addressForm, phone: e.target.value })}
                    className="w-full px-3.5 py-2.5 liquid-input text-neutral-900 dark:text-white rounded-xl"
                  />
                </div>
              </div>

              <div>
                <label className="text-[11px] font-bold text-neutral-700 dark:text-neutral-300 block mb-1">Street Address *</label>
                <input
                  type="text"
                  required
                  value={addressForm.address_line1}
                  onChange={(e) => setAddressForm({ ...addressForm, address_line1: e.target.value })}
                  className="w-full px-3.5 py-2.5 liquid-input text-neutral-900 dark:text-white rounded-xl"
                />
              </div>

              <div>
                <label className="text-[11px] font-bold text-neutral-700 dark:text-neutral-300 block mb-1">Apartment / Suite</label>
                <input
                  type="text"
                  value={addressForm.address_line2}
                  onChange={(e) => setAddressForm({ ...addressForm, address_line2: e.target.value })}
                  className="w-full px-3.5 py-2.5 liquid-input text-neutral-900 dark:text-white rounded-xl"
                />
              </div>

              <div className="grid grid-cols-3 gap-3">
                <div>
                  <label className="text-[11px] font-bold text-neutral-700 dark:text-neutral-300 block mb-1">City *</label>
                  <input
                    type="text"
                    required
                    value={addressForm.city}
                    onChange={(e) => setAddressForm({ ...addressForm, city: e.target.value })}
                    className="w-full px-3.5 py-2.5 liquid-input text-neutral-900 dark:text-white rounded-xl"
                  />
                </div>
                <div>
                  <label className="text-[11px] font-bold text-neutral-700 dark:text-neutral-300 block mb-1">State *</label>
                  <input
                    type="text"
                    required
                    value={addressForm.state}
                    onChange={(e) => setAddressForm({ ...addressForm, state: e.target.value })}
                    className="w-full px-3.5 py-2.5 liquid-input text-neutral-900 dark:text-white rounded-xl"
                  />
                </div>
                <div>
                  <label className="text-[11px] font-bold text-neutral-700 dark:text-neutral-300 block mb-1">Postal Code *</label>
                  <input
                    type="text"
                    required
                    value={addressForm.postal_code}
                    onChange={(e) => setAddressForm({ ...addressForm, postal_code: e.target.value })}
                    className="w-full px-3.5 py-2.5 liquid-input text-neutral-900 dark:text-white rounded-xl"
                  />
                </div>
              </div>

              <div className="pt-2">
                <label className="flex items-center gap-2.5 cursor-pointer text-neutral-700 dark:text-neutral-300 font-medium">
                  <input
                    type="checkbox"
                    checked={addressForm.is_default}
                    onChange={(e) => setAddressForm({ ...addressForm, is_default: e.target.checked })}
                    className="w-4 h-4 rounded text-aura-gold focus:ring-aura-gold"
                  />
                  <span>Set as default delivery address</span>
                </label>
              </div>

              <div className="flex justify-end gap-3 pt-3 border-t border-neutral-200/50 dark:border-neutral-800/60">
                <button
                  type="button"
                  onClick={() => setShowAddressModal(false)}
                  className="px-5 py-2.5 liquid-pill text-neutral-700 dark:text-neutral-300 font-bold"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-6 py-2.5 liquid-btn-gold text-neutral-950 uppercase tracking-wider font-bold rounded-xl shadow-md"
                >
                  Save Address
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
