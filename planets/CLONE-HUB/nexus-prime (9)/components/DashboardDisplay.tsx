
import React from 'react';
import { motion } from 'framer-motion';
import { Shield, Activity, Terminal } from 'lucide-react';
import type { NexusReport } from '../types.ts';

interface DashboardDisplayProps {
  data: NexusReport;
  color: string;
}

export const DashboardDisplay: React.FC<DashboardDisplayProps> = ({ data, color }) => {
  return (
    <motion.div 
      initial={{ opacity: 0, scale: 0.9, y: 50 }}
      animate={{ opacity: 1, scale: 1, y: 0 }}
      transition={{ duration: 0.5, type: 'spring' }}
      className="relative w-full max-w-3xl bg-black/60 backdrop-blur-2xl border-t border-b border-white/10 p-8 rounded-3xl overflow-hidden shadow-2xl"
      style={{ borderColor: color }}
    >
      <div 
        className="absolute top-0 left-1/2 -translate-x-1/2 w-2/3 h-1 opacity-50" 
        style={{ background: `radial-gradient(ellipse at center, ${color} 0%, transparent 80%)` }} 
      />

      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between mb-6">
        <h2 className="text-2xl md:text-3xl font-bold text-white tracking-widest uppercase flex items-center gap-3 mb-2 sm:mb-0">
          <Shield style={{ color }} />
          {data.title}
        </h2>
        <span className="text-xs font-mono text-gray-500 border border-gray-700 px-2 py-1 rounded">SECURE</span>
      </div>

      <div className="mb-6 p-4 bg-white/5 rounded-xl border-l-2" style={{ borderLeftColor: color }}>
        <h3 className="text-gray-400 text-xs uppercase tracking-wider mb-2 flex items-center gap-2">
           <Activity size={14} /> Executive Summary
        </h3>
        <p className="text-base md:text-lg text-gray-100 font-light leading-relaxed">
          {data.executive_summary}
        </p>
      </div>

      <div className="bg-black/80 rounded-lg p-4 md:p-5 font-mono text-sm text-gray-300 border border-white/5 shadow-inner max-h-60 overflow-y-auto">
        <div className="flex items-center gap-2 mb-3 text-gray-500 border-b border-gray-800 pb-2">
            <Terminal size={14} /> 
            <span>/var/log/analysis_core</span>
        </div>
        <pre className="whitespace-pre-wrap text-xs md:text-sm leading-loose">{data.deep_analysis_markdown}</pre>
      </div>
    </motion.div>
  );
};