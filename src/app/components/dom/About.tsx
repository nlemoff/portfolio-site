'use client';

export function About() {
  return (
    <section 
      id="about" 
      className="py-12 md:py-24 lg:py-32 relative"
    >
      <div className="absolute inset-0 bg-gradient-to-br from-purple-900/10 to-pink-900/10 pointer-events-none" />
      <div className="container px-4 md:px-6 relative z-10">
        <div className="max-w-3xl mx-auto">
          <h2 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl mb-8 text-center gradient-text">
            About Me
          </h2>
          <div className="space-y-4 text-gray-300">
            <p>
              I'm a passionate Full Stack Developer, Data Scientist, and Machine Learning Engineer with a strong foundation in both technical and creative problem-solving. My journey in technology has taken me from building web applications to developing machine learning models that uncover hidden patterns in data.
            </p>
            <p>
              With experience spanning startups to enterprise environments, I bring a unique blend of technical expertise and business acumen to every project. I'm particularly interested in the intersection of artificial intelligence and user experience, creating intelligent applications that are both powerful and intuitive.
            </p>
            <p>
              When I'm not coding or analyzing data, you can find me exploring the latest in tech trends, contributing to open-source projects, or experimenting with new frameworks and methodologies to stay at the cutting edge of our rapidly evolving field.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}