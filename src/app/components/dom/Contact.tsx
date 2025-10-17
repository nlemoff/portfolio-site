'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';

export function Contact() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    message: ''
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitMessage, setSubmitMessage] = useState('');

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    setSubmitMessage('');

    try {
      // In a real implementation, you would call your server action here
      // For now, we'll simulate a successful submission
      await new Promise(resolve => setTimeout(resolve, 1000));
      setSubmitMessage('Thanks for your message! Nick will get back to you soon.');
      setFormData({ name: '', email: '', message: '' });
    } catch (error) {
      setSubmitMessage('There was an error sending your message. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <section 
      id="contact" 
      className="py-12 md:py-24 lg:py-32 relative"
    >
      <div className="absolute inset-0 bg-gradient-to-br from-violet-900/10 to-cyan-900/10 pointer-events-none" />
      <div className="container px-4 md:px-6 relative z-10">
        <div className="max-w-2xl mx-auto">
          <h2 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl mb-12 text-center gradient-text">
            Get in Touch
          </h2>
          
          <div className="vaporwave-card rounded-lg p-6 md:p-8">
            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="space-y-2">
                <Label htmlFor="name" className="text-cyan-300">Name</Label>
                <Input
                  id="name"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  required
                  className="bg-background/50 border-vaporwave-purple/30"
                />
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="email" className="text-cyan-300">Email</Label>
                <Input
                  id="email"
                  name="email"
                  type="email"
                  value={formData.email}
                  onChange={handleChange}
                  required
                  className="bg-background/50 border-vaporwave-purple/30"
                />
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="message" className="text-cyan-300">Message</Label>
                <Textarea
                  id="message"
                  name="message"
                  value={formData.message}
                  onChange={handleChange}
                  required
                  rows={5}
                  className="bg-background/50 border-vaporwave-purple/30"
                />
              </div>
              
              <Button 
                type="submit" 
                disabled={isSubmitting}
                className="w-full bg-gradient-to-r from-cyan-500 to-pink-500 hover:from-cyan-600 hover:to-pink-600"
              >
                {isSubmitting ? 'Sending...' : 'Send Message'}
              </Button>
              
              {submitMessage && (
                <div className={`p-3 rounded-md text-center ${
                  submitMessage.includes('error') 
                    ? 'bg-red-500/20 text-red-300' 
                    : 'bg-green-500/20 text-green-300'
                }`}>
                  {submitMessage}
                </div>
              )}
            </form>
            
            <div className="mt-8 pt-6 border-t border-vaporwave-purple/20">
              <h3 className="text-lg font-semibold mb-4 text-cyan-300">Or reach out directly:</h3>
              <div className="flex flex-wrap gap-4">
                <a 
                  href="mailto:nick@nlemoff.com" 
                  className="flex items-center text-gray-300 hover:text-cyan-300 transition-colors"
                >
                  <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                  </svg>
                  nick@nlemoff.com
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}