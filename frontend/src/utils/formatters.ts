/**
 * Currency & Number Formatting Utility for Aura Haute Atelier
 * Formats all monetary values into Indian Rupees (₹) using Indian numbering system
 * Automatically normalizes any legacy USD values (< 500) into authentic luxury INR equivalents
 */

export const normalizeToInr = (amount: number | null | undefined): number => {
  if (amount === null || amount === undefined || isNaN(Number(amount))) {
    return 0;
  }
  const num = Number(amount);
  if (num > 0 && num < 500) {
    // Legacy USD price detected -> normalize to accurate luxury INR pricing ($1 = ~₹85) ending in 99
    return Math.max(2499, Math.round((num * 85) / 100) * 100 - 1);
  }
  return num;
};

export const formatPrice = (amount: number | null | undefined): string => {
  if (amount === null || amount === undefined || isNaN(Number(amount))) {
    return '₹0';
  }
  const normalized = normalizeToInr(amount);
  const numeric = Math.round(normalized);
  return `₹${numeric.toLocaleString('en-IN')}`;
};

export const formatPriceExact = (amount: number | null | undefined): string => {
  if (amount === null || amount === undefined || isNaN(Number(amount))) {
    return '₹0.00';
  }
  const normalized = normalizeToInr(amount);
  return `₹${normalized.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
};

export const CURRENCY_SYMBOL = '₹';
