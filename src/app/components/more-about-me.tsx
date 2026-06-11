const facts = [
  "I'm an Eagle Scout.",
  "I'm a lifelong drummer.",
  "I played professional Apex Legends from 2021 to 2022.",
  "I played on the D1 UC Berkeley CS:GO team my freshman year.",
  "I grew up in West Virginia.",
  "I'm a lifelong Pittsburgh Steelers fan.",
]

export default function MoreAboutMe() {
  return (
    <ul className="mx-auto max-w-3xl list-disc space-y-3 pl-6 text-base leading-7 text-slate-700 dark:text-gray-300 md:text-lg">
      {facts.map((fact) => (
        <li key={fact}>{fact}</li>
      ))}
    </ul>
  )
}
