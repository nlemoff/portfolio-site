import { Metadata } from 'next';

export const siteConfig = {
  name: "nlemoff.com",
  description: "Immersive portfolio of a creative developer, set in a cyberpunk apartment.",
  url: "https://nlemoff.com",
  ogImage: "https://nlemoff.com/og.jpg",
  author: "N. Le Moff",
  links: {
    twitter: "https://twitter.com/nlemoff",
    github: "https://github.com/nlemoff",
  },
}

export const metadata: Metadata = {
  title: {
    default: siteConfig.name,
    template: `%s | ${siteConfig.name}`,
  },
  description: siteConfig.description,
  authors: [
    {
      name: siteConfig.author,
      url: siteConfig.url,
    },
  ],
  creator: siteConfig.author,
  openGraph: {
    type: "website",
    locale: "en_US",
    url: siteConfig.url,
    title: siteConfig.name,
    description: siteConfig.description,
    siteName: siteConfig.name,
    images: [
      {
        url: siteConfig.ogImage,
        width: 1200,
        height: 630,
        alt: siteConfig.name,
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: siteConfig.name,
    description: siteConfig.description,
    images: [siteConfig.ogImage],
    creator: "@nlemoff",
  },
  icons: {
    icon: "/favicon.ico",
  },
  // JSON-LD
  // The JSON-LD schema will be embedded in the page.tsx component instead
  // to have access to dynamic data if needed.
};