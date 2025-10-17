"use client"

import { useState, useEffect, useRef } from "react"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { useForm } from "react-hook-form"
import emailjs from '@emailjs/browser'

type FormData = {
  name: string
  email: string
  message: string
}

const EMAILJS_PUBLIC_KEY = "gqFPXLtgEw6xvtyn2"
const EMAILJS_SERVICE_ID = "default_service"
const EMAILJS_TEMPLATE_ID = "template_br06a7y"

export default function ContactForm() {
  const [pending, setPending] = useState(false)
  const [message, setMessage] = useState("")
  const formRef = useRef<HTMLFormElement>(null)
  const { register, handleSubmit, reset, formState: { isSubmitting } } = useForm<FormData>()

  useEffect(() => {
    emailjs.init(EMAILJS_PUBLIC_KEY)
  }, [])

  const onSubmit = async (data: FormData) => {
    if (!formRef.current) return
    
    setPending(true)
    try {
      await emailjs.sendForm(
        EMAILJS_SERVICE_ID,
        EMAILJS_TEMPLATE_ID,
        formRef.current,
        EMAILJS_PUBLIC_KEY
      )
      setMessage("Message sent successfully!")
      reset() // Clear the form
    } catch (error) {
      console.error('Error sending email:', error)
      setMessage("Failed to send message. Please try again.")
    } finally {
      setPending(false)
    }
  }

  return (
    <Card className="vaporwave-card p-6 border-vaporwave-purple/30 hover:border-vaporwave-purple/60 transition-all">
      <form ref={formRef} onSubmit={handleSubmit(onSubmit)} className="space-y-4">
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

