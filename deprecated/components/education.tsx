import { Card, CardContent } from "@/components/ui/card"

export default function Education() {
  return (
    <Card className="vaporwave-card p-6 border-vaporwave-pink/30 hover:border-vaporwave-pink/60 transition-all">
      <CardContent className="p-0">
        <div className="flex flex-col md:flex-row justify-between mb-2">
          <h3 className="text-lg font-semibold text-vaporwave-teal">University of California - Berkeley</h3>
          <span className="text-sm text-vaporwave-blue">August 2021 - December 2024</span>
        </div>
        <p className="text-vaporwave-teal">Bachelor&apos;s in Data Science</p>
      </CardContent>
    </Card>
  )
}

