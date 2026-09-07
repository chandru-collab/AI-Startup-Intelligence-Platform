"use client";

import { useState, useEffect } from "react";
import { startResearch } from "@/lib/api";

export default function SearchPage() {
  const [searchQuery, setSearchQuery] = useState("");
  const [isSearching, setIsSearching] = useState(false);
  const [activeAgent, setActiveAgent] = useState<string | null>(null);
  const [agentMessage, setAgentMessage] = useState<string>("");
  const [result, setResult] = useState<any>(null);
  const [partialResults, setPartialResults] = useState<Record<string, string>>({});

  useEffect(() => {
    // Connect to WebSocket
    const ws = new WebSocket('ws://localhost:8000/ws/alerts');
    
    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.type === 'agent_start') {
          setActiveAgent(data.agent);
          setAgentMessage(data.message);
        } else if (data.type === 'agent_partial_result') {
          setPartialResults((prev) => ({ ...prev, [data.agent]: data.data }));
        } else if (data.type === 'analysis_complete') {
          setResult(data.data);
          setIsSearching(false);
          setActiveAgent(null);
        }
      } catch (e) {
        console.error("Failed to parse websocket message", e);
      }
    };

    return () => {
      ws.close();
    };
  }, []);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if(searchQuery) {
        setIsSearching(true);
        setResult(null);
        setPartialResults({});
        setActiveAgent('research'); // Optimistic start
        setAgentMessage("Initializing agents...");
        try {
            await startResearch(searchQuery);
            // We wait for the websocket to send 'analysis_complete'
        } catch (error) {
            console.error(error);
            setIsSearching(false);
            setActiveAgent(null);
        }
    }
  };

  const getAgentStyle = (agentName: string) => {
    if (activeAgent === agentName) {
      return "ring-2 ring-indigo-500 bg-indigo-50/50 dark:bg-indigo-900/30 animate-pulse scale-[1.02] transition-all shadow-lg border-indigo-200 dark:border-indigo-800";
    }
    return "border border-gray-100 dark:border-white/5 bg-white/40 dark:bg-black/20 backdrop-blur-md opacity-70 hover:opacity-100 transition-opacity";
  };

  return (
    <div className="flex flex-col gap-8 max-w-5xl mx-auto pb-16 pt-4">
      
      {/* Header Search Section - Premium Glassmorphism */}
      <div className="relative overflow-hidden bg-white/70 dark:bg-gray-900/70 backdrop-blur-xl p-10 rounded-2xl shadow-xl border border-white/40 dark:border-white/10">
        <div className="absolute top-0 right-0 -mr-16 -mt-16 w-64 h-64 rounded-full bg-gradient-to-br from-blue-400 to-indigo-600 opacity-20 blur-3xl mix-blend-multiply"></div>
        <div className="absolute bottom-0 left-0 -ml-16 -mb-16 w-64 h-64 rounded-full bg-gradient-to-tr from-purple-400 to-pink-500 opacity-20 blur-3xl mix-blend-multiply"></div>
        
        <div className="relative z-10">
          <h2 className="text-4xl font-extrabold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-gray-900 to-gray-600 dark:from-white dark:to-gray-300 mb-3">
            Deep Intelligence Engine
          </h2>
          <p className="text-lg text-gray-600 dark:text-gray-400 mb-8 font-medium">
            Deploy a swarm of specialized AI agents to uncover deep insights on any global startup.
          </p>
          
          <form onSubmit={handleSearch} className="flex gap-4">
            <div className="relative flex-1">
              <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                <span className="text-xl">🚀</span>
              </div>
              <input 
                type="text" 
                placeholder="e.g. OpenAI, SpaceX, Anthropic..." 
                className="w-full pl-12 pr-4 py-4 rounded-xl bg-white/80 dark:bg-black/40 border border-gray-200 dark:border-white/10 focus:outline-none focus:ring-4 focus:ring-indigo-500/30 text-lg shadow-inner backdrop-blur-sm transition-all"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                disabled={isSearching}
              />
            </div>
            <button 
              type="submit" 
              disabled={isSearching || !searchQuery}
              className="bg-gradient-to-r from-indigo-600 to-blue-600 hover:from-indigo-700 hover:to-blue-700 disabled:from-indigo-400 disabled:to-blue-400 text-white px-10 py-4 rounded-xl transition-all shadow-lg hover:shadow-indigo-500/30 text-lg font-bold flex items-center gap-2"
            >
              {isSearching ? (
                <>
                  <svg className="animate-spin -ml-1 mr-2 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Deploying Swarm...
                </>
              ) : "Initialize Swarm"}
            </button>
          </form>
        </div>
      </div>

      {/* Active Pipeline Grid */}
      {!result && (
        <div className="bg-white/50 dark:bg-gray-900/50 backdrop-blur-md p-8 rounded-2xl shadow-sm border border-gray-200/50 dark:border-white/5">
          <div className="flex justify-between items-center mb-8">
            <h3 className="text-xl font-bold tracking-tight text-gray-800 dark:text-gray-200">Swarm Telemetry</h3>
            {isSearching ? (
              <div className="flex items-center gap-3">
                <span className="relative flex h-3 w-3">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-indigo-400 opacity-75"></span>
                  <span className="relative inline-flex rounded-full h-3 w-3 bg-indigo-500"></span>
                </span>
                <span className="text-indigo-600 dark:text-indigo-400 font-semibold tracking-wide uppercase text-sm">
                  {agentMessage || "Synchronizing agents..."}
                </span>
              </div>
            ) : (
              <span className="text-gray-400 text-sm font-medium uppercase tracking-widest">Standby</span>
            )}
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
            <div className={`flex flex-col gap-2 p-5 rounded-xl transition-all ${getAgentStyle('research')}`}>
              <div className="flex items-center gap-3">
                <div className="text-3xl drop-shadow-sm">🔍</div>
                <div className="flex-1 flex justify-between items-center">
                  <h4 className="font-bold text-gray-900 dark:text-white">Research Agent</h4>
                  {partialResults['research'] && <span className="bg-emerald-100 text-emerald-700 dark:bg-emerald-900/50 dark:text-emerald-300 text-[10px] font-bold px-2 py-0.5 rounded-full uppercase">Complete</span>}
                </div>
              </div>
              <p className="text-xs text-gray-500 dark:text-gray-400 leading-relaxed">
                {partialResults['research'] ? (
                  <span className="text-gray-700 dark:text-gray-300 font-medium line-clamp-3">{partialResults['research']}</span>
                ) : "Finds startup websites, products, founders."}
              </p>
            </div>
            
            <div className={`flex flex-col gap-2 p-5 rounded-xl transition-all ${getAgentStyle('funding')}`}>
              <div className="flex items-center gap-3">
                <div className="text-3xl drop-shadow-sm">💰</div>
                <div className="flex-1 flex justify-between items-center">
                  <h4 className="font-bold text-gray-900 dark:text-white">Funding Agent</h4>
                  {partialResults['funding'] && <span className="bg-emerald-100 text-emerald-700 dark:bg-emerald-900/50 dark:text-emerald-300 text-[10px] font-bold px-2 py-0.5 rounded-full uppercase">Complete</span>}
                </div>
              </div>
              <p className="text-xs text-gray-500 dark:text-gray-400 leading-relaxed">
                {partialResults['funding'] ? (
                  <span className="text-gray-700 dark:text-gray-300 font-medium line-clamp-3">{partialResults['funding']}</span>
                ) : "Collects funding rounds and investors."}
              </p>
            </div>
            
            <div className={`flex flex-col gap-2 p-5 rounded-xl transition-all ${getAgentStyle('hiring')}`}>
              <div className="flex items-center gap-3">
                <div className="text-3xl drop-shadow-sm">👥</div>
                <div className="flex-1 flex justify-between items-center">
                  <h4 className="font-bold text-gray-900 dark:text-white">Hiring Agent</h4>
                  {partialResults['hiring'] && <span className="bg-emerald-100 text-emerald-700 dark:bg-emerald-900/50 dark:text-emerald-300 text-[10px] font-bold px-2 py-0.5 rounded-full uppercase">Complete</span>}
                </div>
              </div>
              <p className="text-xs text-gray-500 dark:text-gray-400 leading-relaxed">
                {partialResults['hiring'] ? (
                  <span className="text-gray-700 dark:text-gray-300 font-medium line-clamp-3">{partialResults['hiring']}</span>
                ) : "Tracks job postings and team growth."}
              </p>
            </div>
            
            <div className={`flex flex-col gap-2 p-5 rounded-xl transition-all ${getAgentStyle('news')}`}>
              <div className="flex items-center gap-3">
                <div className="text-3xl drop-shadow-sm">📰</div>
                <div className="flex-1 flex justify-between items-center">
                  <h4 className="font-bold text-gray-900 dark:text-white">News Agent</h4>
                  {partialResults['news'] && <span className="bg-emerald-100 text-emerald-700 dark:bg-emerald-900/50 dark:text-emerald-300 text-[10px] font-bold px-2 py-0.5 rounded-full uppercase">Complete</span>}
                </div>
              </div>
              <p className="text-xs text-gray-500 dark:text-gray-400 leading-relaxed">
                {partialResults['news'] ? (
                  <span className="text-gray-700 dark:text-gray-300 font-medium line-clamp-3">{partialResults['news']}</span>
                ) : "Watches press releases and announcements."}
              </p>
            </div>
            
            <div className={`flex flex-col gap-2 p-5 rounded-xl transition-all ${getAgentStyle('social_media')}`}>
              <div className="flex items-center gap-3">
                <div className="text-3xl drop-shadow-sm">📱</div>
                <div className="flex-1 flex justify-between items-center">
                  <h4 className="font-bold text-gray-900 dark:text-white">Social Media Agent</h4>
                  {partialResults['social_media'] && <span className="bg-emerald-100 text-emerald-700 dark:bg-emerald-900/50 dark:text-emerald-300 text-[10px] font-bold px-2 py-0.5 rounded-full uppercase">Complete</span>}
                </div>
              </div>
              <p className="text-xs text-gray-500 dark:text-gray-400 leading-relaxed">
                {partialResults['social_media'] ? (
                  <span className="text-gray-700 dark:text-gray-300 font-medium line-clamp-3">{partialResults['social_media']}</span>
                ) : "Monitors LinkedIn, X, blogs."}
              </p>
            </div>
            
            <div className={`flex flex-col gap-2 p-5 rounded-xl transition-all ${getAgentStyle('verification')}`}>
              <div className="flex items-center gap-3">
                <div className="text-3xl drop-shadow-sm">✅</div>
                <div className="flex-1 flex justify-between items-center">
                  <h4 className="font-bold text-gray-900 dark:text-white">Verification Agent</h4>
                  {partialResults['verification'] && <span className="bg-emerald-100 text-emerald-700 dark:bg-emerald-900/50 dark:text-emerald-300 text-[10px] font-bold px-2 py-0.5 rounded-full uppercase">Complete</span>}
                </div>
              </div>
              <p className="text-xs text-gray-500 dark:text-gray-400 leading-relaxed">
                {partialResults['verification'] ? (
                  <span className="text-gray-700 dark:text-gray-300 font-medium line-clamp-3">{partialResults['verification']}</span>
                ) : "Cross-checks facts across sources."}
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Structured Final Results */}
      {result && (
        <div className="bg-white dark:bg-gray-900 rounded-2xl shadow-2xl border border-gray-200 dark:border-gray-800 overflow-hidden animate-in fade-in slide-in-from-bottom-8 duration-700">
          
          {/* Results Header */}
          <div className="bg-gradient-to-r from-gray-50 to-white dark:from-gray-900 dark:to-gray-800 p-8 border-b border-gray-200 dark:border-gray-700">
            <div className="flex flex-col md:flex-row md:items-end justify-between gap-4">
              <div>
                <div className="flex items-center gap-3 mb-2">
                  <span className="bg-green-100 text-green-700 text-xs font-bold px-3 py-1 rounded-full uppercase tracking-widest border border-green-200 dark:bg-green-900/30 dark:border-green-800">
                    Intelligence Gathered
                  </span>
                </div>
                <h3 className="text-3xl font-black text-gray-900 dark:text-white">
                  Target Profile: <span className="text-indigo-600 dark:text-indigo-400">{result.name}</span>
                </h3>
              </div>
              
              {result.pdf_available && (
                <a 
                  href={`http://localhost:8000/api/v1/startups/${result.name}/report/pdf`} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="bg-indigo-600 hover:bg-indigo-700 text-white px-6 py-3 rounded-lg font-bold transition-all shadow-lg hover:shadow-indigo-500/40 flex items-center gap-2 transform hover:-translate-y-0.5"
                >
                  <span className="text-xl">📄</span> Export Full PDF
                </a>
              )}
            </div>
          </div>
          
          {/* Detailed Agent Breakdown */}
          <div className="p-8 space-y-6">
            <h4 className="text-xl font-bold tracking-tight text-gray-800 dark:text-gray-200 mb-6">Agent Findings Breakdown</h4>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Research */}
              <div className="bg-gray-50/50 dark:bg-gray-800/50 p-6 rounded-xl border border-gray-100 dark:border-gray-700 hover:border-indigo-300 dark:hover:border-indigo-700 transition-colors">
                <div className="flex items-center gap-3 mb-4">
                  <div className="text-2xl bg-white dark:bg-gray-700 p-2 rounded-lg shadow-sm">🔍</div>
                  <h5 className="font-bold text-lg">Research Summary</h5>
                </div>
                <p className="text-gray-700 dark:text-gray-300 text-sm leading-relaxed whitespace-pre-wrap">
                  {result.agent_results?.research || "No data."}
                </p>
              </div>

              {/* Funding */}
              <div className="bg-gray-50/50 dark:bg-gray-800/50 p-6 rounded-xl border border-gray-100 dark:border-gray-700 hover:border-emerald-300 dark:hover:border-emerald-700 transition-colors">
                <div className="flex items-center gap-3 mb-4">
                  <div className="text-2xl bg-white dark:bg-gray-700 p-2 rounded-lg shadow-sm">💰</div>
                  <h5 className="font-bold text-lg">Funding & Runway</h5>
                </div>
                <p className="text-gray-700 dark:text-gray-300 text-sm leading-relaxed whitespace-pre-wrap">
                  {result.agent_results?.funding || "No data."}
                </p>
              </div>

              {/* Hiring */}
              <div className="bg-gray-50/50 dark:bg-gray-800/50 p-6 rounded-xl border border-gray-100 dark:border-gray-700 hover:border-blue-300 dark:hover:border-blue-700 transition-colors">
                <div className="flex items-center gap-3 mb-4">
                  <div className="text-2xl bg-white dark:bg-gray-700 p-2 rounded-lg shadow-sm">👥</div>
                  <h5 className="font-bold text-lg">Hiring & Team</h5>
                </div>
                <p className="text-gray-700 dark:text-gray-300 text-sm leading-relaxed whitespace-pre-wrap">
                  {result.agent_results?.hiring || "No data."}
                </p>
              </div>

              {/* News */}
              <div className="bg-gray-50/50 dark:bg-gray-800/50 p-6 rounded-xl border border-gray-100 dark:border-gray-700 hover:border-purple-300 dark:hover:border-purple-700 transition-colors">
                <div className="flex items-center gap-3 mb-4">
                  <div className="text-2xl bg-white dark:bg-gray-700 p-2 rounded-lg shadow-sm">📰</div>
                  <h5 className="font-bold text-lg">Recent News</h5>
                </div>
                <p className="text-gray-700 dark:text-gray-300 text-sm leading-relaxed whitespace-pre-wrap">
                  {result.agent_results?.news || "No data."}
                </p>
              </div>

              {/* Social */}
              <div className="bg-gray-50/50 dark:bg-gray-800/50 p-6 rounded-xl border border-gray-100 dark:border-gray-700 hover:border-pink-300 dark:hover:border-pink-700 transition-colors">
                <div className="flex items-center gap-3 mb-4">
                  <div className="text-2xl bg-white dark:bg-gray-700 p-2 rounded-lg shadow-sm">📱</div>
                  <h5 className="font-bold text-lg">Social Sentiment</h5>
                </div>
                <p className="text-gray-700 dark:text-gray-300 text-sm leading-relaxed whitespace-pre-wrap">
                  {result.agent_results?.social || "No data."}
                </p>
              </div>

              {/* Verification */}
              <div className="bg-gray-50/50 dark:bg-gray-800/50 p-6 rounded-xl border border-gray-100 dark:border-gray-700 hover:border-amber-300 dark:hover:border-amber-700 transition-colors">
                <div className="flex items-center gap-3 mb-4">
                  <div className="text-2xl bg-white dark:bg-gray-700 p-2 rounded-lg shadow-sm">✅</div>
                  <h5 className="font-bold text-lg">Verification Analysis</h5>
                </div>
                <p className="text-gray-700 dark:text-gray-300 text-sm leading-relaxed whitespace-pre-wrap">
                  {result.agent_results?.verification || "No data."}
                </p>
              </div>
            </div>

            {/* Strategic Synthesis */}
            <div className="mt-8 bg-gradient-to-br from-indigo-900 to-black p-8 rounded-2xl shadow-inner border border-indigo-500/30">
              <h4 className="text-2xl font-black text-white mb-6 flex items-center gap-3">
                <span className="text-3xl">🎯</span> Strategic Synthesis
              </h4>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div>
                  <span className="block text-indigo-300 text-sm font-bold uppercase tracking-widest mb-2">Growth Trajectory</span>
                  <p className="text-white text-xl font-medium leading-relaxed">
                    {result.status}
                  </p>
                </div>
                <div>
                  <span className="block text-indigo-300 text-sm font-bold uppercase tracking-widest mb-2">Investment Thesis</span>
                  <p className="text-white text-xl font-medium leading-relaxed">
                    {result.agent_results?.report || "No thesis available."}
                  </p>
                </div>
              </div>
            </div>
          </div>
          
          {/* Footer Action */}
          <div className="bg-gray-50 dark:bg-gray-900 p-6 border-t border-gray-200 dark:border-gray-800 flex justify-center">
             <button 
                onClick={() => setResult(null)} 
                className="text-gray-600 hover:text-gray-900 dark:text-gray-400 dark:hover:text-white font-bold flex items-center gap-2 hover:bg-gray-200 dark:hover:bg-gray-800 px-6 py-3 rounded-xl transition-all"
             >
                <span className="text-xl">↺</span> Execute New Sweep
             </button>
          </div>
        </div>
      )}
    </div>
  );
}
