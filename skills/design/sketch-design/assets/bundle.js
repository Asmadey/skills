/**
 * Sketch-Design Runtime Bundle (Zero-Dependency Custom Elements)
 * Hand-drawn presentations and diagrams in Excalidraw aesthetic.
 * Stage resolution: 1600 x 900 px.
 */
(function() {
  'use strict';

  // Palette definitions
  const PALETTE = {
    paper: '#faf8f5',
    desk: '#ece7df',
    line: 'rgba(30, 30, 30, 0.08)',
    ink: '#1e1e1e',
    muted: '#5e5e5e',
    tones: {
      orange: { strong: '#bf4520', tint: 'rgba(191, 69, 32, 0.12)' },
      green:  { strong: '#2b7a4b', tint: 'rgba(43, 122, 75, 0.12)' },
      purple: { strong: '#6941c6', tint: 'rgba(105, 65, 198, 0.12)' },
      pink:   { strong: '#c01048', tint: 'rgba(192, 16, 72, 0.12)' },
      blue:   { strong: '#175cd3', tint: 'rgba(23, 92, 211, 0.12)' },
      teal:   { strong: '#0e7090', tint: 'rgba(14, 112, 144, 0.12)' },
      yellow: { strong: '#b54708', tint: 'rgba(247, 144, 9, 0.18)' },
      red:    { strong: '#b42318', tint: 'rgba(180, 35, 24, 0.12)' },
      gray:   { strong: '#475467', tint: 'rgba(71, 84, 103, 0.08)' }
    }
  };

  // Helper to resolve tone or fill color
  function resolveToneName(val) {
    if (!val) return null;
    val = val.replace('-tint', '').trim();
    return PALETTE.tones[val] ? val : null;
  }

  // Pseudo-random wobbly generator for hand-drawn strokes
  function pseudoRandom(seed) {
    const x = Math.sin(seed++) * 10000;
    return x - Math.floor(x);
  }

  function wobbleCubic(x1, y1, x2, y2, seed = 1) {
    const dx = x2 - x1;
    const dy = y2 - y1;
    const len = Math.hypot(dx, dy);
    if (len < 1) return `L ${x2.toFixed(1)} ${y2.toFixed(1)}`;

    const perpX = -dy / len;
    const perpY = dx / len;

    const r1 = (pseudoRandom(seed) - 0.5) * 4;
    const r2 = (pseudoRandom(seed + 1) - 0.5) * 4;

    const cx1 = x1 + dx * 0.33 + perpX * r1;
    const cy1 = y1 + dy * 0.33 + perpY * r1;
    const cx2 = x1 + dx * 0.66 + perpX * r2;
    const cy2 = y1 + dy * 0.66 + perpY * r2;

    return `C ${cx1.toFixed(1)} ${cy1.toFixed(1)}, ${cx2.toFixed(1)} ${cy2.toFixed(1)}, ${x2.toFixed(1)} ${y2.toFixed(1)}`;
  }

  function wobbleLine(x1, y1, x2, y2, seed = 1) {
    return `M ${x1.toFixed(1)} ${y1.toFixed(1)} ${wobbleCubic(x1, y1, x2, y2, seed)}`;
  }

  function wobbleRect(x, y, w, h, seed = 42) {
    const p1 = `M ${x.toFixed(1)} ${y.toFixed(1)} ` +
      `${wobbleCubic(x, y, x + w, y, seed)} ` +
      `${wobbleCubic(x + w, y, x + w, y + h, seed + 2)} ` +
      `${wobbleCubic(x + w, y + h, x, y + h, seed + 4)} ` +
      `${wobbleCubic(x, y + h, x, y, seed + 6)} Z`;

    const p2 = `M ${(x + 1).toFixed(1)} ${(y - 0.5).toFixed(1)} ` +
      `${wobbleCubic(x + 1, y - 0.5, x + w - 1, y + 0.5, seed + 10)} ` +
      `${wobbleCubic(x + w - 1, y + 0.5, x + w - 0.5, y + h - 1, seed + 12)} ` +
      `${wobbleCubic(x + w - 0.5, y + h - 1, x + 1, y + h + 0.5, seed + 14)} ` +
      `${wobbleCubic(x + 1, y + h + 0.5, x - 0.5, y + 1, seed + 16)} Z`;

    return { path1: p1, path2: p2 };
  }

  // Base Element with Step Visibility
  class SkElement extends HTMLElement {
    connectedCallback() {
      this.classList.add('sk-item');
      this.applyStepVisibility();
      this.applyPosition();
    }

    applyPosition() {
      const x = this.getAttribute('x');
      const y = this.getAttribute('y');
      const w = this.getAttribute('w');
      const h = this.getAttribute('h');
      const rot = this.getAttribute('rot');

      if (x !== null) this.style.left = `${x}px`;
      if (y !== null) this.style.top = `${y}px`;
      if (w !== null) this.style.width = `${w}px`;
      if (h !== null) this.style.height = `${h}px`;
      if (rot !== null) this.style.transform = `rotate(${rot}deg)`;
    }

    applyStepVisibility() {
      const deck = this.closest('sk-deck');
      if (!deck) return;
      const step = parseInt(this.getAttribute('step') || '0', 10);
      const out = this.getAttribute('out') ? parseInt(this.getAttribute('out'), 10) : null;
      const dim = this.getAttribute('dim') ? parseInt(this.getAttribute('dim'), 10) : null;

      const current = deck.currentStep;

      let visible = current >= step;
      if (out !== null && current >= out) visible = false;

      this.style.opacity = !visible ? '0' : (dim !== null && current >= dim ? '0.28' : '1');
      this.style.pointerEvents = visible ? 'auto' : 'none';
      this.style.transition = 'opacity 0.28s ease, transform 0.28s ease';
    }
  }

  // 1. Deck Container
  class SkDeck extends HTMLElement {
    constructor() {
      super();
      this.currentIndex = 0;
      this.currentStep = 0;
      this.overviewMode = false;
    }

    connectedCallback() {
      this.slides = Array.from(this.querySelectorAll('sk-slide'));
      this.initScale();
      this.initEvents();
      this.readHash();
      this.updateView();
    }

    initScale() {
      const updateFit = () => {
        if (this.overviewMode) {
          this.style.transform = 'none';
          this.style.width = '100%';
          this.style.height = 'auto';
          return;
        }
        const winW = window.innerWidth;
        const winH = window.innerHeight;
        const scale = Math.min(winW / 1600, winH / 900);
        this.style.width = '1600px';
        this.style.height = '900px';
        this.style.transform = `scale(${scale})`;
        this.style.transformOrigin = 'center center';
      };
      window.addEventListener('resize', updateFit);
      updateFit();
    }

    initEvents() {
      window.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'Enter') {
          e.preventDefault();
          this.next();
        } else if (e.key === 'ArrowLeft' || e.key === 'Backspace') {
          e.preventDefault();
          this.prev();
        } else if (e.key.toLowerCase() === 'o') {
          e.preventDefault();
          this.toggleOverview();
        } else if (e.key.toLowerCase() === 'f') {
          e.preventDefault();
          this.toggleFullscreen();
        } else if (e.key.toLowerCase() === 'r') {
          e.preventDefault();
          this.resetSlide();
        }
      });

      this.addEventListener('click', (e) => {
        if (this.overviewMode) {
          const slide = e.target.closest('sk-slide');
          if (slide) {
            this.currentIndex = this.slides.indexOf(slide);
            this.currentStep = 0;
            this.overviewMode = false;
            this.updateView();
          }
          return;
        }
        if (e.target.closest('a, button')) return;
        this.next();
      });

      window.addEventListener('hashchange', () => this.readHash());
    }

    readHash() {
      const hash = window.location.hash.replace('#', '');
      const num = parseInt(hash, 10);
      if (!isNaN(num) && num >= 1 && num <= this.slides.length) {
        this.currentIndex = num - 1;
        this.currentStep = 0;
        this.updateView();
      }
    }

    writeHash() {
      window.location.hash = `#${this.currentIndex + 1}`;
    }

    next() {
      const activeSlide = this.slides[this.currentIndex];
      if (!activeSlide) return;
      const maxStep = activeSlide.maxStep;

      if (this.currentStep < maxStep) {
        this.currentStep++;
        this.updateSteps();
      } else if (this.currentIndex < this.slides.length - 1) {
        this.currentIndex++;
        this.currentStep = 0;
        this.updateView();
      }
    }

    prev() {
      if (this.currentStep > 0) {
        this.currentStep--;
        this.updateSteps();
      } else if (this.currentIndex > 0) {
        this.currentIndex--;
        const prevSlide = this.slides[this.currentIndex];
        this.currentStep = prevSlide ? prevSlide.maxStep : 0;
        this.updateView();
      }
    }

    resetSlide() {
      this.currentStep = 0;
      this.updateSteps();
    }

    toggleOverview() {
      this.overviewMode = !this.overviewMode;
      this.classList.toggle('overview-active', this.overviewMode);
      this.updateView();
    }

    toggleFullscreen() {
      if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen().catch(() => {});
      } else {
        document.exitFullscreen().catch(() => {});
      }
    }

    updateView() {
      this.writeHash();
      this.slides.forEach((slide, idx) => {
        if (this.overviewMode) {
          slide.style.display = 'block';
          slide.classList.toggle('is-current', idx === this.currentIndex);
        } else {
          slide.style.display = idx === this.currentIndex ? 'block' : 'none';
        }
      });
      this.updateSteps();
    }

    updateSteps() {
      const activeSlide = this.slides[this.currentIndex];
      if (!activeSlide) return;
      activeSlide.querySelectorAll('.sk-item, [step], [out], [dim]').forEach(item => {
        if (typeof item.applyStepVisibility === 'function') {
          item.applyStepVisibility();
        }
      });
      activeSlide.querySelectorAll('sk-arrow').forEach(arrow => {
        if (typeof arrow.renderArrow === 'function') {
          arrow.renderArrow();
        }
      });
    }
  }

  // 2. Slide Element
  class SkSlide extends HTMLElement {
    connectedCallback() {
      this.classList.add('sk-slide-stage');
      const tone = this.getAttribute('tone') || 'orange';
      const toneDef = PALETTE.tones[tone] || PALETTE.tones.orange;
      this.style.setProperty('--slide-tone', toneDef.strong);
      this.style.setProperty('--slide-tint', toneDef.tint);
    }

    get maxStep() {
      let max = 0;
      this.querySelectorAll('.sk-item, [step], [out], [dim]').forEach(item => {
        const s = parseInt(item.getAttribute('step') || '0', 10);
        const out = parseInt(item.getAttribute('out') || '0', 10);
        const dim = parseInt(item.getAttribute('dim') || '0', 10);
        max = Math.max(max, s, out, dim);
      });
      return max;
    }
  }

  // 3. Title Component
  class SkTitle extends SkElement {
    connectedCallback() {
      super.connectedCallback();
      const num = this.getAttribute('num') || this.getAttribute('number') || '';
      const text = this.getAttribute('text') || this.innerHTML.trim();
      this.innerHTML = `
        <div class="sk-title-wrap">
          ${num ? `<span class="sk-num-circle">${num}</span>` : ''}
          <div class="sk-title-text-group">
            <h1 class="sk-title-heading">${text}</h1>
            <svg class="sk-title-underline" viewBox="0 0 500 16" preserveAspectRatio="none">
              <path d="${wobbleLine(0, 8, 495, 8, 77)}" stroke="var(--slide-tone, ${PALETTE.tones.orange.strong})" stroke-width="3.5" fill="none" stroke-linecap="round"/>
            </svg>
          </div>
        </div>
      `;
    }
  }

  // 4. Box / Card Component
  class SkBox extends SkElement {
    connectedCallback() {
      super.connectedCallback();
      const label = this.getAttribute('label');
      const tone = resolveToneName(this.getAttribute('tone')) || resolveToneName(this.getAttribute('fill'));
      const lineTone = resolveToneName(this.getAttribute('line'));
      const w = parseInt(this.getAttribute('w') || '300', 10);
      const h = parseInt(this.getAttribute('h') || '200', 10);

      const strokeColor = lineTone && PALETTE.tones[lineTone] ? PALETTE.tones[lineTone].strong : PALETTE.ink;
      const fillColor = tone && PALETTE.tones[tone] ? PALETTE.tones[tone].tint : 'transparent';
      const content = this.innerHTML;
      const { path1, path2 } = wobbleRect(4, 4, w - 8, h - 8, Math.floor(Math.random() * 500) + 1);

      this.innerHTML = `
        <svg class="sk-svg-bg" viewBox="0 0 ${w} ${h}">
          <path d="${path1}" fill="${fillColor}" stroke="${strokeColor}" stroke-width="2.2" stroke-linejoin="round"/>
          <path d="${path2}" fill="none" stroke="${strokeColor}" stroke-width="1.2" stroke-linejoin="round" opacity="0.6"/>
        </svg>
        ${label ? `<div class="sk-box-label">${label}</div>` : ''}
        <div class="sk-box-inner">${content}</div>
      `;
    }
  }

  // 5. Document Component (sk-doc)
  class SkDoc extends SkElement {
    connectedCallback() {
      super.connectedCallback();
      const w = parseInt(this.getAttribute('w') || '160', 10);
      const h = parseInt(this.getAttribute('h') || '210', 10);
      const label = this.getAttribute('label') || '';
      const linesAttr = this.getAttribute('lines') || '';
      const fold = 24;

      const docPath = `M 4 4 H ${w - fold} L ${w - 4} ${fold} V ${h - 4} H 4 Z`;
      const foldFlap = `M ${w - fold} 4 V ${fold} H ${w - 4} Z`;

      let linesSvg = '';
      if (linesAttr) {
        const lineParts = linesAttr.split(',').map(s => s.trim());
        lineParts.forEach((part, idx) => {
          const [colName, lenPercent] = part.split(' ');
          const pct = parseInt(lenPercent || '80', 10);
          const tName = resolveToneName(colName);
          const strokeCol = tName ? PALETTE.tones[tName].strong : '#a0a0a0';
          const lineY = 46 + idx * 24;
          const lineW = Math.max(20, (w - 40) * (pct / 100));
          if (lineY < h - 20) {
            linesSvg += `<line x1="20" y1="${lineY}" x2="${20 + lineW}" y2="${lineY}" stroke="${strokeCol}" stroke-width="3" stroke-linecap="round"/>`;
          }
        });
      } else {
        linesSvg = `
          <line x1="20" y1="45" x2="${w - 24}" y2="45" stroke="#d0d0d0" stroke-width="3" stroke-linecap="round"/>
          <line x1="20" y1="70" x2="${w - 36}" y2="70" stroke="#d0d0d0" stroke-width="3" stroke-linecap="round"/>
          <line x1="20" y1="95" x2="${w - 20}" y2="95" stroke="#d0d0d0" stroke-width="3" stroke-linecap="round"/>
          <line x1="20" y1="120" x2="${w - 44}" y2="120" stroke="#d0d0d0" stroke-width="3" stroke-linecap="round"/>
        `;
      }

      this.innerHTML = `
        <svg class="sk-svg-bg" viewBox="0 0 ${w} ${h}">
          <path d="${docPath}" fill="#ffffff" stroke="${PALETTE.ink}" stroke-width="2.2" stroke-linejoin="round"/>
          <path d="${foldFlap}" fill="${PALETTE.desk}" stroke="${PALETTE.ink}" stroke-width="2" stroke-linejoin="round"/>
          ${linesSvg}
        </svg>
        ${label ? `<div class="sk-doc-label">${label}</div>` : ''}
        <div class="sk-doc-inner">${this.innerHTML}</div>
      `;
    }
  }

  // 6. Speech Bubble (sk-bubble)
  class SkBubble extends SkElement {
    connectedCallback() {
      super.connectedCallback();
      const w = parseInt(this.getAttribute('w') || '280', 10);
      const h = parseInt(this.getAttribute('h') || '140', 10);
      const tail = this.getAttribute('tail') || 'bl';
      const tone = resolveToneName(this.getAttribute('tone')) || resolveToneName(this.getAttribute('fill')) || 'blue';
      const fill = PALETTE.tones[tone]?.tint || PALETTE.tones.blue.tint;
      const stroke = PALETTE.tones[tone]?.strong || PALETTE.ink;

      const { path1, path2 } = wobbleRect(4, 4, w - 8, h - 8, 88);

      let tailPath = `M 28 ${h - 6} L 12 ${h + 24} L 56 ${h - 6} Z`;
      if (tail === 'br') tailPath = `M ${w - 56} ${h - 6} L ${w - 12} ${h + 24} L ${w - 28} ${h - 6} Z`;
      else if (tail === 'tl') tailPath = `M 28 6 L 12 -24 L 56 6 Z`;
      else if (tail === 'tr') tailPath = `M ${w - 56} 6 L ${w - 12} -24 L ${w - 28} 6 Z`;

      const content = this.getAttribute('text') || this.innerHTML;

      this.innerHTML = `
        <svg class="sk-svg-bg" viewBox="0 0 ${w} ${h}" preserveAspectRatio="none" style="overflow: visible;">
          <path d="${path1}" fill="${fill}" stroke="${stroke}" stroke-width="2.4" stroke-linejoin="round"/>
          <path d="${path2}" fill="none" stroke="${stroke}" stroke-width="1.2" opacity="0.5"/>
          <path d="${tailPath}" fill="${fill}" stroke="${stroke}" stroke-width="2.4" stroke-linejoin="round"/>
        </svg>
        <div class="sk-bubble-inner">${content}</div>
      `;
    }
  }

  // 7. Chip / Badge (sk-chip)
  class SkChip extends SkElement {
    connectedCallback() {
      super.connectedCallback();
      const text = this.getAttribute('text') || this.innerHTML.trim();
      this.innerHTML = `<span class="sk-chip-tag">${text}</span>`;
    }
  }

  // 8. Mark (sk-mark: check / cross)
  class SkMark extends SkElement {
    connectedCallback() {
      super.connectedCallback();
      const kind = this.getAttribute('kind') || 'check';
      if (kind === 'check') {
        this.innerHTML = `
          <svg class="sk-mark-svg" viewBox="0 0 40 40">
            <path d="M 6 22 L 16 32 L 34 8" fill="none" stroke="${PALETTE.tones.green.strong}" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        `;
      } else {
        this.innerHTML = `
          <svg class="sk-mark-svg" viewBox="0 0 40 40">
            <path d="M 8 8 L 32 32 M 32 8 L 8 32" fill="none" stroke="${PALETTE.tones.red.strong}" stroke-width="4.5" stroke-linecap="round"/>
          </svg>
        `;
      }
    }
  }

  // 9. Hand-drawn Arrow (sk-arrow)
  class SkArrow extends SkElement {
    connectedCallback() {
      super.connectedCallback();
      setTimeout(() => this.renderArrow(), 0);
    }

    renderArrow() {
      const slide = this.closest('sk-slide');
      const fromSel = this.getAttribute('from');
      const toSel = this.getAttribute('to');

      let x1 = parseFloat(this.getAttribute('x1') || '0');
      let y1 = parseFloat(this.getAttribute('y1') || '0');
      let x2 = parseFloat(this.getAttribute('x2') || '100');
      let y2 = parseFloat(this.getAttribute('y2') || '0');

      if (fromSel && toSel && slide) {
        const fromEl = slide.querySelector(fromSel);
        const toEl = slide.querySelector(toSel);
        if (fromEl && toEl) {
          const fx = parseFloat(fromEl.getAttribute('x') || fromEl.offsetLeft);
          const fy = parseFloat(fromEl.getAttribute('y') || fromEl.offsetTop);
          const fw = parseFloat(fromEl.getAttribute('w') || fromEl.offsetWidth || 100);
          const fh = parseFloat(fromEl.getAttribute('h') || fromEl.offsetHeight || 60);

          const tx = parseFloat(toEl.getAttribute('x') || toEl.offsetLeft);
          const ty = parseFloat(toEl.getAttribute('y') || toEl.offsetTop);
          const tw = parseFloat(toEl.getAttribute('w') || toEl.offsetWidth || 100);
          const th = parseFloat(toEl.getAttribute('h') || toEl.offsetHeight || 60);

          if (tx >= fx + fw) {
            // from left to right
            x1 = fx + fw + 6;
            x2 = tx - 6;
            const midY = fy + fh / 2;
            if (midY >= ty + 20 && midY <= ty + th - 20) {
              y1 = midY;
              y2 = midY;
            } else {
              y1 = midY;
              y2 = ty + th / 2;
            }
          } else if (fx >= tx + tw) {
            // from right to left
            x1 = fx - 6;
            x2 = tx + tw + 6;
            const midY = fy + fh / 2;
            if (midY >= ty + 20 && midY <= ty + th - 20) {
              y1 = midY;
              y2 = midY;
            } else {
              y1 = midY;
              y2 = ty + th / 2;
            }
          } else if (ty >= fy + fh) {
            // from top to bottom
            x1 = fx + fw / 2;
            x2 = tx + tw / 2;
            y1 = fy + fh + 6;
            y2 = ty - 6;
          } else {
            // from bottom to top
            x1 = fx + fw / 2;
            x2 = tx + tw / 2;
            y1 = fy - 6;
            y2 = ty + th + 6;
          }
        }
      }

      const tone = resolveToneName(this.getAttribute('tone')) || 'ink';
      const label = this.getAttribute('label') || '';
      const color = PALETTE.tones[tone]?.strong || PALETTE.ink;

      const minX = Math.min(x1, x2) - 40;
      const minY = Math.min(y1, y2) - 40;
      const w = Math.max(Math.abs(x2 - x1) + 80, 80);
      const h = Math.max(Math.abs(y2 - y1) + 80, 80);

      const localX1 = x1 - minX;
      const localY1 = y1 - minY;
      const localX2 = x2 - minX;
      const localY2 = y2 - minY;

      const angle = Math.atan2(localY2 - localY1, localX2 - localX1);
      const headLen = 16;
      const hx1 = localX2 - headLen * Math.cos(angle - Math.PI / 6);
      const hy1 = localY2 - headLen * Math.sin(angle - Math.PI / 6);
      const hx2 = localX2 - headLen * Math.cos(angle + Math.PI / 6);
      const hy2 = localY2 - headLen * Math.sin(angle + Math.PI / 6);

      this.style.left = `${minX}px`;
      this.style.top = `${minY}px`;
      this.style.width = `${w}px`;
      this.style.height = `${h}px`;

      this.innerHTML = `
        <svg class="sk-svg-bg" viewBox="0 0 ${w} ${h}">
          <path d="${wobbleLine(localX1, localY1, localX2, localY2, 101)}" fill="none" stroke="${color}" stroke-width="2.8" stroke-linecap="round"/>
          <path d="M ${hx1} ${hy1} L ${localX2} ${localY2} L ${hx2} ${hy2}" fill="none" stroke="${color}" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        ${label ? `<div class="sk-arrow-label" style="left:${(localX1 + localX2)/2}px; top:${(localY1 + localY2)/2 - 20}px; color:${color};">${label}</div>` : ''}
      `;
    }
  }

  // 10. Hand Note Marker (sk-note)
  class SkNote extends SkElement {
    connectedCallback() {
      super.connectedCallback();
      this.classList.add('sk-note-text');
      const text = this.getAttribute('text') || this.innerHTML.trim();
      this.innerHTML = text;
    }
  }

  // 11. Bottom Caption Summary (sk-caption)
  class SkCaption extends SkElement {
    connectedCallback() {
      super.connectedCallback();
      this.classList.add('sk-caption-bar');
    }
  }

  // 12. Spark / AI Icon (sk-spark)
  class SkSpark extends SkElement {
    connectedCallback() {
      super.connectedCallback();
      const label = this.getAttribute('label') || 'Claude';
      const size = parseInt(this.getAttribute('size') || '36', 10);
      this.innerHTML = `
        <svg class="sk-spark-icon" style="width:${size}px; height:${size}px;" viewBox="0 0 36 36">
          <path d="M 18 2 Q 18 18 34 18 Q 18 18 18 34 Q 18 18 2 18 Q 18 18 18 2 Z" fill="${PALETTE.tones.purple.strong}" stroke="${PALETTE.ink}" stroke-width="1.6"/>
        </svg>
        <span class="sk-spark-label">${label}</span>
      `;
    }
  }

  // 13. Human Figure (sk-figure)
  class SkFigure extends SkElement {
    connectedCallback() {
      super.connectedCallback();
      const label = this.getAttribute('label') || 'Пользователь';
      this.innerHTML = `
        <svg class="sk-figure-svg" viewBox="0 0 60 80">
          <circle cx="30" cy="18" r="10" fill="#ffffff" stroke="${PALETTE.ink}" stroke-width="2.2"/>
          <line x1="30" y1="28" x2="30" y2="54" stroke="${PALETTE.ink}" stroke-width="2.2" stroke-linecap="round"/>
          <line x1="14" y1="38" x2="46" y2="38" stroke="${PALETTE.ink}" stroke-width="2.2" stroke-linecap="round"/>
          <line x1="30" y1="54" x2="16" y2="76" stroke="${PALETTE.ink}" stroke-width="2.2" stroke-linecap="round"/>
          <line x1="30" y1="54" x2="44" y2="76" stroke="${PALETTE.ink}" stroke-width="2.2" stroke-linecap="round"/>
        </svg>
        <div class="sk-figure-label">${label}</div>
      `;
    }
  }

  // 14. Meter / Fill Indicator (sk-meter)
  class SkMeter extends SkElement {
    connectedCallback() {
      super.connectedCallback();
      const w = parseInt(this.getAttribute('w') || '200', 10);
      const h = parseInt(this.getAttribute('h') || '36', 10);
      const val = Math.min(100, Math.max(0, parseInt(this.getAttribute('value') || '50', 10)));
      const tone = resolveToneName(this.getAttribute('tone')) || 'green';
      const strongColor = PALETTE.tones[tone]?.strong || PALETTE.tones.green.strong;

      const fillW = Math.max(6, Math.round(((w - 8) * val) / 100));
      const { path1, path2 } = wobbleRect(2, 2, w - 4, h - 4, 33);
      const fillPath = wobbleRect(4, 4, fillW, h - 8, 44).path1;

      this.innerHTML = `
        <svg class="sk-svg-bg" viewBox="0 0 ${w} ${h}">
          <path d="${path1}" fill="${PALETTE.paper}" stroke="${PALETTE.ink}" stroke-width="2.2"/>
          <path d="${path2}" fill="none" stroke="${PALETTE.ink}" stroke-width="1.2" opacity="0.5"/>
          <path d="${fillPath}" fill="${strongColor}" opacity="0.85"/>
        </svg>
        <div class="sk-meter-label">${val}%</div>
      `;
    }
  }

  // 15. Dice / Randomness Icon (sk-dice)
  class SkDice extends SkElement {
    connectedCallback() {
      super.connectedCallback();
      const size = parseInt(this.getAttribute('size') || '48', 10);
      const { path1 } = wobbleRect(4, 4, size - 8, size - 8, 55);

      this.innerHTML = `
        <svg class="sk-svg-bg" viewBox="0 0 ${size} ${size}">
          <path d="${path1}" fill="#ffffff" stroke="${PALETTE.ink}" stroke-width="2.2"/>
          <circle cx="${size/2}" cy="${size/2}" r="3" fill="${PALETTE.ink}"/>
        </svg>
      `;
    }
  }

  // Register Custom Elements
  customElements.define('sk-deck', SkDeck);
  customElements.define('sk-slide', SkSlide);
  customElements.define('sk-title', SkTitle);
  customElements.define('sk-box', SkBox);
  customElements.define('sk-doc', SkDoc);
  customElements.define('sk-bubble', SkBubble);
  customElements.define('sk-chip', SkChip);
  customElements.define('sk-mark', SkMark);
  customElements.define('sk-arrow', SkArrow);
  customElements.define('sk-note', SkNote);
  customElements.define('sk-caption', SkCaption);
  customElements.define('sk-spark', SkSpark);
  customElements.define('sk-figure', SkFigure);
  customElements.define('sk-meter', SkMeter);
  customElements.define('sk-dice', SkDice);

})();
