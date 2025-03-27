import { Card, CardContent } from "@/components/ui/card"
import { Github } from "lucide-react"
import Link from "next/link"

interface ProjectCardProps {
  title: string
  description: string
  link: string
  tags: string[]
}

export default function ProjectCard({ title, description, link, tags }: ProjectCardProps) {
  return (
    <Card className="vaporwave-card border-vaporwave-teal/30 hover:border-vaporwave-teal/60 transition-all">
      <CardContent className="p-4">
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-2">
          <h3 className="font-semibold text-xl text-vaporwave-teal">{title}</h3>
          <Link
            href={link}
            target="_blank"
            className="inline-flex items-center gap-1 text-sm text-vaporwave-blue hover:text-vaporwave-pink transition-colors mt-1 md:mt-0"
          >
            <Github className="h-4 w-4" />
            <span>View Code</span>
          </Link>
        </div>
        <p className="text-sm text-gray-300 mb-4">{description}</p>
        <div className="flex flex-wrap gap-2">
          {tags.map((tag) => (
            <span
              key={tag}
              className="inline-flex items-center rounded-md bg-vaporwave-dark px-2 py-1 text-xs font-medium text-vaporwave-pink ring-1 ring-inset ring-vaporwave-pink/30"
            >
              {tag}
            </span>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}

