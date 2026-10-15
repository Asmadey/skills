"use client";

import React, { useRef } from "react";
import { useScrollcraft } from "./useScrollcraft";

interface CinematicHeroProps {
  badge?: string;
  title: string;
  subtitle: string;
  primaryCtaText?: string;
  primaryCtaHref?: string;
  secondaryCtaText?: string;
  secondaryCtaHref?: string;
}

export function CinematicHero({
  badge = "PersonalOS • Intelligence Operating System",
  title = "Командный центр нового поколения",
  subtitle = "Иммерсивная экосистема для локальных ИИ-агентов, автономных исследований и инженерных рабочих процессов.",
  primaryCtaText = "Начать работу",
  primaryCtaHref = "#get-started",
  secondaryCtaText = "Документация",
  secondaryCtaHref = "#docs",
}: CinematicHeroProps) {
  const heroRef = useRef<HTMLDivElement>(null);
  const { progress, isReducedMotion } = useScrollcraft(heroRef);

  // Параллакс-смещения слоев глубины (отключаются при reduced motion)
  const bgTranslateY = isReducedMotion ? 0 : progress * 80;
  const cardTranslateY = isReducedMotion ? 0 : -progress * 40;
  const cardScale = isReducedMotion ? 1 : 1 - progress * 0.05;
  const contentOpacity = isReducedMotion ? 1 : Math.max(1 - progress * 1.6, 0);

  return (
    <section
      ref={heroRef}
      className="relative w-full min-h-[140dvh] bg-neutral-950 text-neutral-50 overflow-hidden"
    >
      {/* СЛОЙ 0: Backdrop Plane (Фоновый глубокий градиент и сетка) */}
      <div
        className="sticky top-0 h-[100dvh] w-full flex items-center justify-center overflow-hidden"
        style={{
          transform: `translate3d(0, ${bgTranslateY}px, 0)`,
          willChange: "transform",
        }}
      >
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_80%_80%_at_50%_-20%,rgba(120,119,198,0.22),rgba(255,255,255,0))]" />
        <div className="absolute inset-0 bg-[linear-gradient(to_right,#1f293715_1px,transparent_1px),linear-gradient(to_bottom,#1f293715_1px,transparent_1px)] bg-[size:4rem_4rem] [mask-image:radial-gradient(ellipse_60%_50%_at_50%_40%,#000_70%,transparent_100%)]" />
      </div>

      {/* СЛОЙ 1 & 2: Foreground & Subject Plane (Текстовый контур + Интерактивный терминал с Border Beam) */}
      <div className="sticky top-0 h-[100dvh] w-full flex flex-col items-center justify-center px-4 sm:px-6 lg:px-8 pointer-events-none">
        {/* Контентный заголовок */}
        <div
          className="max-w-4xl text-center space-y-6 pointer-events-auto"
          style={{
            opacity: contentOpacity,
            willChange: "opacity",
          }}
        >
          {badge && (
            <div className="inline-flex items-center gap-2 px-3 py-1 text-xs font-medium rounded-full bg-neutral-900 border border-neutral-800 text-neutral-300 shadow-sm">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
              {badge}
            </div>
          )}

          <h1 className="text-4xl sm:text-6xl lg:text-7xl font-extrabold tracking-tight bg-clip-text text-transparent bg-gradient-to-b from-white via-neutral-100 to-neutral-400">
            {title}
          </h1>

          <p className="text-base sm:text-xl text-neutral-400 max-w-2xl mx-auto leading-relaxed">
            {subtitle}
          </p>

          <div className="flex flex-wrap items-center justify-center gap-4 pt-4">
            <a
              href={primaryCtaHref}
              className="px-6 py-3 text-sm font-semibold text-neutral-950 bg-white rounded-lg hover:bg-neutral-200 transition-colors shadow-lg shadow-white/10"
            >
              {primaryCtaText}
            </a>
            <a
              href={secondaryCtaHref}
              className="px-6 py-3 text-sm font-semibold text-neutral-300 bg-neutral-900 border border-neutral-800 rounded-lg hover:bg-neutral-800 transition-colors"
            >
              {secondaryCtaText}
            </a>
          </div>
        </div>

        {/* СЛОЙ 3: Subject Actor (Интерактивная 3D-панель с MagicUI Border Beam) */}
        <div
          className="mt-12 w-full max-w-5xl rounded-2xl border border-neutral-800/80 bg-neutral-900/60 backdrop-blur-xl p-4 shadow-2xl pointer-events-auto relative overflow-hidden"
          style={{
            transform: `translate3d(0, ${cardTranslateY}px, 0) scale(${cardScale})`,
            willChange: "transform",
          }}
        >
          {/* Border Beam Effect */}
          <div className="absolute inset-0 pointer-events-none rounded-2xl border border-transparent [mask-clip:padding-box,border-box] [mask-composite:intersect] [mask-image:linear-gradient(transparent,transparent),linear-gradient(#000,#000)] before:absolute before:aspect-square before:w-[200px] before:animate-[spin_4s_linear_infinite] before:bg-[conic-gradient(from_0deg,transparent_0_340deg,rgba(255,255,255,0.8)_360deg)] before:[offset-anchor:calc(100%-100px)_calc(100%-100px)]" />

          {/* Превью внутреннего интерфейса PersonalOS */}
          <div className="rounded-xl bg-neutral-950 border border-neutral-800 p-4 font-mono text-xs text-neutral-400 space-y-2">
            <div className="flex items-center gap-2 border-b border-neutral-800 pb-2">
              <span className="w-3 h-3 rounded-full bg-red-500/80" />
              <span className="w-3 h-3 rounded-full bg-yellow-500/80" />
              <span className="w-3 h-3 rounded-full bg-green-500/80" />
              <span className="ml-2 text-neutral-500 text-[11px]">personal-os ~ /arena/active-duel</span>
            </div>
            <div className="text-emerald-400">$ /security-audit --effort medium</div>
            <div className="text-neutral-300">✔ Recon & Ledger Initialized: 69 files tracked</div>
            <div className="text-neutral-300">✔ 3-Lens Panel Quorum: Consensus Reached</div>
            <div className="text-neutral-500">Status: PASS (0 Critical / 0 High)</div>
          </div>
        </div>
      </div>
    </section>
  );
}
