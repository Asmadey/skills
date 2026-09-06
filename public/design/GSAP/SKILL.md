---
name: gsap
description: >
  Comprehensive GreenSock Animation Platform (GSAP) skill suite. Includes core tweens (to, from, fromTo),
  timelines, ScrollTrigger, React (useGSAP), Vue/Nuxt/Svelte frameworks, utilities (gsap.utils),
  plugins (Flip, ScrollSmoother, SplitText, MorphSVG, Draggable, Observer), and 60fps performance optimizations.
  Use when writing, optimizing, or reviewing animations in JavaScript, TypeScript, React, Next.js, Vue, or Vanilla JS.
license: MIT
metadata:
  frameworks: "Vanilla JS, React, Next.js, Vue, Nuxt, Svelte, Astro"
  plugins_included: "ScrollTrigger, useGSAP, Flip, SplitText, MorphSVG, DrawSVG, ScrollSmoother, Observer, MotionPath"
---

# GSAP (GreenSock Animation Platform) AI Skill

Official AI Skill for [GSAP](https://gsap.com) — the industry-standard JavaScript animation library.

> **GSAP is 100% free** — including every plugin (SplitText, MorphSVG, ScrollSmoother, Flip, etc.) for commercial use. Install directly from npm: `npm install gsap @gsap/react` (no `.npmrc` / Club token needed).

---

## ⚡ Canonical GSAP Cheat Sheet

```javascript
// 1. Imports and plugin registration (once per app/component)
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
gsap.registerPlugin(ScrollTrigger);

// 2. Single Tween (prefer transforms & autoAlpha over top/left/opacity)
gsap.to(".box", {
  x: 100,
  autoAlpha: 1,
  duration: 0.6,
  ease: "power2.inOut",
  stagger: 0.1
});

// 3. Timelines (for sequential / choreographed animations)
const tl = gsap.timeline({ defaults: { duration: 0.5, ease: "power2.out" } });
tl.to(".header", { y: 0, autoAlpha: 1 })
  .to(".card", { scale: 1, stagger: 0.1 }, "-=0.2")
  .to(".button", { autoAlpha: 1 });

// 4. ScrollTrigger (scroll-linked animations & pinning)
gsap.to(".section", {
  scrollTrigger: {
    trigger: ".section",
    start: "top 80%",
    end: "bottom 20%",
    scrub: true,
    pin: true
  },
  x: 200
});

// 5. React / Next.js Integration (useGSAP hook with scope & cleanup)
import { useGSAP } from "@gsap/react";
gsap.registerPlugin(useGSAP);

export function MyComponent() {
  const container = useRef();
  
  useGSAP(() => {
    gsap.from(".item", { y: 30, opacity: 0, stagger: 0.08 });
  }, { scope: container });

  return <div ref={container}><div className="item">1</div><div className="item">2</div></div>;
}
```

---

## 📚 Specialized Sub-Skills & Reference Guides

Detailed modules located in `skills/`:

| Sub-Skill | Path | Description & Triggers |
|---|---|---|
| **gsap-core** | [skills/gsap-core/SKILL.md](skills/gsap-core/SKILL.md) | Core API: `gsap.to()`, `from()`, `fromTo()`, `set()`, eases, staggers, responsive `matchMedia()`. |
| **gsap-timeline** | [skills/gsap-timeline/SKILL.md](skills/gsap-timeline/SKILL.md) | `gsap.timeline()`, position parameter (`+=`, `-=`, `<`), labels, nesting, playback controls. |
| **gsap-scrolltrigger** | [skills/gsap-scrolltrigger/SKILL.md](skills/gsap-scrolltrigger/SKILL.md) | ScrollTrigger: scrub, pin, start/end triggers, snapping, refresh, parallax. |
| **gsap-react** | [skills/gsap-react/SKILL.md](skills/gsap-react/SKILL.md) | React / Next.js: `useGSAP` hook, refs scoping, SSR hydration safety, automatic cleanup on unmount. |
| **gsap-plugins** | [skills/gsap-plugins/SKILL.md](skills/gsap-plugins/SKILL.md) | Plugins: Flip, ScrollSmoother, SplitText, MorphSVG, DrawSVG, MotionPath, Draggable, Observer, CustomEase. |
| **gsap-frameworks** | [skills/gsap-frameworks/SKILL.md](skills/gsap-frameworks/SKILL.md) | Vue 3 / Nuxt, Svelte / SvelteKit: lifecycle hooks (`onMounted`, `onUnmounted`), scoped cleanup. |
| **gsap-utils** | [skills/gsap-utils/SKILL.md](skills/gsap-utils/SKILL.md) | `gsap.utils`: `clamp`, `mapRange`, `interpolate`, `random`, `snap`, `toArray`, `wrap`, `pipe`. |
| **gsap-performance** | [skills/gsap-performance/SKILL.md](skills/gsap-performance/SKILL.md) | 60fps rules: GPU transforms (x/y/scale/rotation), `autoAlpha`, avoiding layout thrashing. |

---

## 🎯 Best Practices for AI Coding

1. **Always use GPU transforms**: Use `x`, `y`, `xPercent`, `yPercent`, `scale`, `rotation` instead of `top`, `left`, `margin`, `width`, `height`.
2. **Use `autoAlpha` instead of `opacity`**: `autoAlpha` automatically toggles `visibility: hidden` when opacity hits 0, preventing ghost click blocking.
3. **Always scope and clean up in React/Vue**: Never query global DOM selectors without `{ scope: containerRef }` or `gsap.context()`. Always use `@gsap/react` `useGSAP()` or revert contexts on unmount.
4. **Prefer Timelines over delays**: Avoid chaining multiple `delay` properties; group animations in `gsap.timeline()` for maintainable sequences.
5. **Call `ScrollTrigger.refresh()` after DOM changes**: If content loads dynamically or fonts load, refresh ScrollTrigger recalculations.
