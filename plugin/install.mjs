#!/usr/bin/env node
// plugin/install.mjs
// Copies scaffold infrastructure into the target project.
// Run: node plugin/install.mjs (from target project root)
// Or via npx: npx @agentfolio/plugin

import { cpSync, mkdirSync, existsSync, readFileSync, writeFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const PLUGIN_ROOT = join(__dirname, '..');
const TARGET = process.cwd();

console.log('🤖 Agentfolio Plugin Installer\n');

// Items to copy from plugin root to target
const toCopy = [
  { src: '.github/workflows',       dst: '.github/workflows',       label: 'Workflows (7 files)' },
  { src: '.github/ISSUE_TEMPLATE',  dst: '.github/ISSUE_TEMPLATE',  label: 'Issue templates' },
  { src: 'skills',                  dst: 'skills',                  label: 'Skill files (6 files)' },
  { src: 'state',                   dst: 'state',                   label: 'State templates' },
];

// Files to copy only if they don't exist (don't overwrite user's versions)
const toInitIfMissing = [
  { src: 'CLAUDE.md', dst: 'CLAUDE.md', label: 'Root CLAUDE.md' },
];

let installed = 0;
let skipped = 0;

for (const item of toCopy) {
  const srcPath = join(PLUGIN_ROOT, item.src);
  const dstPath = join(TARGET, item.dst);

  if (!existsSync(srcPath)) {
    console.log(`  ⚠ Skipping ${item.label} (source not found)`);
    skipped++;
    continue;
  }

  mkdirSync(dstPath, { recursive: true });
  cpSync(srcPath, dstPath, { recursive: true });
  console.log(`  ✓ ${item.label}`);
  installed++;
}

for (const item of toInitIfMissing) {
  const srcPath = join(PLUGIN_ROOT, item.src);
  const dstPath = join(TARGET, item.dst);

  if (existsSync(dstPath)) {
    console.log(`  → ${item.label} already exists, skipping`);
    skipped++;
    continue;
  }

  if (!existsSync(srcPath)) continue;

  const content = readFileSync(srcPath, 'utf-8');
  writeFileSync(dstPath, content);
  console.log(`  ✓ ${item.label} (initialized)`);
  installed++;
}

console.log(`\n✅ Installed ${installed} items (${skipped} skipped)\n`);
console.log('Next steps:');
console.log('  1. Create apps/[your-app]/ with CLAUDE.md, FEATURE_STATUS.md, growth_goals.md');
console.log('  2. Update APP_NAME in each workflow file (currently: portfolio)');
console.log('  3. Add ANTHROPIC_API_KEY to GitHub repository secrets');
console.log('  4. Enable GitHub Pages: Settings → Pages → Source: GitHub Actions');
console.log('  5. Run onboard.yml: Actions → Onboard → Run workflow\n');
console.log('Docs: https://github.com/yourusername/agentfolio/blob/main/docs/onboarding.md');
