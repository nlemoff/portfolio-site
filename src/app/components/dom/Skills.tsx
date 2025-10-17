'use client';

export function Skills() {
  const skillCategories = [
    {
      name: "Frontend",
      skills: ["React", "Next.js", "TypeScript", "Tailwind CSS", "Three.js", "WebGL"]
    },
    {
      name: "Backend",
      skills: ["Node.js", "Python", "FastAPI", "Docker", "PostgreSQL", "MongoDB"]
    },
    {
      name: "Data Science & ML",
      skills: ["Python", "TensorFlow", "PyTorch", "Scikit-learn", "Pandas", "NumPy"]
    },
    {
      name: "Cloud & DevOps",
      skills: ["AWS", "GCP", "CI/CD", "Kubernetes", "Terraform", "Serverless"]
    }
  ];

  return (
    <section 
      id="skills" 
      className="py-12 md:py-24 lg:py-32 relative"
    >
      <div className="absolute inset-0 bg-gradient-to-br from-cyan-900/10 to-blue-900/10 pointer-events-none" />
      <div className="container px-4 md:px-6 relative z-10">
        <h2 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl mb-12 text-center gradient-text">
          Skills
        </h2>
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4 max-w-5xl mx-auto">
          {skillCategories.map((category, index) => (
            <div 
              key={index} 
              className="vaporwave-card rounded-lg p-6 transition-all hover:scale-[1.02]"
            >
              <h3 className="text-xl font-bold mb-4 text-cyan-300">{category.name}</h3>
              <ul className="space-y-2">
                {category.skills.map((skill, skillIndex) => (
                  <li key={skillIndex} className="flex items-center">
                    <div className="w-2 h-2 bg-pink-500 rounded-full mr-2"></div>
                    <span className="text-gray-300">{skill}</span>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}