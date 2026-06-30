# Wincars — Design System Rules (for Figma MCP)

## Current state of this repository

This repository does **not** yet contain a frontend codebase. It currently
holds only design documentation:

- `DESIGN_GUIDELINE.md` — pointer to the Figma design guideline
- `.claude/settings.local.json` — local Claude Code permissions

There is **no component library, no token files, no build system, and no
styling framework implemented in code yet**. The single source of truth for
the design system today is the Figma file below. Everything in this doc is
derived from that file so that Figma MCP tools (`get_design_context`,
`get_design_system`, `use_figma`, etc.) produce output consistent with the
brand — and so that whoever builds the actual app has a starting spec to
implement tokens/components from.

**Figma files**:
- **WINCARS-Poland** — `https://www.figma.com/design/cVG8QGhFsJzdVNQE3Kf7nr/WINCARS-Poland`
  Pages:
  - `Home + правки` (node `0:1`) — main site mockup + review notes
  - `Onboarding v2 (Wincars)` (node `361:344`) — AB Soft-structure onboarding slide deck variant (16:9), RU
- **Onboarding Deck (Wincars)** — `https://www.figma.com/design/eMB0d4zxvVFVI8izlIFYys/Onboarding-Deck--Wincars-`
  (node `1:124`) — primary 16-slide onboarding deck (16:9), RU. Separate file from WINCARS-Poland —
  always confirm which file key a request targets before calling `use_figma`.

---

## 1. Design Tokens

No token files exist in code (no `tokens.json`, `theme.ts`, Tailwind config,
etc.). Tokens below are read directly from the Figma file and
`DESIGN_GUIDELINE.md`. When a token system is introduced, mirror this
structure (e.g. as CSS custom properties, a Tailwind theme, or a Style
Dictionary source file).

### Colors

| Token              | Hex       | RGB (0–1)                         | Usage |
|--------------------|-----------|------------------------------------|-------|
| `color.yellow`        | `#FFCD11` | `1, 0.8039, 0.0667`              | Primary brand accent, CTAs |
| `color.yellow-light`  | `#FFDE64` | `1, 0.8706, 0.3922`              | Hero headings, secondary accent |
| `color.dark`          | `#0F1013` | `0.0588, 0.0627, 0.0745`         | Dark sections, footer, hero overlay |
| `color.white`         | `#FFFFFF` | `1, 1, 1`                        | Base background / text on dark |
| `color.black`         | `#000000` | `0, 0, 0`                        | Primary text on light |
| `color.gray-medium-dark` | `#4E4949` | `0.306, 0.286, 0.286`         | Body text on light (FAQ, paragraphs) |
| `color.gray-light-bg` | `#F5F5F4` | `0.965, 0.965, 0.957`            | Light section / card backgrounds |
| `color.yellow-pale`   | `#FFF8D9` | `1, 0.973, 0.851`                | Highlight section backgrounds |

CTA buttons additionally use a glass effect:
`background: rgba(255,255,255,0.2)`, `border: 1px solid rgba(255,229,132,0.49)`,
`backdrop-blur: ~2-3px`, `border-radius: 35px` (pill).

### Typography

Fonts: **Inter** (UI/body) and **Bebas Neue** (display headings).

| Style token        | Font / Weight              | Size  | Line height | Notes |
|---------------------|----------------------------|-------|-------------|-------|
| `text.h1-hero`      | Bebas Neue, Regular        | 72px  | 0.8 (80%)   | Hero "Sprowadź" style headline, letter-spacing 0.5 |
| `text.h2-section`   | Inter, Bold                | 32px  | 40px        | Section headings (e.g. FAQs) |
| `text.h2-display`   | Inter, Extra Bold          | 48–64px | ~108%     | Large content-slide titles |
| `text.body-medium`  | Inter, Medium              | 16–18px | 22–28px   | Nav links, intro paragraphs |
| `text.body-regular` | Inter, Semi Bold            | 16–18px | 26–28px   | Paragraph copy — onboarding decks use Semi Bold (not Regular) for all body/description text for better legibility on dark and pale backgrounds |
| `text.body-light`   | Inter, Light               | 50px  | 69px        | Hero subline ("samochód marzeń") |
| `text.label`        | Inter, Medium, uppercase   | 11–13px | —          | Pills/tags, letter-spacing 1.5px |
| `text.paragraph-bold` | Inter, Bold              | 16px  | 26px        | FAQ questions, letter-spacing 0.08px |
| `text.cta`          | Inter, Semi Bold, uppercase | 16px | 1.2         | Buttons |

> Gotcha: in the Figma API, weight variants are named `"Semi Bold"` and
> `"Extra Bold"` (with a space) — not `"SemiBold"`/`"ExtraBold"`.

### Spacing

8px base grid: `4, 8, 12, 16, 24, 32, 48, 64, 80, 120` px.
Section/page horizontal padding on the main site is **120px** (desktop,
1440px frame). Onboarding deck slides (1920×1080) use **80–120px** outer
padding and **40px** gaps between bento cards.

### Border Radius

| Token | Value | Usage |
|-------|-------|-------|
| `radius.none` | 0 | — |
| `radius.sm`   | 4px | small elements |
| `radius.md`   | 8px | inputs |
| `radius.lg`   | 12–13px | cards, hero image |
| `radius.full` | 26–35px / 100px | pill buttons, tags (main site CTAs) |

### Section pill / label component

Onboarding-deck section pills (e.g. "SECTION 1", "ONBOARDING", "О КОМПАНИИ")
use a **standardized**, fully-rounded pill style:

- Padding: **30px horizontal, 16px vertical**
- Corner radius: **90px**
- Auto-layout frame, single text child, `Inter Semi Bold`, uppercase,
  letter-spacing ~1.5px
- Built via `use_figma` as an auto-layout frame (`primaryAxisSizingMode`/
  `counterAxisSizingMode: "AUTO"`) so width hugs the label text

When adding new pills to any onboarding/slide-deck file, match this spec
exactly so all pills render uniformly — this was retrofitted across both
onboarding decks (see Practical notes below for the standardization script
pattern).

### Shadows / Elevation

`sm`, `md`, `lg`, and a yellow "glow" elevation (used on hover states, e.g.
car-card hover border + glow). No concrete shadow values are codified yet —
extract per-component from Figma when implementing.

---

## 2. Component Library

No code component library exists. The Figma file's "Home + правки" page
contains the component inventory to be implemented, including:

- **Header / Nav** — logo, nav links with active underline, CTA pill button
- **Hero** — full-bleed image with gradient overlay, headline, sub-line, CTA,
  bottom split links ("Import auta z USA" / "Import auta z Kanady")
- **Car Card** — default + hover states (yellow border + glow)
- **FAQ / Accordion** — question row + plus icon + divider line, two-column
  grid, expand/collapse
- **Footer** — dark background, logo, link columns, contact row, copyright
- **Buttons / CTAs** — Primary (solid yellow pill), Secondary (glass pill),
  Arrow CTA, Hover, Disabled states
- **Form elements** — default/focused input, list/menu row

When building these as code components, name them to match the Figma layer
names above (`Header`, `Hero`, `CTA -2`, `FAQs`, `Footer`, etc.) so Code
Connect / `get_code_connect_map` can map cleanly between Figma and code.

---

## 3. Frameworks & Libraries

**None chosen yet.** This is a greenfield implementation. Until a stack is
selected:

- Treat `clientFrameworks: "unknown"` / `clientLanguages: "unknown"` as
  accurate when calling `get_design_context`.
- Do not assume React/Tailwind — the Figma MCP returns React+Tailwind
  reference code by default, but it **must be translated** to whatever stack
  is chosen for this project before being committed.
- No bundler, package.json, or lockfile exists in the repo yet.

---

## 4. Asset Management

All current assets (photos, icons, logos) live only inside the Figma file
and are exported on demand via `get_design_context` / `download_assets`
(temporary `figma.com/api/mcp/asset/...` URLs, valid ~7 days). There is no
`/public`, `/assets`, or CDN setup in this repo yet. When implementing,
download and re-host these assets locally (e.g. `/public/images`,
`/public/icons`) rather than linking to Figma's temporary URLs.

---

## 5. Icon System

Icons currently exist as Figma vector layers/instances only (e.g. "Plus
icon", arrow vectors `Group 9266`, "Vector"). No icon font or SVG sprite
system exists in code. Recommended when implementing: export as individual
SVGs and either inline them as components or use an SVG sprite, named after
their Figma layer names (e.g. `icon-plus.svg`, `icon-arrow.svg`).

---

## 6. Styling Approach

Not yet decided in code. Figma source uses absolute/auto-layout frames with:

- Flat color fills (see token table above)
- 1px hairline dividers/borders
- Rounded corners per `radius.*` tokens
- A dark/light/yellow alternating section rhythm (see Onboarding Deck for a
  reference of this rhythm in practice)

No global stylesheet, CSS Modules, or styled-components setup exists yet.
Responsive behavior is not yet specified — the only frame size documented is
desktop (1440px wide for the site, 1920×1080 for the onboarding deck).

---

## 7. Project Structure

```
/home/user/Wincars
├── DESIGN_GUIDELINE.md   # pointer to Figma design guideline page
├── CLAUDE.md             # this file
└── .claude/
    └── settings.local.json
```

There is no `src/`, `components/`, or feature-folder structure yet. When
scaffolding the app, propose a structure (framework + folder layout) before
generating components, and update this file with the chosen conventions so
future Figma MCP-driven work follows them.

---

## Practical notes for Figma MCP usage in this repo

- File key: `cVG8QGhFsJzdVNQE3Kf7nr`
- Always confirm which **page** (`Home + правки` vs `Onboarding Deck
  (Wincars)`) and **node id** you're targeting — `get_metadata` without a
  `nodeId` only lists top-level pages.
- `figma.currentPage` is read-only in the plugin sandbox — use
  `await figma.setCurrentPageAsync(page)`.
- Reuse the color/typography tokens above when generating new Figma content
  via `use_figma` so new pages stay visually consistent with `Home + правки`.
