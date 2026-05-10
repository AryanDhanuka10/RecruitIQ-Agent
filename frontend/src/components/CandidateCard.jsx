import React from 'react';
import { CheckCircle, AlertTriangle, HelpCircle, Award } from 'lucide-react';

export default function CandidateCard({ candidate, onOverride }) {
  const isHire = candidate.recommendation === "HIRE";
  const isMaybe = candidate.recommendation === "MAYBE";

  return (
    <div className="glassmorphism p-6 flex flex-col md:flex-row items-start md:items-center justify-between gap-4 animate-in slide-in-from-bottom-4 duration-500">
      <div className="flex-1 space-y-2">
        <div className="flex items-center gap-3">
          <h3 className="text-2xl font-bold text-white">{candidate.candidate_id}</h3>
          <span className={`px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wide flex items-center gap-1 ${isHire ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/50' : isMaybe ? 'bg-amber-500/20 text-amber-400 border border-amber-500/50' : 'bg-red-500/20 text-red-400 border border-red-500/50'}`}>
            {isHire ? <CheckCircle className="w-3 h-3" /> : isMaybe ? <HelpCircle className="w-3 h-3" /> : <AlertTriangle className="w-3 h-3" />}
            {candidate.recommendation}
          </span>
          <span className="text-xs text-gray-400 ml-2">Conf: {(candidate.confidence * 100).toFixed(0)}%</span>
        </div>
        
        <div className="flex items-center gap-2">
          <Award className="w-5 h-5 text-blue-400" />
          <span className="text-lg text-gray-300 font-semibold">{candidate.weighted_total}/10</span>
        </div>
        
        {candidate.red_flags && candidate.red_flags.length > 0 && (
          <div className="mt-4 p-3 bg-red-900/20 border border-red-900/50 rounded-lg">
            <h4 className="text-red-400 text-sm font-semibold mb-1 flex items-center gap-1">
              <AlertTriangle className="w-4 h-4" /> Red Flags
            </h4>
            <ul className="list-disc list-inside text-sm text-gray-300 space-y-1">
              {candidate.red_flags.map((flag, idx) => (
                <li key={idx}>{flag}</li>
              ))}
            </ul>
          </div>
        )}
      </div>

      <div className="flex flex-col gap-2 min-w-[140px]">
        {!isHire && (
          <button
            onClick={() => onOverride(candidate.candidate_id, "HIRE")}
            className="px-4 py-2 bg-emerald-600/20 hover:bg-emerald-600/40 text-emerald-400 border border-emerald-500/30 rounded-lg text-sm font-medium transition-colors"
          >
            Force Hire
          </button>
        )}
        <button
          className="px-4 py-2 bg-gray-800 hover:bg-gray-700 text-gray-300 border border-gray-600 rounded-lg text-sm font-medium transition-colors"
        >
          View Details
        </button>
      </div>
    </div>
  );
}
