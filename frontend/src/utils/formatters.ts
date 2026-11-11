/**
 * Currency & Number Formatting Utility for Aura Apparel
 * Formats all monetary values into Indian Rupees (₹) using Indian numbering system
 */

export const formatPrice = (amount: number | null | undefined): string => {
  if (amount === null || amount === undefined || isNaN(Number(amount))) {
    return '₹0';
  }
  const numeric = Math.round(Number(amount));
  return `₹${numeric.toLocaleString('en-IN')}`;
};

export const formatPriceExact = (amount: number | null | undefined): string => {
  if (amount === null || amount === undefined || isNaN(Number(amount))) {
    return '₹0.00';
  }
  const num = Number(amount);
  return `₹${num.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
};

export const CURRENCY_SYMBOL = '₹';
