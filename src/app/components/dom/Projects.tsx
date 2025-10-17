'use client';

export function Projects() {
  const projects = [
    {
      title: "Personal Portfolio Website",
      description: "A modern, responsive portfolio website built with Next.js, TypeScript, and Tailwind CSS. Features a custom vaporwave theme, dark mode support, and EmailJS integration for the contact form.",
      tags: ["Next.js", "TypeScript", "Tailwind CSS", "shadcn/ui"],
      link: "https://github.com/nlemoff/portfolio-site"
    },
    {
      title: "Audio Transcriber",
      description: "A macOS application that captures both microphone and system audio while providing real-time transcription capabilities using Fast API and Docker.",
      tags: ["SwiftUI", "Docker", "Fast API", "GCP"],
      link: "https://github.com/nlemoff/audio-transcriber"
    },
    {
      title: "Machine Learning Visualizer",
      description: "A React-based web application for visualizing machine learning model predictions with interactive data visualization using Chart.js.",
      tags: ["React", "TypeScript", "Chart.js", "Tailwind CSS"],
      link: "https://github.com/nlemoff/ml-visualizer"
    },
    {
      title: "POV Classification in Sentences",
      description: "A BERT-based deep learning model for multi-class Point of View (POV) classification in literary texts, achieving 65% accuracy.",
      tags: ["BERT", "NLP", "Deep Learning", "Python"],
      link: "https://github.com/nlemoff/pov-classification"
    },
    {
      title: "Titanic Survival Prediction",
      description: "Led a UC Berkeley-hosted Kaggle competition team, focusing on predicting Titanic passenger survival with 80% accuracy.",
      tags: ["Kaggle", "Machine Learning", "Python", "Data Science"],
      link: "https://github.com/nlemoff/titanic-prediction"
    },
    {
      title: "Earnings Predictions for College Graduates",
      description: "Analyzed the interplay between college majors, gender, and earnings, to shed light on the gender wage gap's influence in early career stages.",
      tags: ["Data Analysis", "Prediction Models", "Python"],
      link: "https://github.com/nlemoff/earnings-prediction"
    }
  ];

  return (
    <section 
      id="projects" 
      className="py-12 md:py-24 lg:py-32 relative"
    >
      <div className="absolute inset-0 bg-gradient-to-br from-purple-900/10 to-pink-900/10 pointer-events-none" />
      <div className="container px-4 md:px-6 relative z-10">
        <h2 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl mb-12 text-center gradient-text">
          Projects
        </h2>
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3 max-w-5xl mx-auto">
          {projects.map((project, index) => (
            <div 
              key={index} 
              className="vaporwave-card rounded-lg p-6 transition-all hover:scale-[1.02]"
            >
              <h3 className="text-xl font-bold mb-2 text-cyan-300">{project.title}</h3>
              <p className="text-gray-300 mb-4">{project.description}</p>
              <div className="flex flex-wrap gap-2 mb-4">
                {project.tags.map((tag, tagIndex) => (
                  <span 
                    key={tagIndex} 
                    className="px-2 py-1 text-xs rounded-full bg-pink-500/20 text-pink-300"
                  >
                    {tag}
                  </span>
                ))}
              </div>
              <a 
                href={project.link} 
                target="_blank" 
                rel="noopener noreferrer"
                className="inline-flex items-center text-cyan-400 hover:text-cyan-300 transition-colors"
              >
                View Project
                <svg 
                  className="ml-1 w-4 h-4" 
                  fill="none" 
                  stroke="currentColor" 
                  viewBox="0 0 24 24"
                >
                  <path 
                    strokeLinecap="round" 
                    strokeLinejoin="round" 
                    strokeWidth={2} 
                    d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" 
                  />
                </svg>
              </a>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}