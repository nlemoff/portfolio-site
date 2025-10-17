import React from 'react';

const skills = [
  { name: 'TypeScript', level: '95%' },
  { name: 'React / Next.js', level: '90%' },
  { name: 'Three.js / R3F', level: '85%' },
  { name: 'Node.js', level: '80%' },
  { name: 'Tailwind CSS', level: '95%' },
  { name: 'GraphQL', level: '75%' },
  { name: 'Figma', level: '85%' },
  { name: 'Blender', level: '70%' },
];

export const Skills = () => {
  return (
    <section id="skills" className="min-h-screen container mx-auto py-24 px-4">
      <h2 className="text-3xl font-bold mb-12 text-center">Skills</h2>
      <div className="max-w-4xl mx-auto">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {skills.map((skill) => (
            <div key={skill.name} className="mb-4">
              <div className="flex justify-between mb-1">
                <span className="text-base font-medium text-primary">{skill.name}</span>
                <span className="text-sm font-medium text-muted-foreground">{skill.level}</span>
              </div>
              <div className="w-full bg-secondary rounded-full h-2.5">
                <div className="bg-primary h-2.5 rounded-full" style={{ width: skill.level }}></div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};
