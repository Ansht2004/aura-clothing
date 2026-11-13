import React from 'react';
import { Link } from 'react-router-dom';

interface AuraLogoProps {
  variant?: 'navbar' | 'footer' | 'auth' | 'drawer' | 'hero';
  showInsignia?: boolean;
  showTagline?: boolean;
  className?: string;
  asLink?: boolean;
  linkTo?: string;
  onClick?: () => void;
}

export const AuraLogo: React.FC<AuraLogoProps> = ({
  variant = 'navbar',
  showInsignia = true,
  showTagline = true,
  className = '',
  asLink = true,
  linkTo = '/',
  onClick,
}) => {
  // Sizing configurations based on variant
  const config = {
    navbar: {
      emblemSize: 42,
      auraTitleSize: 'text-2xl sm:text-[28px]',
      taglineSize: 'text-[8px] sm:text-[8.5px]',
      gap: 'gap-3.5',
      tracking: 'tracking-[0.32em]',
      taglineTracking: 'tracking-[0.42em]',
      starSize: 11,
    },
    drawer: {
      emblemSize: 38,
      auraTitleSize: 'text-2xl sm:text-[26px]',
      taglineSize: 'text-[8px]',
      gap: 'gap-3',
      tracking: 'tracking-[0.32em]',
      taglineTracking: 'tracking-[0.4em]',
      starSize: 10,
    },
    auth: {
      emblemSize: 56,
      auraTitleSize: 'text-3xl sm:text-4xl',
      taglineSize: 'text-[10px]',
      gap: 'gap-4',
      tracking: 'tracking-[0.34em]',
      taglineTracking: 'tracking-[0.45em]',
      starSize: 14,
    },
    footer: {
      emblemSize: 46,
      auraTitleSize: 'text-3xl',
      taglineSize: 'text-[9px]',
      gap: 'gap-3.5',
      tracking: 'tracking-[0.32em]',
      taglineTracking: 'tracking-[0.42em]',
      starSize: 12,
    },
    hero: {
      emblemSize: 68,
      auraTitleSize: 'text-4xl sm:text-5xl',
      taglineSize: 'text-xs',
      gap: 'gap-4.5',
      tracking: 'tracking-[0.36em]',
      taglineTracking: 'tracking-[0.48em]',
      starSize: 18,
    },
  }[variant];

  const logoContent = (
    <div className={`inline-flex items-center ${config.gap} group select-none ${className}`}>
      {showInsignia && (
        <div className="relative shrink-0 flex items-center justify-center">
          {/* Ambient Radiant Halo (Breathing Golden Aura Bloom) */}
          <div
            className="absolute inset-0 rounded-full bg-gradient-to-tr from-amber-400/30 via-aura-gold/40 to-yellow-200/25 dark:from-aura-gold/35 dark:via-amber-500/25 dark:to-yellow-300/30 blur-md scale-125 opacity-75 group-hover:opacity-100 group-hover:scale-150 transition-all duration-700 pointer-events-none"
          />

          {/* Precision Haute Couture Golden Crest Emblem */}
          <svg
            width={config.emblemSize}
            height={config.emblemSize}
            viewBox="0 0 56 56"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
            className="relative z-10 transition-transform duration-500 group-hover:scale-105 group-hover:rotate-1 drop-shadow-[0_2px_12px_rgba(212,175,55,0.45)] dark:drop-shadow-[0_4px_16px_rgba(240,205,125,0.6)]"
          >
            <defs>
              {/* Brilliant Multi-Stop Specular Gold Gradient */}
              <linearGradient id="auraGoldBright" x1="0" y1="0" x2="56" y2="56" gradientUnits="userSpaceOnUse">
                <stop offset="0%" stopColor="#FFFFFF" />
                <stop offset="18%" stopColor="#FFF2B8" />
                <stop offset="42%" stopColor="#EBBF5C" />
                <stop offset="70%" stopColor="#BA8624" />
                <stop offset="88%" stopColor="#966A16" />
                <stop offset="100%" stopColor="#FFEAA3" />
              </linearGradient>

              {/* Deep Contrast Chiseled Gold for Right Facet */}
              <linearGradient id="auraGoldShadow" x1="28" y1="12" x2="44" y2="44" gradientUnits="userSpaceOnUse">
                <stop offset="0%" stopColor="#FFF5CC" />
                <stop offset="35%" stopColor="#C9972C" />
                <stop offset="75%" stopColor="#8A5E12" />
                <stop offset="100%" stopColor="#5E3E07" />
              </linearGradient>

              {/* Shimmering Bezel Rim Gradient */}
              <linearGradient id="auraBezel" x1="4" y1="4" x2="52" y2="52" gradientUnits="userSpaceOnUse">
                <stop offset="0%" stopColor="#FFF9E6" />
                <stop offset="30%" stopColor="#D4AF37" />
                <stop offset="60%" stopColor="#875E19" />
                <stop offset="85%" stopColor="#F5D77F" />
                <stop offset="100%" stopColor="#FFFFFF" />
              </linearGradient>

              {/* Outer Radial Glow */}
              <radialGradient id="auraRadialCore" cx="28" cy="28" r="28" gradientUnits="userSpaceOnUse">
                <stop offset="0%" stopColor="#FFEAA3" stopOpacity="0.45" />
                <stop offset="50%" stopColor="#D4AF37" stopOpacity="0.18" />
                <stop offset="100%" stopColor="#141312" stopOpacity="0" />
              </radialGradient>

              {/* Soft Drop Glow Filter */}
              <filter id="starGlow" x="-50%" y="-50%" width="200%" height="200%">
                <feGaussianBlur in="SourceGraphic" stdDeviation="1.5" result="blur" />
                <feMerge>
                  <feMergeNode in="blur" />
                  <feMergeNode in="SourceGraphic" />
                </feMerge>
              </filter>
            </defs>

            {/* Shield Body: Octagonal Haute Couture Medallion */}
            {/* Background Crystal Plate */}
            <path
              d="M 28 3.5 L 49.5 14.2 L 52.5 38 L 36.5 52.5 L 19.5 52.5 L 3.5 38 L 6.5 14.2 Z"
              fill="url(#auraRadialCore)"
              className="dark:fill-[#121110] fill-[#FAF6EE]"
            />

            {/* Polished Obsidian / Ivory Core Glass */}
            <path
              d="M 28 5.5 L 48 15.5 L 50.5 37 L 35.5 50.5 L 20.5 50.5 L 5.5 37 L 8 15.5 Z"
              className="fill-neutral-900/90 dark:fill-[#0C0B0A]/95"
            />

            {/* Outer Precious Bezel Frame with Metallic Gradient */}
            <path
              d="M 28 4 L 49 14.8 L 52 38 L 36.2 52.2 L 19.8 52.2 L 4 38 L 7 14.8 Z"
              fill="none"
              stroke="url(#auraBezel)"
              strokeWidth="1.6"
              strokeLinejoin="round"
            />

            {/* Inner Concentric Hairline Inlay */}
            <path
              d="M 28 7.5 L 46 16.8 L 48.5 36 L 34.8 48.5 L 21.2 48.5 L 7.5 36 L 10 16.8 Z"
              fill="none"
              stroke="url(#auraGoldBright)"
              strokeWidth="0.65"
              strokeDasharray="2.5 1.5"
              opacity="0.85"
            />

            {/* 4 Corner Micro-Diamond Accents */}
            <polygon points="28,4 29.5,5.5 28,7 26.5,5.5" fill="#FFFFFF" />
            <polygon points="50.5,27 52,28.5 50.5,30 49,28.5" fill="#FFE8A3" />
            <polygon points="28,49.5 29.5,51 28,52.5 26.5,51" fill="#FFFFFF" />
            <polygon points="5.5,27 7,28.5 5.5,30 4,28.5" fill="#FFE8A3" />

            {/* The Sculpted Haute Couture "A" Monogram */}
            <g id="monogram-A">
              {/* Left Architectural Pillar (Lit Facet) */}
              <path
                d="M 28 14.5 L 25.8 19 L 16 38.5 L 13.5 43.5 L 17.5 43.5 L 19.8 38.5 L 25.5 38.5 L 28 33.5 L 22.2 33.5 L 27.5 22.5 Z"
                fill="url(#auraGoldBright)"
              />

              {/* Right Architectural Pillar (Chiseled Shadow Facet) */}
              <path
                d="M 28 14.5 L 30.2 19 L 40 38.5 L 42.5 43.5 L 38.5 43.5 L 36.2 38.5 L 30.5 38.5 L 28 33.5 L 33.8 33.5 L 28.5 22.5 Z"
                fill="url(#auraGoldShadow)"
              />

              {/* Central Floating Diamond Keystone */}
              <polygon
                points="28,26.5 31,31 28,35.5 25,31"
                fill="url(#auraGoldBright)"
                stroke="#FFEAA3"
                strokeWidth="0.5"
              />
              <circle cx="28" cy="31" r="1.2" fill="#FFFFFF" />
            </g>

            {/* Crown: The 8-Pointed Celestial Radiant Aura Star at Apex */}
            <g filter="url(#starGlow)">
              {/* Diagonal Light Spikes */}
              <path
                d="M 25 11.5 L 31 11.5 M 28 8.5 L 28 14.5"
                stroke="#FFFFFF"
                strokeWidth="0.8"
                strokeLinecap="round"
              />
              {/* Brilliant 8-Point Diamond Star */}
              <path
                d="M 28 7 L 29.2 10.3 L 32.5 11.5 L 29.2 12.7 L 28 16 L 26.8 12.7 L 23.5 11.5 L 26.8 10.3 Z"
                fill="#FFFFFF"
              />
              <circle cx="28" cy="11.5" r="1" fill="#FFEAA3" />
            </g>
          </svg>
        </div>
      )}

      {/* Brand Typographic Wordmark & Haute Atelier Sub-title */}
      <div className="flex flex-col">
        {/* Main Brand Title: "AURA" with Radiant Molten Gold Metallic Finish */}
        <div className="relative flex items-center">
          <span
            className={`font-serif ${config.auraTitleSize} font-bold ${config.tracking} leading-none tracking-tighter uppercase transition-all duration-300 relative z-10 
              bg-gradient-to-r from-[#241B0E] via-[#946813] via-[#CA9E3C] to-[#5C3F08] 
              dark:from-[#FFFFFF] dark:via-[#FDE293] dark:via-[#FFF0C2] dark:to-[#E5A835] 
              bg-clip-text text-transparent
              drop-shadow-[0_1px_2px_rgba(0,0,0,0.12)]
              dark:drop-shadow-[0_2px_16px_rgba(240,205,125,0.65)]
              group-hover:brightness-110`}
          >
            AURA
          </span>

          {/* Golden Specular Sheen Glint */}
          <span className="absolute -top-1.5 -right-2.5 text-amber-500 dark:text-yellow-200 opacity-90 group-hover:scale-125 group-hover:rotate-45 transition-transform duration-500 animate-pulse">
            ✦
          </span>
        </div>

        {/* Subtitle: "✦ HAUTE ATELIER ✦" with Fine Parisian Craftsmanship */}
        {showTagline && (
          <div className="flex items-center gap-1.5 mt-1">
            <span className="text-[6.5px] text-amber-600 dark:text-aura-goldLight">◆</span>
            <span
              className={`${config.taglineSize} uppercase ${config.taglineTracking} font-bold text-neutral-900 dark:text-[#EED396] group-hover:text-aura-gold transition-colors duration-300 whitespace-nowrap leading-none`}
            >
              HAUTE ATELIER
            </span>
            <span className="text-[6.5px] text-amber-600 dark:text-aura-goldLight">◆</span>
          </div>
        )}
      </div>
    </div>
  );

  if (asLink) {
    return (
      <Link to={linkTo} onClick={onClick} className="inline-block focus:outline-none">
        {logoContent}
      </Link>
    );
  }

  return logoContent;
};
