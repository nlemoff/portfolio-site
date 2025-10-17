'use client';

import React from 'react';
import { DOMLayout } from '@/app/components/dom/DOMLayout';

export function StaticFallback() {
  return (
    <div className="min-h-screen bg-background retro-grid">
      <DOMLayout />
    </div>
  );
}