import { Card, CardContent } from "@/components/ui/card"

const experiences = [
  {
    company: "FullProof",
    location: "San Francisco, CA / Remote",
    position: "Founding Engineer",
    period: "March 2025 - Present",
    responsibilities: [
      "Architected Evie, FullProof's real-time deposition agent, from a demo spread across disconnected services into a unified GCP-backed production system for live transcript processing, document-grounded reasoning, attorney-facing suggestions, and deposition-prep workflows.",
      "Owned FullProof's applied AI research loop: papers, open-source systems, model releases, and hundreds of prototypes across agent memory, real-time agents, hybrid RAG, retrieval/reranking, tool use, long-context workflows, and eval methodology.",
      "Productionized research ideas into a Python/FastAPI agent service with streaming endpoints for live transcript lines, chat/RAG, document extraction, strategy generation, outline generation, tracker summaries, persistent case memory, and final-round deposition workflows.",
      "Designed real-time agent orchestration that records transcript state, routes each line through research / quick-check / suppression paths, and returns citation-backed tactical suggestions with timing, route, usage, and tool-call traces.",
      "Built document-grounded retrieval over case files with Vertex AI Search / Discovery Engine, case-scoped filtering, dynamic exhibit mapping, caching, concurrency controls, source-identity observability, and fail-closed behavior for unsupported evidence.",
      "Created replay/evaluation infrastructure for AI reliability: transcript replays, browser-projected agent output, service health snapshots, event logs, line-level lifecycle traces, scoring, and regression coverage.",
      "Shipped across React/Vite, TypeScript, Node/Express, Python, FastAPI, PostgreSQL, Prisma, Redis, Socket.IO, BullMQ, Vertex AI Search, and Google Cloud.",
    ],
  },
  {
    company: "Formula SAE Electric at Berkeley",
    location: "Berkeley, CA",
    position: "Simulations Team Lead",
    period: "May 2024 - January 2025",
    responsibilities: [
      "Led a 25+ person simulations team across 7 vehicle-modeling projects for UC Berkeley's Formula SAE electric racecar team.",
      "Developed a lap-time simulator using a two-track bicycle model and introduced Git/GitHub workflows for a larger engineering contributor base.",
      "Built aerodynamic and vehicle-analysis pipelines that connected CAN data with simulation outputs.",
      "Containerized simulation environments with Docker so contributors could work from a consistent setup.",
    ],
  },
  {
    company: "National Institute of Standards and Technology (NIST)",
    location: "Remote",
    position: "Research Intern",
    period: "January 2024 - August 2024",
    responsibilities: [
      "Implemented optimized graph edit distance code in Python and C++ for inorganic materials datasets after reviewing core algorithmic approaches.",
      "Contributed to a long-running materials-science project embedding 167,500 ICSD entries into a structural-similarity space to study experimental discovery, computed materials proposals, and synthesizability priors.",
      "Reviewed and merged multiple PRs to make the latest research code reproducible and runnable on other machines ahead of the group's Nature submission.",
    ],
  },
  {
    company: "Lawrence Berkeley National Laboratory",
    location: "Berkeley, CA",
    position: "Machine Learning Student Assistant",
    period: "September 2023 - August 2024",
    responsibilities: [
      "Developed Faster R-CNN and YOLOv8 models to detect oil and gas wells in historical maps, reaching 0.98 mAP in under 5 minutes of training.",
      "Reviewed and compared 20+ CNN architectures for historical-map object detection.",
      "Co-authored an abstract submitted to AGU 2024 on the object-detection approach.",
    ],
  },
  {
    company: "Mojo Vision",
    location: "Saratoga, CA",
    position: "Data Science and Data Management Intern",
    period: "July 2023 - June 2024",
    responsibilities: [
      "Designed Python/MySQL data pipelines for quantum dot life tests that became the company's standard processing workflow.",
      "Built Tableau dashboards for quantum dot validation data and reduced manual review work.",
      "Wrote Python and SQLAlchemy monitoring code to detect and report issues in company MySQL databases.",
    ],
  },
  {
    company: "Formula SAE Electric at Berkeley",
    location: "Berkeley, CA",
    position: "Simulations Engineer / Data Scientist",
    period: "February 2024 - May 2024",
    responsibilities: [
      "Developed a tire model using Tire Testing Consortium data, pandas, and scikit-learn to guide next-year vehicle parameters.",
      "Created a battery-pack sizing process that balanced sizing constraints, weight, and lap-time impact.",
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
                <li key={idx} className="text-sm text-slate-700 dark:text-gray-300">
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
