import { Card } from "@/components/ui/card"

const technologies = [
  {
    category: "Languages",
    skills: ["Python", "TypeScript", "JavaScript", "SQL", "C/C++", "Java", "Go", "R"],
  },
  {
    category: "AI / ML / research",
    skills: [
      "LLM agents",
      "Real-time agents",
      "Agent memory",
      "Hybrid RAG",
      "Retrieval/reranking",
      "Vertex AI Search",
      "Eval harnesses",
      "Replay testing",
      "Prompt/system design",
      "PyTorch",
      "TensorFlow",
      "scikit-learn",
      "Computer vision",
      "NLP",
      "Literature review",
      "Rapid prototyping",
    ],
  },
  {
    category: "Product engineering",
    skills: [
      "React",
      "Vite",
      "Next.js",
      "Node.js",
      "Express",
      "FastAPI",
      "PostgreSQL",
      "Redis",
      "Socket.IO",
      "BullMQ",
      "Prisma",
      "Tailwind CSS",
    ],
  },
  {
    category: "Infrastructure / workflow",
    skills: [
      "Google Cloud",
      "Docker",
      "Git/GitHub",
      "CI/CD",
      "Playwright",
      "Jupyter",
      "Tableau",
      "Observability",
    ],
  },
]

export default function TechStack() {
  return (
    <div className="grid gap-6 md:grid-cols-2">
      {technologies.map((tech) => (
        <Card
          key={tech.category}
          className="vaporwave-card p-6 border-vaporwave-blue/30 hover:border-vaporwave-blue/60 transition-all"
        >
          <h3 className="text-lg font-semibold mb-4 text-vaporwave-teal">{tech.category}</h3>
          <div className="flex flex-wrap gap-2">
            {tech.skills.map((skill) => (
              <span
                key={skill}
                className="inline-flex items-center rounded-md bg-vaporwave-dark px-2 py-1 text-sm font-medium text-vaporwave-pink ring-1 ring-inset ring-vaporwave-pink/30 hover:ring-vaporwave-pink/60 transition-colors"
              >
                {skill}
              </span>
            ))}
          </div>
        </Card>
      ))}
    </div>
  )
}
