# Deployment Changes

## Summary
The deployment workflow has been changed from Vercel to GitHub Pages.

## Changes Made

### 1. Updated `.github/workflows/deploy.yml`
- **Before**: Deployed to Vercel using Vercel CLI and secrets
- **After**: Deploys to GitHub Pages using GitHub Actions

### 2. Key Differences

#### Removed:
- Vercel-specific environment variables (`VERCEL_ORG_ID`, `VERCEL_PROJECT_ID`)
- Vercel CLI installation and commands
- Vercel Token requirement

#### Added:
- GitHub Pages permissions (contents: read, pages: write, id-token: write)
- Proper build and deploy jobs for GitHub Pages
- Uses official GitHub Pages actions (`actions/configure-pages@v4`, `actions/upload-pages-artifact@v3`, `actions/deploy-pages@v4`)

## What You Need to Do

### 1. Enable GitHub Pages in Repository Settings
1. Go to your repository settings
2. Navigate to **Pages** section (under "Code and automation")
3. Under "Build and deployment":
   - **Source**: Select "GitHub Actions"
4. Save the changes

### 2. Remove Vercel Secrets (Optional)
If you want to clean up, you can remove these secrets from your repository:
- `VERCEL_TOKEN`
- `VERCEL_ORG_ID`
- `VERCEL_PROJECT_ID`

Go to: Settings → Secrets and variables → Actions

### 3. Push to Main Branch
Once you merge this PR and push to the `main` branch, the workflow will automatically:
1. Build your Next.js site as a static export
2. Deploy it to GitHub Pages
3. Make it available at `https://<username>.github.io/<repository-name>/`

## Technical Details

The workflow now:
1. **Build Job**: 
   - Checks out the code
   - Sets up Node.js 20 with npm caching
   - Installs dependencies with `npm ci`
   - Builds the Next.js site with `npm run build` (which creates the `out` directory)
   - Uploads the `out` directory as a Pages artifact

2. **Deploy Job**:
   - Depends on the build job
   - Uses the official GitHub Pages deployment action
   - Deploys the artifact to GitHub Pages
   - Provides the deployment URL

## Configuration Already in Place

Your `next.config.js` is already correctly configured for static export:
```javascript
output: 'export',
images: { unoptimized: true },
distDir: 'out',
trailingSlash: true,
```

This ensures Next.js builds a static site that's compatible with GitHub Pages.
