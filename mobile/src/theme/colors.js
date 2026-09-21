/**
 * JobPilot AI — Design Tokens: Colors
 *
 * Premium color palette with dark/light mode support.
 * Uses HSL for fine-tuned harmonious colors.
 */

export const colors = {
  // Brand
  primary: {
    50: '#eef2ff',
    100: '#e0e7ff',
    200: '#c7d2fe',
    300: '#a5b4fc',
    400: '#818cf8',
    500: '#6366f1',  // Main brand
    600: '#4f46e5',
    700: '#4338ca',
    800: '#3730a3',
    900: '#312e81',
  },

  // Accent — warm coral
  accent: {
    50: '#fff1f2',
    100: '#ffe4e6',
    200: '#fecdd3',
    300: '#fda4af',
    400: '#fb7185',
    500: '#f43f5e',
    600: '#e11d48',
    700: '#be123c',
    800: '#9f1239',
    900: '#881337',
  },

  // Success
  success: {
    50: '#ecfdf5',
    100: '#d1fae5',
    400: '#34d399',
    500: '#10b981',
    600: '#059669',
    700: '#047857',
  },

  // Warning
  warning: {
    50: '#fffbeb',
    100: '#fef3c7',
    400: '#fbbf24',
    500: '#f59e0b',
    600: '#d97706',
  },

  // Error
  error: {
    50: '#fef2f2',
    100: '#fee2e2',
    400: '#f87171',
    500: '#ef4444',
    600: '#dc2626',
  },

  // Neutrals
  neutral: {
    0: '#ffffff',
    50: '#f8fafc',
    100: '#f1f5f9',
    200: '#e2e8f0',
    300: '#cbd5e1',
    400: '#94a3b8',
    500: '#64748b',
    600: '#475569',
    700: '#334155',
    800: '#1e293b',
    850: '#172033',
    900: '#0f172a',
    950: '#020617',
  },

  // Match score gradient
  match: {
    low: '#f87171',      // < 50
    medium: '#fbbf24',   // 50-70
    good: '#34d399',     // 70-85
    excellent: '#6366f1', // 85-100
  },
};

// Dark mode overrides
export const darkColors = {
  bg: colors.neutral[900],
  bgCard: colors.neutral[850],
  bgElevated: colors.neutral[800],
  text: colors.neutral[50],
  textSecondary: colors.neutral[400],
  textMuted: colors.neutral[500],
  border: colors.neutral[700],
  borderLight: colors.neutral[800],
};

// Light mode
export const lightColors = {
  bg: colors.neutral[50],
  bgCard: colors.neutral[0],
  bgElevated: colors.neutral[0],
  text: colors.neutral[900],
  textSecondary: colors.neutral[600],
  textMuted: colors.neutral[400],
  border: colors.neutral[200],
  borderLight: colors.neutral[100],
};

export function getMatchColor(score) {
  if (score >= 85) return colors.match.excellent;
  if (score >= 70) return colors.match.good;
  if (score >= 50) return colors.match.medium;
  return colors.match.low;
}
