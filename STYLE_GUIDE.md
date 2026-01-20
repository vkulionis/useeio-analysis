# Design System & Style Guide

A clean, minimalist design system optimized for data visualization dashboards.

---

## Philosophy

- **Clarity over decoration** — Remove visual noise, let data speak
- **Thin lines, no shadows** — Flat design with subtle depth via borders
- **Limited color palette** — Semantic colors only, used consistently
- **Bold typography** — Strong hierarchy through weight, not size
- **Generous whitespace** — Content needs room to breathe

---

## Colors

### Base Palette

```css
/* Backgrounds */
--bg-primary: #ffffff;        /* Main background */
--bg-secondary: #fafafa;      /* Cards, inputs, hover states */
--bg-tertiary: #f0f0f0;       /* Active states, selected items */

/* Borders */
--border-light: #f0f0f0;      /* Table rows, subtle divisions */
--border-default: #e5e5e5;    /* Cards, inputs, primary borders */

/* Text */
--text-primary: #1a1a1a;      /* Headings, primary content */
--text-secondary: #444444;    /* Body text, descriptions */
--text-muted: #666666;        /* Labels, captions */
--text-subtle: #888888;       /* Metadata, hints */
--text-disabled: #aaaaaa;     /* Disabled states */
```

### Semantic Colors

```css
/* Status & Data */
--color-positive: #16a34a;    /* Success, growth, key sectors */
--color-negative: #dc2626;    /* Error, decline, high risk */
--color-warning: #ea580c;     /* Warning, medium risk, forward linkage */
--color-info: #2563eb;        /* Information, backward linkage */
--color-neutral: #9ca3af;     /* Inactive, weak linkage */
```

### Usage Rules

| Context | Color |
|---------|-------|
| Positive values (+$1B, growth) | `#16a34a` |
| Negative values (-$1B, decline) | `#dc2626` |
| Warnings, medium severity | `#ea580c` |
| Information, neutral highlight | `#2563eb` |
| Disabled, inactive | `#9ca3af` |

---

## Typography

### Font Stack

```css
/* Primary - UI and body text */
font-family: 'IBM Plex Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;

/* Monospace - Numbers, data, code */
font-family: 'IBM Plex Mono', 'SF Mono', 'Consolas', monospace;
```

### Scale

| Element | Size | Weight | Color |
|---------|------|--------|-------|
| Page title | 1.5rem | 700 | `#1a1a1a` |
| Section title | 1.1rem | 700 | `#1a1a1a` |
| Card title | 0.85-0.9rem | 700 | `#1a1a1a` |
| Body text | 0.8-0.9rem | 400 | `#444444` |
| Label | 0.7-0.75rem | 500-600 | `#666666` |
| Caption/meta | 0.65-0.7rem | 400 | `#888888` |
| Data values | 1-1.5rem | 600-700 | varies |

### Weight Guidelines

- **700 (Bold)** — Titles, headings, key metrics
- **600 (Semi-bold)** — Labels, important values
- **500 (Medium)** — Selected states, emphasis
- **400 (Regular)** — Body text, descriptions

---

## Spacing

### Base Unit

Use **4px** as the base unit. Common values:

```css
--space-1: 4px;
--space-2: 8px;
--space-3: 12px;
--space-4: 16px;
--space-5: 20px;
--space-6: 24px;
--space-8: 32px;
--space-10: 40px;
```

### Component Spacing

| Component | Padding |
|-----------|---------|
| Page container | 32px |
| Card | 20-24px |
| Table cell | 8-10px horizontal, 8px vertical |
| Button | 10-12px vertical, 16px horizontal |
| Input | 10-12px |
| List item | 10-12px |

### Grid Gaps

| Context | Gap |
|---------|-----|
| Card grid | 24-32px |
| Metric cards | 16px |
| List items | 4px |
| Table rows | 0 (use border) |

---

## Borders & Radius

### Border Widths

```css
--border-width: 1px;          /* Standard - all borders */
--border-width-thick: 2px;    /* Active tabs, focus states */
--border-width-accent: 3px;   /* Selected list items (left border) */
```

### Border Radius

```css
--radius-sm: 2px;             /* Badges, small elements */
--radius-md: 3-4px;           /* Buttons, inputs, cards */
--radius-lg: 4px;             /* Large cards (keep subtle) */
```

### Rules

- **No rounded corners > 4px** — Keep edges sharp
- **1px borders only** — Never use thicker borders for containers
- **Border color: `#e5e5e5`** — Consistent throughout

---

## Components

### Cards

```css
.card {
    background: #ffffff;
    border: 1px solid #e5e5e5;
    border-radius: 4px;
    padding: 20px;
}

/* Alternative: subtle background card */
.card-muted {
    background: #fafafa;
    border: 1px solid #e5e5e5;
    border-radius: 4px;
    padding: 16px;
}
```

### Buttons

```css
/* Primary */
.btn {
    background: #1a1a1a;
    color: #ffffff;
    border: none;
    padding: 10px 16px;
    border-radius: 4px;
    font-size: 0.8rem;
    font-weight: 600;
    cursor: pointer;
}

.btn:hover {
    background: #333333;
}

.btn:disabled {
    opacity: 0.4;
    cursor: not-allowed;
}

/* Secondary/Outline */
.btn-outline {
    background: #ffffff;
    color: #666666;
    border: 1px solid #e5e5e5;
}

.btn-outline:hover {
    background: #fafafa;
}
```

### Inputs

```css
.input {
    width: 100%;
    background: #fafafa;
    border: 1px solid #e5e5e5;
    color: #1a1a1a;
    padding: 10px 12px;
    border-radius: 4px;
    font-size: 0.85rem;
    font-family: inherit;
    outline: none;
}

.input:focus {
    border-color: #1a1a1a;
}

.input::placeholder {
    color: #888888;
}
```

### Tables

```css
.table {
    width: 100%;
    border-collapse: collapse;
}

.table th {
    text-align: left;
    padding: 8px 10px;
    font-size: 0.65rem;
    font-weight: 600;
    color: #666666;
    text-transform: uppercase;
    letter-spacing: 0.3px;
    border-bottom: 1px solid #e5e5e5;
}

.table td {
    padding: 8px 10px;
    font-size: 0.8rem;
    border-bottom: 1px solid #f0f0f0;
}

.table tr:hover {
    background: #fafafa;
}
```

### List Items

```css
.list-item {
    padding: 10px 12px;
    border-radius: 3px;
    margin-bottom: 4px;
    cursor: pointer;
    background: #fafafa;
    border-left: 3px solid transparent;
}

.list-item:hover {
    background: #f0f0f0;
}

.list-item.selected {
    background: #e5e5e5;
    border-left-color: #1a1a1a;
}

/* Semantic variants */
.list-item.positive { border-left-color: #16a34a; }
.list-item.warning { border-left-color: #ea580c; }
.list-item.info { border-left-color: #2563eb; }
```

### Badges

```css
.badge {
    display: inline-block;
    padding: 2px 6px;
    border-radius: 2px;
    font-size: 0.6rem;
    font-weight: 600;
    text-transform: uppercase;
}

.badge-high {
    background: #fef2f2;
    color: #dc2626;
}

.badge-medium {
    background: #fff7ed;
    color: #ea580c;
}

.badge-low {
    background: #f0fdf4;
    color: #16a34a;
}
```

### Progress/Data Bars

```css
.bar {
    height: 4px;
    background: #e5e5e5;
    border-radius: 2px;
    overflow: hidden;
}

.bar-fill {
    height: 100%;
    border-radius: 2px;
    transition: width 0.3s ease;
}

.bar-fill.positive { background: #16a34a; }
.bar-fill.negative { background: #dc2626; }
.bar-fill.warning { background: #ea580c; }
.bar-fill.info { background: #2563eb; }
```

### Tabs

```css
.tabs {
    display: flex;
    border-bottom: 1px solid #e5e5e5;
}

.tab {
    padding: 10px 16px;
    font-size: 0.85rem;
    font-weight: 500;
    color: #666666;
    cursor: pointer;
    border-bottom: 2px solid transparent;
    transition: all 0.15s;
}

.tab:hover {
    color: #1a1a1a;
}

.tab.active {
    color: #1a1a1a;
    border-bottom-color: #1a1a1a;
}
```

### Tooltips

```css
.tooltip {
    position: fixed;
    pointer-events: none;
    background: #ffffff;
    border: 1px solid #e5e5e5;
    padding: 12px 16px;
    border-radius: 4px;
    font-size: 0.8rem;
    max-width: 300px;
    z-index: 1000;
    opacity: 0;
    transition: opacity 0.1s;
}

.tooltip.visible {
    opacity: 1;
}

.tooltip-title {
    font-weight: 600;
    margin-bottom: 8px;
}

.tooltip-row {
    display: flex;
    justify-content: space-between;
    gap: 16px;
    margin-bottom: 3px;
}

.tooltip-label {
    color: #666666;
}

.tooltip-value {
    font-family: 'IBM Plex Mono', monospace;
    font-weight: 500;
}
```

---

## Data Visualization

### Chart Colors

For categorical data (e.g., quadrants):

```css
--chart-green: #16a34a;       /* Key/Primary */
--chart-orange: #ea580c;      /* Secondary */
--chart-blue: #2563eb;        /* Tertiary */
--chart-gray: #9ca3af;        /* Inactive/Weak */
```

### Axes & Grid

```css
/* Axis lines */
stroke: #e5e5e5;
stroke-width: 1;

/* Axis text */
fill: #666666;
font-size: 0.7rem;

/* Reference lines (dashed) */
stroke: #e5e5e5;
stroke-dasharray: none;  /* Solid for this style */
```

### Data Points

```css
/* Default state */
fill-opacity: 0.7;
stroke-width: 1;

/* Hover state */
fill-opacity: 1;
stroke-width: 2;

/* Dimmed (when another is selected) */
fill-opacity: 0.1;
stroke-width: 1;

/* Selected */
fill-opacity: 1;
stroke-width: 3;
stroke: #1a1a1a;
```

---

## Responsive Breakpoints

```css
/* Tablet */
@media (max-width: 1100px) {
    /* Stack grids vertically */
    /* Reduce to 2-column metric grids */
}

/* Mobile */
@media (max-width: 768px) {
    /* Single column everything */
    /* Reduce padding to 16px */
}
```

---

## Scrollbars

```css
::-webkit-scrollbar {
    width: 6px;
}

::-webkit-scrollbar-track {
    background: transparent;
}

::-webkit-scrollbar-thumb {
    background: #e5e5e5;
    border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
    background: #d0d0d0;
}
```

---

## Transitions

```css
/* Standard interaction */
transition: all 0.15s ease;

/* Data animations */
transition: width 0.3s ease;

/* Tooltip */
transition: opacity 0.1s ease;
```

---

## Do's and Don'ts

### ✅ Do

- Use monospace font for all numbers and data values
- Keep borders at 1px
- Use semantic colors consistently
- Add hover states to interactive elements
- Use uppercase + letter-spacing for labels
- Left-align text, right-align numbers

### ❌ Don't

- Add box shadows
- Use border-radius > 4px
- Use more than 4-5 colors
- Make text smaller than 0.65rem
- Use colored backgrounds for cards
- Add decorative elements

---

## Example: Metric Card

```html
<div class="metric-card">
    <div class="metric-label">Total output</div>
    <div class="metric-value positive">+$24.5B</div>
    <div class="metric-detail">Across 411 industries</div>
</div>
```

```css
.metric-card {
    background: #fafafa;
    border: 1px solid #e5e5e5;
    border-radius: 4px;
    padding: 16px;
}

.metric-label {
    font-size: 0.7rem;
    font-weight: 600;
    color: #666666;
    text-transform: uppercase;
    letter-spacing: 0.3px;
    margin-bottom: 6px;
}

.metric-value {
    font-size: 1.5rem;
    font-weight: 700;
    font-family: 'IBM Plex Mono', monospace;
}

.metric-value.positive { color: #16a34a; }
.metric-value.negative { color: #dc2626; }

.metric-detail {
    font-size: 0.7rem;
    color: #888888;
    margin-top: 4px;
}
```

---

## Quick Reference

| Property | Value |
|----------|-------|
| Primary font | IBM Plex Sans |
| Mono font | IBM Plex Mono |
| Border color | #e5e5e5 |
| Border radius | 4px max |
| Primary text | #1a1a1a |
| Muted text | #666666 |
| Background | #ffffff |
| Card background | #fafafa |
| Positive | #16a34a |
| Negative | #dc2626 |
| Warning | #ea580c |
| Info | #2563eb |
