import { Card } from "@/components/ui/card"

const technologies = [
  {
    category: "Programming Languages",
    skills: ["Python", "Java", "C/C++", "R", "SQL", "HTML/CSS", "TypeScript", "Go", "MATLAB"],
  },
  {
    category: "Data Science & ML",
    skills: [
      "Pandas",
      "NumPy",
      "TensorFlow",
      "PyTorch",
      "Keras",
      "scikit-learn",
      "Deep Learning",
      "Computer Vision",
      "NLP",
    ],
  },
  {
    category: "Databases & Tools",
    skills: ["MySQL", "PostgreSQL", "MongoDB", "NoSQL", "Docker", "Git", "Jupyter", "Tableau", "Power BI"],
  },
  {
    category: "Web & Software",
    skills: [
      "React.js",
      "Django",
      "Apache Spark",
      "Agile",
      "Software Testing",
      "Data Structures & Algorithms",
      "Figma",
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

