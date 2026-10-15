"use client";

import React from "react";

interface BentoItem {
  title: string;
  description: string;
  tag: string;
  colSpan?: string;
}

const DEFAULT_ITEMS: BentoItem[] = [
  {
    title: "Автономные агенты и турниры Arena",
    description: "Многоагентные состязания с перекрестными атаками, защитой и оценкой по строгой судейской шкале.",
    tag: "Orchestration",
    colSpan: "col-span-1 md:col-span-2",
  },
  {
    title: "Детерминированный аудит безопасности",
    description: "Синтез методологий Claude Security и Cloudflare с 3-линзовой коллегией и нулевыми ложными тревогами.",
    tag: "Security",
    colSpan: "col-span-1",
  },
  {
    title: "Официальный стек Expo & React Native",
    description: "25 инженерных навыков: нативный UI, анимации Reanimated, файловый роутинг и облачные сервисы EAS.",
    tag: "Mobile",
    colSpan: "col-span-1",
  },
  {
    title: "Cinematic Scroll Timeline",
    description: "Многослойный пространственный скролл с аппаратным 60 FPS ускорением и абсолютным запретом скролл-джекинга.",
    tag: "UX Engineering",
    colSpan: "col-span-1 md:col-span-2",
  },
];

export function BentoFeatures({ items = DEFAULT_ITEMS }: { items?: BentoItem[] }) {
  return (
    <section className="py-24 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
      <div className="text-center max-w-3xl mx-auto mb-16 space-y-4">
        <h2 className="text-3xl sm:text-5xl font-bold tracking-tight text-white">
          Архитектурные столпы PersonalOS
        </h2>
        <p className="text-neutral-400 text-base sm:text-lg">
          Каждый компонент спроектирован по стандарту высокой плотности информации и нулевой терпимости к AI-шаблонам.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {items.map((item, index) => (
          <div
            key={index}
            className={`group relative rounded-2xl border border-neutral-800 bg-neutral-900/40 p-8 hover:border-neutral-700 transition-all duration-300 hover:shadow-2xl hover:shadow-white/5 overflow-hidden flex flex-col justify-between ${
              item.colSpan || "col-span-1"
            }`}
          >
            {/* Интерактивный подсвет MagicUI при наведении */}
            <div className="absolute inset-0 bg-gradient-to-br from-indigo-500/10 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500" />

            <div className="space-y-4 relative z-10">
              <span className="inline-block px-2.5 py-0.5 rounded-full text-[11px] font-semibold tracking-wide uppercase bg-neutral-800 text-neutral-300 border border-neutral-700">
                {item.tag}
              </span>
              <h3 className="text-xl sm:text-2xl font-bold text-neutral-100 group-hover:text-white transition-colors">
                {item.title}
              </h3>
              <p className="text-sm sm:text-base text-neutral-400 leading-relaxed">
                {item.description}
              </p>
            </div>

            <div className="pt-6 relative z-10 flex items-center gap-2 text-xs font-semibold text-neutral-400 group-hover:text-emerald-400 transition-colors">
              <span>Изучить спецификацию</span>
              <span className="transform group-hover:translate-x-1 transition-transform">→</span>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
