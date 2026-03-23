import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: process.env.SITE_URL || 'https://tokenman.io',
  base: process.env.BASE_PATH || '/',
  integrations: [
    tailwind(),
    sitemap(),
  ],
  output: 'static',
});
