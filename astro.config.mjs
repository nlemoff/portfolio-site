import { defineConfig } from 'astro/config';

// Static site for GitHub Pages (custom domain www.nlemoff.com, served from the root).
export default defineConfig({
  site: 'https://www.nlemoff.com',
  outDir: './out',
  build: { inlineStylesheets: 'never' },
});
