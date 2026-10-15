"use client";

import { useEffect, useState, useRef } from "react";

interface ScrollcraftState {
  progress: number;       // Прогресс скролла от 0.0 до 1.0 в рамках секции
  viewportTop: number;    // Абсолютная позиция скролла
  isReducedMotion: boolean;
}

/**
 * useScrollcraft: React-хук привязки скролл-таймлайна для Cinematic Component Architecture.
 * - Чистый requestAnimationFrame (60 FPS, без скролл-джекинга).
 * - Автоматически отслеживает системный режим prefers-reduced-motion.
 * - Безопасен для мобильных устройств (iOS Safari dvh).
 */
export function useScrollcraft(containerRef?: React.RefObject<HTMLElement | null>): ScrollcraftState {
  const [state, setState] = useState<ScrollcraftState>({
    progress: 0,
    viewportTop: 0,
    isReducedMotion: false,
  });

  const rafId = useRef<number | null>(null);

  useEffect(() => {
    if (typeof window === "undefined") return;

    // Проверка reduced motion
    const motionQuery = window.matchMedia("(prefers-reduced-motion: reduce)");
    let isReduced = motionQuery.matches;

    const handleMotionChange = (e: MediaQueryListEvent) => {
      isReduced = e.matches;
      setState((prev) => ({ ...prev, isReducedMotion: isReduced }));
    };

    if (motionQuery.addEventListener) {
      motionQuery.addEventListener("change", handleMotionChange);
    }

    const updateScroll = () => {
      const scrollY = window.scrollY || window.pageYOffset;

      if (isReduced) {
        setState({
          progress: 0,
          viewportTop: scrollY,
          isReducedMotion: true,
        });
        return;
      }

      let progress = 0;
      if (containerRef && containerRef.current) {
        const rect = containerRef.current.getBoundingClientRect();
        const height = rect.height - window.innerHeight;
        if (height > 0) {
          progress = Math.min(Math.max(-rect.top / height, 0), 1);
        }
      } else {
        const docHeight = document.documentElement.scrollHeight - window.innerHeight;
        progress = docHeight > 0 ? Math.min(Math.max(scrollY / docHeight, 0), 1) : 0;
      }

      setState({
        progress,
        viewportTop: scrollY,
        isReducedMotion: isReduced,
      });

      rafId.current = null;
    };

    const onScroll = () => {
      if (rafId.current === null) {
        rafId.current = requestAnimationFrame(updateScroll);
      }
    };

    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onScroll, { passive: true });
    updateScroll();

    return () => {
      window.removeEventListener("scroll", onScroll);
      window.removeEventListener("resize", onScroll);
      if (motionQuery.removeEventListener) {
        motionQuery.removeEventListener("change", handleMotionChange);
      }
      if (rafId.current !== null) {
        cancelAnimationFrame(rafId.current);
      }
    };
  }, [containerRef]);

  return state;
}
