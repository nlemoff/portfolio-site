import Link from 'next/link'

export default function NotFound() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-4 text-center">
      <h2 className="text-4xl font-bold mb-4">Page Not Found</h2>
      <p className="text-xl mb-8">Could not find the requested page</p>
      <Link
        href="/"
        className="px-6 py-3 bg-vaporwave-pink text-vaporwave-dark rounded-lg hover:bg-vaporwave-pink/90 transition-colors"
      >
        Return Home
      </Link>
    </div>
  )
} 
