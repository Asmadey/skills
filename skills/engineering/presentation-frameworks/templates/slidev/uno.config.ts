import { defineConfig } from 'unocss'

export default defineConfig({
  shortcuts: {
    // Layout & Backgrounds
    'bg-main': 'bg-[#0F172A] text-[#F9FAFB]',
    'slide-container': 'w-full h-full p-12 flex flex-col justify-center relative overflow-hidden',
    
    // Typography
    'text-primary': 'text-[#F9FAFB]',
    'text-secondary': 'text-[#D1D5DB]',
    'text-accent': 'text-[#818CF8]',
    'heading-1': 'text-5xl font-bold text-center mb-8 tracking-tight',
    'heading-2': 'text-3xl font-bold mb-6',
    'subtitle': 'text-xl text-[#D1D5DB] text-center font-normal',
    
    // Cards (Brand/Black.md)
    'card-basic': 'bg-gradient-to-br from-[#1E293B] to-[#334155] rounded-[32px] p-10 border border-white/8 shadow-2xl relative',
    'card-pro': 'bg-gradient-to-b from-[#3B82F6] to-[#10B981] rounded-[32px] p-10 border border-white/10 shadow-glow text-white relative',
    'card-team': 'bg-gradient-to-bl from-[#1E3A5F] to-[#312E81] rounded-[32px] p-10 border border-white/8 shadow-2xl relative',
    
    // UI Elements
    'btn-glossy': 'bg-gradient-to-b from-[#374151] via-[#1F2937] to-[#111827] rounded-full px-7 py-3 border border-white/10 shadow-lg hover:shadow-[0_0_20px_rgba(129,140,248,0.3)] transition-all flex items-center gap-3 text-white font-medium cursor-pointer no-underline block w-fit mx-auto',
    'btn-icon': 'w-8 h-8 rounded-full flex items-center justify-center bg-[#818CF8] text-[#0F172A]',
    
    // Utilities
    'glass': 'backdrop-blur-md bg-white/5 border border-white/10',
    'spacer': 'h-px w-full bg-gradient-to-r from-transparent via-white/10 to-transparent my-8',
    'glow-text': 'text-transparent bg-clip-text bg-gradient-to-r from-[#818CF8] to-[#C7D2FE] drop-shadow-[0_0_10px_rgba(129,140,248,0.5)]',
  },
  theme: {
    colors: {
      brand: {
        dark: '#0F172A',     // Background
        light: '#F9FAFB',    // Text
        accent: '#818CF8',   // Primary
        gray: '#D1D5DB',     // Secondary Text
        cardStart: '#1E293B',
        cardEnd: '#334155',
      },
    },
    fontFamily: {
      sans: 'Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
      mono: '"Fira Code", monospace',
    },
  },
})
