import React from 'react';
import { Loader2 } from 'lucide-react';

export default function LoadingOverlay() {
  return (
    <div className="glassmorphism p-12 max-w-lg mx-auto mt-12 text-center space-y-6 animate-in fade-in zoom-in duration-500">
      <div className="relative mx-auto w-24 h-24">
        <div className="absolute inset-0 rounded-full border-t-2 border-b-2 border-blue-500 animate-spin"></div>
        <div className="absolute inset-2 rounded-full border-l-2 border-r-2 border-emerald-500 animate-[spin_1.5s_linear_reverse_infinite]"></div>
        <Loader2 className="absolute inset-0 m-auto w-8 h-8 text-white animate-pulse" />
      </div>
      <div>
        <h3 className="text-2xl font-bold text-white mb-2">Analyzing Candidates</h3>
        <p className="text-gray-400 animate-pulse">Our AI is currently parsing resumes, computing semantic matches, and scoring profiles. This may take a minute...</p>
      </div>
    </div>
  );
}
