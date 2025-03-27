"use client"

import { useState } from "react"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { useForm } from "react-hook-form"

type FormData = {
  name: string
  email: string
  message: string
}

export default function ContactForm() {
  const [pending, setPending] = useState(false)
  const [message, setMessage] = useState("")
  const { register, handleSubmit, formState: { isSubmitting } } = useForm<FormData>()

  const onSubmit = async (data: FormData) => {
    setPending(true)
    try {
      const formData = new FormData()
      formData.append("name", data.name)
      formData.append("email", data.email)
      formData.append("message", data.message)
      setMessage("Message sent successfully!")
    } catch {
      setMessage("Failed to send message. Please try again.")
    } finally {
      setPending(false)
    }
  }

  return (
    <Card className="vaporwave-card p-6 border-vaporwave-purple/30 hover:border-vaporwave-purple/60 transition-all">
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <div>
          <label htmlFor="name" className="block text-sm font-medium mb-2 text-vaporwave-teal">
            Name
          </label>
          <Input
            id="name"
            type="text"
            placeholder="Your name"
            required
            className="bg-vaporwave-dark/50 border-vaporwave-pink/30 focus:border-vaporwave-pink focus:ring-vaporwave-pink/30"
            {...register("name")}
          />
        </div>
        <div>
          <label htmlFor="email" className="block text-sm font-medium mb-2 text-vaporwave-teal">
            Email
          </label>
          <Input
            id="email"
            type="email"
            placeholder="Your email"
            required
            className="bg-vaporwave-dark/50 border-vaporwave-pink/30 focus:border-vaporwave-pink focus:ring-vaporwave-pink/30"
            {...register("email")}
          />
        </div>
        <div>
          <label htmlFor="message" className="block text-sm font-medium mb-2 text-vaporwave-teal">
            Message
          </label>
          <Textarea
            id="message"
            placeholder="Your message"
            required
            className="bg-vaporwave-dark/50 border-vaporwave-pink/30 focus:border-vaporwave-pink focus:ring-vaporwave-pink/30"
            {...register("message")}
          />
        </div>
        <Button
          type="submit"
          className="w-full bg-vaporwave-gradient hover:opacity-90 text-white border-none"
          disabled={pending || isSubmitting}
        >
          {pending ? "Sending..." : "Send Message"}
        </Button>
        {message && (
          <p className={`text-sm ${message.includes("success") ? "text-green-500" : "text-red-500"}`}>
            {message}
          </p>
        )}
      </form>
    </Card>
  )
}

