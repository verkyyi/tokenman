# Landing Page Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the current agent dashboard with a clean, mobile-first developer-tool landing page that explains Agentfolio and drives adoption.

**Architecture:** Complete rewrite of `src/pages/index.astro` (remove all state file reads and client-side JS) and simplification of `src/layouts/Base.astro` (remove agent badge, GitHub API calls, relative-time scripts). Single-page static site with 6 sections using scoped CSS.

**Tech Stack:** Astro 4.16, Tailwind CSS 3.4, static output to GitHub Pages. No client-side JavaScript.

**Spec:** `docs/superpowers/specs/2026-03-22-landing-page-redesign-design.md`

---

### Task 1: Simplify Base.astro layout

Strip the layout down to a clean HTML shell. Remove agent badge, state file reads, client-side JavaScript, cosmic gradient, and glowing pseudo-elements.

**Files:**
- Modify: `src/layouts/Base.astro` (complete rewrite of lines 1-206)

- [ ] **Step 1: Rewrite Base.astro**

Replace the entire file with a minimal layout. Remove:
- The `readFileSync` imports and agent log parsing (lines 1-29)
- The agent badge HTML (lines 55-65)
- The `<script>` block with relative-time formatting and GitHub API calls (lines 67-130)
- The cosmic gradient body styles and glowing pseudo-elements (lines 134-167)
- The agent badge styles (lines 169-204)

New content:

```astro
---
interface Props {
  title?: string;
  description?: string;
}

const {
  title = 'Agentfolio — Self-evolving GitHub Actions for any repo',
  description = 'Add an autonomous dev pipeline to your GitHub repo. 11 workflows that research, triage, code, review, and deploy.'
} = Astro.props;
---

<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <meta name="description" content={description} />
  <link rel="canonical" href={Astro.url.href} />
  <meta property="og:type" content="website" />
  <meta property="og:title" content={title} />
  <meta property="og:description" content={description} />
  <meta property="og:url" content={Astro.url.href} />
  <meta property="og:site_name" content="Agentfolio" />
  <meta name="twitter:card" content="summary" />
  <meta name="twitter:title" content={title} />
  <meta name="twitter:description" content={description} />
  <meta name="robots" content="index, follow" />
  <meta name="generator" content={Astro.generator} />
  <link rel="sitemap" href="/sitemap-index.xml" />
</head>
<body>
  <slot />
</body>
</html>

<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  html { overflow-x: hidden; }
  body {
    font-family: system-ui, -apple-system, sans-serif;
    background: #0d1117;
    color: #e6edf3;
    min-height: 100vh;
    overflow-x: hidden;
    width: 100%;
  }
</style>
```

- [ ] **Step 2: Verify the build compiles**

Run: `cd /home/dev/projects/agentfolio && npm run build`
Expected: Build succeeds (the page will be unstyled but functional)

- [ ] **Step 3: Commit**

```bash
git add src/layouts/Base.astro
git commit -m "feat(profile): simplify Base.astro — remove dashboard artifacts"
```

---

### Task 2: Rewrite index.astro — Hero section

Start the page rewrite with the hero. Remove all state file imports and the entire old page. Build the hero section mobile-first.

**Files:**
- Modify: `src/pages/index.astro` (complete rewrite of lines 1-551)

- [ ] **Step 1: Replace index.astro with hero section**

Remove all `readFileSync` imports, state parsing logic (lines 1-139), and the entire old template + styles (lines 140-551). Replace with:

```astro
---
import Base from '../layouts/Base.astro';
---

<Base>
  <main class="page">

    <!-- Hero -->
    <section class="hero">
      <p class="wordmark">Agentfolio</p>
      <h1 class="headline">Self-evolving GitHub Actions for any repo</h1>
      <p class="subtitle">
        11 workflows that research, triage, code, review, and deploy — autonomously.
        Add to your project with Claude Code.
      </p>
      <div class="hero-actions">
        <a href="#get-started" class="btn-primary">Get Started</a>
        <a href="https://github.com/verkyyi/agentfolio" target="_blank" rel="noopener noreferrer" class="btn-secondary">View on GitHub</a>
      </div>
    </section>

  </main>
</Base>

<style>
  .page {
    max-width: 640px;
    margin: 0 auto;
    padding: 48px 20px;
  }

  /* Hero */
  .hero {
    text-align: center;
    padding: 40px 0 48px;
  }
  .wordmark {
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #7d8590;
    margin-bottom: 16px;
  }
  .headline {
    font-size: 28px;
    font-weight: 700;
    line-height: 1.3;
    color: #e6edf3;
    margin-bottom: 16px;
  }
  .subtitle {
    font-size: 15px;
    color: #7d8590;
    line-height: 1.6;
    margin-bottom: 32px;
  }
  .hero-actions {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }
  .btn-primary {
    display: inline-flex;
    justify-content: center;
    align-items: center;
    padding: 12px 24px;
    background: #238636;
    color: #fff;
    font-size: 14px;
    font-weight: 600;
    border-radius: 6px;
    text-decoration: none;
    min-height: 44px;
  }
  .btn-primary:hover { background: #2ea043; }
  .btn-secondary {
    display: inline-flex;
    justify-content: center;
    align-items: center;
    padding: 12px 24px;
    background: transparent;
    color: #e6edf3;
    font-size: 14px;
    font-weight: 600;
    border-radius: 6px;
    text-decoration: none;
    border: 1px solid #30363d;
    min-height: 44px;
  }
  .btn-secondary:hover { border-color: #8b949e; }

  /* Desktop: inline buttons */
  @media (min-width: 640px) {
    .hero { padding: 64px 0 56px; }
    .headline { font-size: 36px; }
    .hero-actions {
      flex-direction: row;
      justify-content: center;
    }
  }
</style>
```

- [ ] **Step 2: Verify build and preview**

Run: `cd /home/dev/projects/agentfolio && npm run build`
Expected: Build succeeds. Single page with centered hero.

- [ ] **Step 3: Commit**

```bash
git add src/pages/index.astro
git commit -m "feat(profile): rewrite index.astro — hero section, mobile-first"
```

---

### Task 3: Add "What It Does" section

Four capability rows below the hero.

**Files:**
- Modify: `src/pages/index.astro` (add section after hero, add styles)

- [ ] **Step 1: Add the What It Does section**

Insert after the closing `</section>` of the hero, before `</main>`:

```astro
    <!-- What It Does -->
    <section class="section">
      <h2 class="section-label">What it does</h2>
      <div class="capabilities">
        <div class="capability">
          <span class="cap-name">Evolve</span>
          <span class="cap-desc">Researches your ecosystem hourly, opens issues</span>
        </div>
        <div class="capability">
          <span class="cap-name">Triage</span>
          <span class="cap-desc">Classifies and routes every new issue</span>
        </div>
        <div class="capability">
          <span class="cap-name">Code + Review</span>
          <span class="cap-desc">Implements on branches, reviews its own PRs</span>
        </div>
        <div class="capability">
          <span class="cap-name">Deploy</span>
          <span class="cap-desc">Builds and ships on merge</span>
        </div>
      </div>
    </section>
```

- [ ] **Step 2: Add styles for this section**

Append to the `<style>` block:

```css
  /* Sections */
  .section {
    padding: 32px 0;
    border-top: 1px solid #21262d;
  }
  .section-label {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #7d8590;
    margin-bottom: 20px;
  }

  /* Capabilities */
  .capabilities {
    display: flex;
    flex-direction: column;
    gap: 16px;
  }
  .capability {
    display: flex;
    flex-direction: column;
    gap: 4px;
  }
  .cap-name {
    font-size: 14px;
    font-weight: 600;
    color: #e6edf3;
  }
  .cap-desc {
    font-size: 14px;
    color: #7d8590;
    line-height: 1.5;
  }

  @media (min-width: 640px) {
    .capabilities {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 20px;
    }
  }
```

- [ ] **Step 3: Verify build**

Run: `cd /home/dev/projects/agentfolio && npm run build`
Expected: Build succeeds.

- [ ] **Step 4: Commit**

```bash
git add src/pages/index.astro
git commit -m "feat(profile): add What It Does section"
```

---

### Task 4: Add "How It Works" pipeline section

Horizontal pipeline on desktop, vertical on mobile.

**Files:**
- Modify: `src/pages/index.astro` (add section, add styles)

- [ ] **Step 1: Add the How It Works section**

Insert after the What It Does section, before `</main>`:

```astro
    <!-- How It Works -->
    <section class="section">
      <h2 class="section-label">How it works</h2>
      <div class="pipeline">
        <div class="pipe-step">
          <span class="pipe-name">Evolve</span>
          <span class="pipe-freq">hourly</span>
        </div>
        <span class="pipe-arrow" aria-hidden="true"></span>
        <div class="pipe-step">
          <span class="pipe-name">Triage</span>
          <span class="pipe-freq">per issue</span>
        </div>
        <span class="pipe-arrow" aria-hidden="true"></span>
        <div class="pipe-step">
          <span class="pipe-name">Code</span>
          <span class="pipe-freq">per issue</span>
        </div>
        <span class="pipe-arrow" aria-hidden="true"></span>
        <div class="pipe-step">
          <span class="pipe-name">Review</span>
          <span class="pipe-freq">per PR</span>
        </div>
        <span class="pipe-arrow" aria-hidden="true"></span>
        <div class="pipe-step">
          <span class="pipe-name">Deploy</span>
          <span class="pipe-freq">on merge</span>
        </div>
      </div>
    </section>
```

- [ ] **Step 2: Add pipeline styles**

Append to the `<style>` block:

```css
  /* Pipeline */
  .pipeline {
    display: flex;
    flex-direction: column;
    align-items: stretch;
    gap: 0;
  }
  .pipe-step {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 16px;
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 6px;
  }
  .pipe-name {
    font-size: 14px;
    font-weight: 600;
    color: #e6edf3;
  }
  .pipe-freq {
    font-size: 12px;
    color: #7d8590;
  }
  .pipe-arrow {
    display: flex;
    justify-content: center;
    padding: 4px 0;
    color: #30363d;
    font-size: 0;
  }
  .pipe-arrow::after {
    content: '\2193'; /* ↓ */
    font-size: 14px;
  }

  @media (min-width: 640px) {
    .pipeline {
      flex-direction: row;
      align-items: center;
      gap: 0;
    }
    .pipe-step {
      flex: 1;
      flex-direction: column;
      text-align: center;
      gap: 4px;
    }
    .pipe-arrow {
      padding: 0 4px;
    }
    .pipe-arrow::after {
      content: '\2192'; /* → */
    }
  }
```

- [ ] **Step 3: Verify build**

Run: `cd /home/dev/projects/agentfolio && npm run build`
Expected: Build succeeds.

- [ ] **Step 4: Commit**

```bash
git add src/pages/index.astro
git commit -m "feat(profile): add How It Works pipeline section"
```

---

### Task 5: Add "Use Cases" section

Three cards stacked on mobile, row on desktop.

**Files:**
- Modify: `src/pages/index.astro` (add section, add styles)

- [ ] **Step 1: Add the Use Cases section**

Insert after the How It Works section, before `</main>`:

```astro
    <!-- Use Cases -->
    <section class="section">
      <h2 class="section-label">Best for</h2>
      <div class="use-cases">
        <div class="use-case">
          <h3 class="uc-title">Open-source projects</h3>
          <p class="uc-desc">Auto-triage issues, research your ecosystem, ship fixes</p>
        </div>
        <div class="use-case">
          <h3 class="uc-title">Personal websites</h3>
          <p class="uc-desc">Content updates, self-healing deploys, zero maintenance</p>
        </div>
        <div class="use-case">
          <h3 class="uc-title">Any GitHub repo</h3>
          <p class="uc-desc">Add autonomous CI to what you already have</p>
        </div>
      </div>
    </section>
```

- [ ] **Step 2: Add use case styles**

Append to the `<style>` block:

```css
  /* Use Cases */
  .use-cases {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }
  .use-case {
    padding: 16px;
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 6px;
  }
  .uc-title {
    font-size: 14px;
    font-weight: 600;
    color: #e6edf3;
    margin-bottom: 4px;
  }
  .uc-desc {
    font-size: 14px;
    color: #7d8590;
    line-height: 1.5;
  }

  @media (min-width: 640px) {
    .use-cases {
      flex-direction: row;
    }
    .use-case {
      flex: 1;
    }
  }
```

- [ ] **Step 3: Verify build**

Run: `cd /home/dev/projects/agentfolio && npm run build`
Expected: Build succeeds.

- [ ] **Step 4: Commit**

```bash
git add src/pages/index.astro
git commit -m "feat(profile): add Use Cases section"
```

---

### Task 6: Add "Get Started" section and footer

The CTA section with onboarding steps and a code block, plus the footer.

**Files:**
- Modify: `src/pages/index.astro` (add sections, add styles)

- [ ] **Step 1: Add the Get Started section and footer**

Insert after the Use Cases section, before `</main>`:

```astro
    <!-- Get Started -->
    <section class="section" id="get-started">
      <h2 class="section-label">Get started</h2>
      <ol class="steps">
        <li>Open Claude Code in your repo</li>
        <li>Paste this prompt:</li>
      </ol>
      <div class="code-block">
        <code>Set up agentfolio in this repo. Follow https://github.com/verkyyi/agentfolio/blob/main/docs/onboarding.md</code>
      </div>
      <ol class="steps" start="3">
        <li>Claude analyzes your stack, writes config, copies workflows</li>
        <li>Push and enable GitHub Actions</li>
      </ol>
      <p class="started-note">
        Works best with public repos deployed to GitHub Pages.
        Open-source projects and personal websites are ideal starting points.
      </p>
    </section>

    <!-- Footer -->
    <footer class="footer">
      <a href="https://github.com/verkyyi/agentfolio" target="_blank" rel="noopener noreferrer">GitHub</a>
      <span class="footer-sep">·</span>
      <span>MIT License</span>
      <span class="footer-sep">·</span>
      <span>Built with Astro</span>
    </footer>
```

- [ ] **Step 2: Add Get Started and footer styles**

Append to the `<style>` block:

```css
  /* Get Started */
  .steps {
    padding-left: 20px;
    margin-bottom: 16px;
  }
  .steps li {
    font-size: 14px;
    color: #e6edf3;
    line-height: 1.8;
  }
  .code-block {
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 6px;
    padding: 16px;
    margin-bottom: 16px;
    overflow-x: auto;
  }
  .code-block code {
    font-size: 13px;
    color: #e6edf3;
    font-family: ui-monospace, 'SF Mono', 'Fira Code', monospace;
    line-height: 1.6;
    white-space: pre-wrap;
    word-break: break-word;
  }
  .started-note {
    font-size: 13px;
    color: #7d8590;
    line-height: 1.6;
    margin-top: 16px;
  }

  /* Footer */
  .footer {
    padding: 32px 0;
    border-top: 1px solid #21262d;
    text-align: center;
    font-size: 13px;
    color: #7d8590;
  }
  .footer a {
    color: #7d8590;
    text-decoration: none;
  }
  .footer a:hover { color: #e6edf3; }
  .footer-sep {
    margin: 0 8px;
    color: #30363d;
  }
```

- [ ] **Step 3: Verify full build**

Run: `cd /home/dev/projects/agentfolio && npm run build`
Expected: Build succeeds. All 6 sections present in the output.

- [ ] **Step 4: Commit**

```bash
git add src/pages/index.astro
git commit -m "feat(profile): add Get Started section and footer"
```

---

### Task 7: Visual verification and final cleanup

Preview the built site, check mobile and desktop rendering, fix any issues.

**Files:**
- Possibly modify: `src/pages/index.astro`, `src/layouts/Base.astro`

- [ ] **Step 1: Build and preview**

Run: `cd /home/dev/projects/agentfolio && npm run build && npm run preview`
Open the preview URL. Check:
- All 6 sections render correctly
- Mobile view (375px): buttons stack, pipeline is vertical, cards stack
- Desktop view (>640px): buttons inline, pipeline horizontal, cards in a row
- "Get Started" anchor link works from hero CTA
- "View on GitHub" link opens the repo
- Code block is readable and scrolls on narrow screens
- No horizontal overflow on any viewport
- Footer displays correctly

- [ ] **Step 2: Fix any issues found**

Address layout, spacing, or content issues discovered during preview.

- [ ] **Step 3: Final commit**

```bash
git add src/pages/index.astro src/layouts/Base.astro
git commit -m "feat(profile): landing page redesign — clean, mobile-first, developer-minimal"
```

---

### Task Summary

| Task | Description | Key Files |
|------|-------------|-----------|
| 1 | Simplify Base.astro | `src/layouts/Base.astro` |
| 2 | Hero section | `src/pages/index.astro` |
| 3 | What It Does section | `src/pages/index.astro` |
| 4 | How It Works pipeline | `src/pages/index.astro` |
| 5 | Use Cases section | `src/pages/index.astro` |
| 6 | Get Started + Footer | `src/pages/index.astro` |
| 7 | Visual verification | Both files |

Tasks 2-6 all modify the same file (`index.astro`) and must be executed sequentially. Task 1 can run independently (modifies a different file). Task 7 depends on all previous tasks.
