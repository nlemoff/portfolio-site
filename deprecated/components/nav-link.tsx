"use client"

import type React from "react"

import type { ReactNode } from "react"

interface NavLinkProps {
  href: string
  children: ReactNode
  className?: string
}

export default function NavLink({ href, children, className = "" }: NavLinkProps) {
  const handleClick = (e: React.MouseEvent<HTMLAnchorElement>) => {
    e.preventDefault()

    // Get the target element
    const targetId = href.replace("#", "")
    const targetElement = document.getElementById(targetId)

    if (targetElement) {
      // Scroll to the element
      targetElement.scrollIntoView({ behavior: "smooth" })

      // Update URL hash without causing a page jump
      window.history.pushState(null, "", href)
    }
  }

  return (
    <a href={href} onClick={handleClick} className={`transition-colors hover:text-vaporwave-pink ${className}`}>
      {children}
    </a>
  )
}

