import { Card, CardContent } from "@/components/ui/card"

const experiences = [
  {
    company: "Formula SAE Electric at Berkeley",
    location: "Berkeley, CA, USA",
    position: "Simulations Team Lead",
    period: "May 2024 - January 2025",
    responsibilities: [
      "Built and managed a diverse team of 25+ members across 7 projects, designing team infrastructure to meet the demands of UC Berkeley's largest engineering club.",
      "Oversaw the development of an advanced lap time simulator utilizing a two-track bicycle model and implemented robust Git/GitHub version control practices.",
      "Led critical aerodynamic analysis, engineering a pipeline integrating CAN data and simulations.",
      "Spearheaded migration to Docker containerization for simulation environments, standardizing development dependencies across 25+ team members and achieving a 40% increase in team productivity.",
    ],
  },
  {
    company: "National Institute of Standards and Technology (NIST)",
    location: "Remote",
    position: "Research Intern",
    period: "January 2024 - August 2024",
    responsibilities: [
      "Conducted extensive literature review of state-of-the-art graph edit distance algorithms for NIST's materials science mapping project.",
      "Engineered optimized graph edit distance algorithm using Python and C++ for mapping inorganic materials datasets, achieving 20% faster computation while maintaining accuracy.",
    ],
  },
  {
    company: "Lawrence Berkeley National Laboratory",
    location: "Berkeley, CA, USA",
    position: "Machine Learning Student Assistant",
    period: "September 2023 - August 2024",
    responsibilities: [
      "Developed Faster R-CNN and YOLOv8 computer vision models to detect oil and gas wells in historical maps, achieving 0.98 mAP in under 5 minutes of training.",
      "Conducted academic literature review and in-depth analysis of over 20 different Convolutional Neural Network (CNN) architectures.",
      "Co-authored an abstract submitted to AGU 2024, showcasing the innovative object detection approach.",
    ],
  },
  {
    company: "Mojo Vision",
    location: "Saratoga, CA, USA",
    position: "Data Science and Data Management Intern",
    period: "July 2023 - June 2024",
    responsibilities: [
      "Designed a sophisticated data infrastructure for quantum dot life tests using Python, and MySQL, adopted as the standard data processing pipeline for the entire company.",
      "Built Tableau dashboards for visualizing quantum dot data, speeding up data validation workflow by 40%.",
      "Implemented a program using Python and SQLAlchemy that autonomously monitors and reports issues in company MySQL database.",
    ],
  },
  {
    company: "Formula SAE Electric at Berkeley",
    location: "Berkeley, CA, USA",
    position: "Simulations Engineer - Data Scientist",
    period: "February 2024 - May 2024",
    responsibilities: [
      "Developed a tire model using Tire Testing Consortium data, pandas, and scikit-learn, optimizing parameters for the following year's car.",
      "Created a process for sizing the car's battery pack, integrating sizing constraints, weight considerations, and lap time.",
    ],
  },
]

export default function Experience() {
  return (
    <div className="space-y-6">
      {experiences.map((exp, index) => (
        <Card
          key={index}
          className="vaporwave-card p-6 border-vaporwave-purple/30 hover:border-vaporwave-purple/60 transition-all"
        >
          <CardContent className="p-0">
            <div className="flex flex-col md:flex-row justify-between mb-2">
              <div>
                <h3 className="text-lg font-semibold text-vaporwave-pink">{exp.company}</h3>
                <p className="text-sm text-vaporwave-teal">{exp.location}</p>
              </div>
              <span className="text-sm text-vaporwave-blue">{exp.period}</span>
            </div>
            <p className="font-medium mb-2 text-vaporwave-purple">{exp.position}</p>
            <ul className="list-disc pl-5 space-y-1">
              {exp.responsibilities.map((resp, idx) => (
                <li key={idx} className="text-sm text-gray-300">
                  {resp}
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>
      ))}
    </div>
  )
}

