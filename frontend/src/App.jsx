import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Download, Users } from 'lucide-react';
import UploadSection from './components/UploadSection';
import LoadingOverlay from './components/LoadingOverlay';
import CandidateCard from './components/CandidateCard';

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';
const DOMAIN = import.meta.env.VITE_API_BASE_URL ? import.meta.env.VITE_API_BASE_URL.replace('/api/v1', '') : 'http://localhost:8000';

function App() {
  const [jdFile, setJdFile] = useState(null);
  const [resumeFiles, setResumeFiles] = useState([]);
  
  const [jobId, setJobId] = useState(null);
  const [status, setStatus] = useState('idle'); // idle, processing, completed, failed
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  const handleGenerate = async () => {
    if (!jdFile || resumeFiles.length === 0) return;
    
    setStatus('processing');
    setError(null);
    
    const formData = new FormData();
    formData.append('jd_file', jdFile);
    resumeFiles.forEach(file => {
      formData.append('resume_files', file);
    });

    try {
      const res = await axios.post(`${API_BASE}/shortlist`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setJobId(res.data.job_id);
    } catch (err) {
      console.error(err);
      setError('Failed to initiate shortlist job.');
      setStatus('failed');
    }
  };

  useEffect(() => {
    let interval;
    if (jobId && status === 'processing') {
      interval = setInterval(async () => {
        try {
          const res = await axios.get(`${API_BASE}/results/${jobId}`);
          if (res.data.status === 'completed') {
            setResults(res.data);
            setStatus('completed');
            clearInterval(interval);
          } else if (res.data.status === 'failed') {
            setError(res.data.error || 'Job failed on the server.');
            setStatus('failed');
            clearInterval(interval);
          }
        } catch (err) {
          console.error("Polling error:", err);
        }
      }, 2000);
    }
    return () => clearInterval(interval);
  }, [jobId, status]);

  const handleOverride = async (candidateId, recommendation) => {
    try {
      await axios.post(`${API_BASE}/override/${jobId}/${candidateId}`, { recommendation });
      
      // Optimistically update UI
      if (results && results.top_candidates) {
        const updated = results.top_candidates.map(c => 
          c.candidate_id === candidateId ? { ...c, recommendation } : c
        );
        setResults({ ...results, top_candidates: updated });
      }
    } catch (err) {
      console.error("Override failed", err);
      alert("Failed to override candidate status.");
    }
  };

  return (
    <div className="container mx-auto px-4 py-8 max-w-6xl">
      {/* Header */}
      <header className="mb-12 text-center md:text-left flex items-center gap-3">
        <div className="p-3 bg-blue-500/20 rounded-xl border border-blue-500/30 shadow-[0_0_15px_rgba(59,130,246,0.5)]">
          <Users className="w-8 h-8 text-blue-400" />
        </div>
        <div>
          <h1 className="text-3xl font-extrabold tracking-tight">RecruitIQ <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-emerald-400">Agent</span></h1>
          <p className="text-gray-400 text-sm">AI-Powered Shortlisting & Evaluation</p>
        </div>
      </header>

      {/* Main Content Area */}
      <main>
        {status === 'idle' && (
          <UploadSection 
            jdFile={jdFile} 
            setJdFile={setJdFile} 
            resumeFiles={resumeFiles} 
            setResumeFiles={setResumeFiles} 
            onGenerate={handleGenerate} 
          />
        )}

        {status === 'processing' && <LoadingOverlay />}

        {status === 'failed' && (
          <div className="glassmorphism p-8 max-w-2xl mx-auto text-center border-red-500/50">
            <h2 className="text-2xl font-bold text-red-400 mb-2">Analysis Failed</h2>
            <p className="text-gray-300">{error}</p>
            <button 
              onClick={() => setStatus('idle')}
              className="mt-6 px-6 py-2 bg-gray-800 hover:bg-gray-700 rounded-lg transition-colors"
            >
              Try Again
            </button>
          </div>
        )}

        {status === 'completed' && results && (
          <div className="space-y-8 animate-in fade-in duration-700">
            <div className="flex flex-col md:flex-row items-center justify-between gap-4 glassmorphism p-6 bg-blue-900/10">
              <div>
                <h2 className="text-2xl font-bold text-white">Analysis Complete!</h2>
                <p className="text-gray-400 text-sm">Scored {results.top_candidates.length} candidates.</p>
              </div>
              <div className="flex gap-4">
                <a 
                  href={`${DOMAIN}${results.html_url}`} 
                  target="_blank" 
                  rel="noreferrer"
                  className="px-4 py-2 border border-gray-600 hover:bg-gray-800 rounded-lg text-sm font-medium transition-colors"
                >
                  View HTML Report
                </a>
                <a 
                  href={`${DOMAIN}${results.pdf_url}`} 
                  target="_blank" 
                  rel="noreferrer"
                  className="flex items-center gap-2 px-6 py-2 bg-gradient-to-r from-blue-600 to-blue-500 hover:from-blue-500 hover:to-blue-400 rounded-lg text-sm font-bold text-white shadow-lg shadow-blue-500/20 transition-transform transform hover:-translate-y-0.5"
                >
                  <Download className="w-4 h-4" /> Download PDF
                </a>
              </div>
            </div>

            <div className="grid gap-4">
              {results.top_candidates.map((cand, idx) => (
                <CandidateCard 
                  key={idx} 
                  candidate={cand} 
                  onOverride={handleOverride} 
                />
              ))}
            </div>
            
            <div className="text-center mt-12">
              <button 
                onClick={() => {
                  setJdFile(null);
                  setResumeFiles([]);
                  setStatus('idle');
                }}
                className="text-gray-400 hover:text-white underline underline-offset-4 text-sm"
              >
                Start a new job
              </button>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
