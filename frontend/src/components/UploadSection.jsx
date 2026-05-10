import React from 'react';
import { UploadCloud, FileText, File } from 'lucide-react';

export default function UploadSection({
  jdFile,
  setJdFile,
  resumeFiles,
  setResumeFiles,
  onGenerate
}) {
  return (
    <div className="glassmorphism p-8 max-w-3xl mx-auto mt-12 space-y-8 animate-in fade-in zoom-in duration-500">
      <div className="text-center">
        <h2 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-emerald-400">
          Upload Documents
        </h2>
        <p className="text-gray-400 mt-2">Provide the Job Description and Candidate Resumes to begin analysis.</p>
      </div>

      <div className="grid md:grid-cols-2 gap-8">
        {/* JD Upload */}
        <div className="space-y-4">
          <label className="block text-sm font-medium text-gray-300">Job Description (.txt)</label>
          <div className="relative group border-2 border-dashed border-gray-600 rounded-xl p-8 text-center hover:border-blue-400 transition-colors cursor-pointer bg-gray-800/20">
            <input 
              type="file" 
              accept=".txt" 
              onChange={(e) => setJdFile(e.target.files[0])}
              className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
            />
            <FileText className="mx-auto h-8 w-8 text-gray-400 group-hover:text-blue-400 transition-colors" />
            <p className="mt-2 text-sm text-gray-400 group-hover:text-gray-300">
              {jdFile ? jdFile.name : "Drag & drop JD here"}
            </p>
          </div>
        </div>

        {/* Resumes Upload */}
        <div className="space-y-4">
          <label className="block text-sm font-medium text-gray-300">Resumes (.pdf)</label>
          <div className="relative group border-2 border-dashed border-gray-600 rounded-xl p-8 text-center hover:border-emerald-400 transition-colors cursor-pointer bg-gray-800/20">
            <input 
              type="file" 
              multiple
              accept=".pdf" 
              onChange={(e) => setResumeFiles(Array.from(e.target.files))}
              className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
            />
            <File className="mx-auto h-8 w-8 text-gray-400 group-hover:text-emerald-400 transition-colors" />
            <p className="mt-2 text-sm text-gray-400 group-hover:text-gray-300">
              {resumeFiles.length > 0 ? `${resumeFiles.length} files selected` : "Drag & drop Resumes here"}
            </p>
          </div>
        </div>
      </div>

      <div className="flex justify-center pt-4">
        <button
          onClick={onGenerate}
          disabled={!jdFile || resumeFiles.length === 0}
          className="flex items-center px-8 py-3 rounded-full bg-gradient-to-r from-blue-600 to-emerald-600 hover:from-blue-500 hover:to-emerald-500 disabled:opacity-50 disabled:cursor-not-allowed font-semibold text-white shadow-lg hover:shadow-emerald-500/25 transition-all transform hover:-translate-y-0.5 active:translate-y-0"
        >
          <UploadCloud className="mr-2 h-5 w-5" />
          Generate Shortlist
        </button>
      </div>
    </div>
  );
}
