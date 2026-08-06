# HTML/CSS Slide Engine (Light Theme)

## Contents

1. When to use this route
2. Base template framework (Palette A "Crisp Swiss")
3. Palette B variable block ("Warm Editorial")
4. Layout recipes
5. Building the same design in PowerPoint

## When to use this route

Two output routes share one design system:

- **Primary**: native editable `.pptx` (python-pptx or PptxGenJS). Use the
  px→pt conversion table in `design-system.md` §9.
- **This route**: HTML/CSS slides when the deliverable is a browser-based
  deck, a PDF export, or a fast visual prototype that will be rebuilt in
  PowerPoint later.

The HTML canvas is 1280 × 720 px at 96 dpi — exactly one 16:9 PowerPoint
slide. The CSS values below are the source of truth for both routes.

## Base template framework (Palette A "Crisp Swiss")

When outputting HTML/CSS presentation slides, adhere to this precise style
structure:

```html
<style>
  :root {
    --bg-main: #FFFFFF;
    --bg-card: #F1F5F9;
    --text-primary: #020617;
    --text-secondary: #64748B;
    --accent: #4F46E5; /* Vivid Indigo */
    --border-line: #E2E8F0;
  }

  .slide-container {
    width: 1280px;
    height: 720px;
    background-color: var(--bg-main);
    color: var(--text-primary);
    font-family: 'Inter', -apple-system, sans-serif;
    padding: 60px 80px;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    position: relative;
    overflow: hidden;
  }

  /* Badge Pill Accent — tinted background, no border */
  .badge-pill {
    display: inline-flex;
    align-items: center;
    background: rgba(79, 70, 229, 0.08); /* Light accent tint */
    color: var(--accent);
    padding: 6px 16px;
    border-radius: 100px;
    font-size: 14px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
  }

  /* Ultra Bold Section Titles */
  .slide-title {
    font-size: 44px;
    font-weight: 800;
    line-height: 1.15;
    letter-spacing: -1px;
    color: var(--text-primary);
    margin: 0;
  }

  .slide-title span.highlight {
    color: var(--accent);
  }

  /* Hero Number Layout */
  .hero-number {
    font-size: 140px;
    font-weight: 800;
    line-height: 1;
    color: var(--accent);
    letter-spacing: -3px;
  }

  /* Minimalist Card — light fill, no border by default */
  .tile-card {
    background-color: var(--bg-card);
    border: 2px solid transparent;
    border-radius: 16px;
    padding: 32px;
    flex: 1;
  }

  .tile-card.featured {
    border-color: var(--accent); /* crisp 2px accent border */
    background-color: #FFFFFF;
  }

  /* Stark contrast block for Layout 2 */
  .contrast-block {
    background-color: #0F172A; /* deep obsidian; or var(--accent) */
    color: #FFFFFF;
  }

  /* Single soft elevation — never heavier, never with a border */
  .soft-shadow {
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.04);
  }
</style>
```

Load fonts with a self-contained fallback chain; never ship a deck that
depends on a font that may be absent:

```html
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
```

For offline or PDF-export decks, embed the font files or fall back to
`'Inter', 'Helvetica Neue', Arial, sans-serif`.

## Palette B variable block ("Warm Editorial")

Swap the `:root` block and the badge tint; everything else stays identical:

```css
:root {
  --bg-main: #FDFBF7;
  --bg-card: #F3F0E6;
  --text-primary: #1C1917;
  --text-secondary: #78716C;
  --accent: #EA580C; /* Burnt Orange — hero-size only on alabaster */
  --border-line: #E7E2D8;
}

.badge-pill {
  background: rgba(234, 88, 12, 0.08);
}

.contrast-block {
  background-color: #EA580C;
  color: #1C1917; /* deep stone on orange keeps 4.9:1; white would fail */
}
```

Crimson variant: `--accent: #DC2626;` with badge tint
`rgba(220, 38, 38, 0.08)`; crimson keeps 4.7:1 on alabaster, so it may also
carry badge and short-label text.

## Layout recipes

All recipes live inside `.slide-container`.

### Layout 1 — Hero Metric

```html
<div class="slide-container">
  <span class="badge-pill">Q2 · Retention</span>
  <div>
    <div class="hero-number">87%</div>
    <p style="color: var(--text-secondary); font-size: 18px; max-width: 560px;">
      khách hàng quay lại sau khi thời gian thanh toán giảm còn 4 phút.
    </p>
  </div>
  <span style="color: var(--text-secondary); font-size: 12px;">
    Nguồn: khảo sát nội bộ, 05/2026 · Số liệu thực tế
  </span>
</div>
```

The rest of the slide stays empty white space. Resist the urge to fill it.

### Layout 2 — Stark Editorial Split

```html
<div class="slide-container" style="padding: 0; flex-direction: row;">
  <div style="width: 50%; padding: 60px 56px; display: flex;
              flex-direction: column; justify-content: center; gap: 24px;">
    <span class="badge-pill">Chương 2</span>
    <h2 class="slide-title">Khách rời đi vì <span class="highlight">thanh toán chậm</span></h2>
  </div>
  <div class="contrast-block" style="width: 50%; display: flex;
       align-items: center; padding: 60px;">
    <!-- one key quote or statement; or a full-bleed image instead -->
  </div>
</div>
```

### Layout 3 — Max-3 Tiles

```html
<div class="slide-container">
  <h2 class="slide-title">Ba việc cần làm trong quý này</h2>
  <div style="display: flex; gap: 24px;">
    <div class="tile-card">…</div>
    <div class="tile-card featured">…</div> <!-- exactly ONE featured -->
    <div class="tile-card">…</div>
  </div>
</div>
```

Never render a fourth tile; split the content across slides instead.

### Layout 4 — Bold Statement / Minimal Quote

```html
<div class="slide-container" style="justify-content: center;">
  <blockquote style="margin: 0; padding-left: 32px;
                     border-left: 4px solid var(--accent);
                     font-size: 56px; font-weight: 800; line-height: 1.2;
                     color: var(--text-primary); max-width: 960px;">
    “Chúng tôi không cần thêm báo cáo. Chúng tôi cần bớt ba bước phê duyệt.”
  </blockquote>
  <p style="color: var(--text-secondary); margin-top: 24px;">
    Giám đốc vận hành, khách hàng sản xuất — phỏng vấn 03/2026
  </p>
</div>
```

## Building the same design in PowerPoint

When the deliverable is `.pptx`, translate this template instead of exporting
screenshots:

- Slide background → slide background fill (`--bg-main`).
- `.badge-pill` → rounded-full auto-shape filled with the pre-computed 8%
  tint (`#F1F0FD` indigo, `#EBF7F3` emerald, `#FDF2EC` orange, `#FCEEEE`
  crimson), no outline, 10.5 pt uppercase tracked accent text.
- `.hero-number` → 90–120 pt text box, bold, accent fill, tight character
  spacing.
- `.tile-card` → rounded rectangle, 0.16 in radius, light card fill, no
  outline; featured card gets a 1.5 pt accent outline.
- `.contrast-block` → full-height rectangle in obsidian or accent with
  contrast-checked text color (§11 of design-system.md).
- Prefer flat cards in `.pptx`: areas are defined by tint fills, hairlines,
  or accent borders. Gotcha: python-pptx writes a `p:style` whose
  `a:effectRef` points at theme effect styles; the bundled default theme has
  no `effectStyleList`, and LibreOffice then falls back to a drop shadow for
  any effectRef index. Remove the `p:style` element from the shape for
  guaranteed flat cards (fill, line, and run fonts are set explicitly and do
  not need it). If the deck deliberately wants its single soft elevation,
  add an explicit `a:effectLst` outer shadow (≈ 4% black alpha) in `spPr`
  instead — never mix shadow and border on one card.
- Editable native text always wins over flattened images. Do not flatten
  unless fidelity requires it and the user accepts the tradeoff.
