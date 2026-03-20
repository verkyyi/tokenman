import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import sitemap from '@astrojs/sitemap';

// Read site URL from profile.json at build time
// Falls back to GitHub Pages URL pattern
let siteUrl = 'https://yourusername.github.io';
try {
  const profile = JSON.parse(
    await import('fs').then(fs =>
      fs.readFileSync('./content/profile.json', 'utf-8')
    )
  );
  if (profile.site_url) siteUrl = profile.site_url;
} catch {}

export default defineConfig({
  site: siteUrl,
  integrations: [
    tailwind(),
    sitemap(),
  ],
  // Static output — deploys to GitHub Pages
  output: 'static',
});
