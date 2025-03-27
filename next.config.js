/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  basePath: '/portfolio-site',
  assetPrefix: '/portfolio-site/',
  images: {
    unoptimized: true,
  },
}

module.exports = nextConfig 