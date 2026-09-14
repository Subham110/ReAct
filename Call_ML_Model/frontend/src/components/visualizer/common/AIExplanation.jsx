import { Clock } from 'lucide-react';

const AIExplanation = ({ analysis, processingTime }) => {
  return (
  <>
    <div className="bg-gradient-to-br from-indigo-950/40 to-gray-900/80 backdrop-blur-md border border-indigo-500/20 rounded-xl p-6 flex flex-col shadow-xl relative overflow-hidden group">
      <div className="absolute top-0 right-0 w-32 h-32 bg-indigo-500/10 rounded-full blur-3xl group-hover:bg-indigo-500/20 transition-all duration-700 pointer-events-none"></div>
      
      <div className="flex items-center gap-2 mb-4">
        <h3 className="text-sm font-semibold text-indigo-300 uppercase tracking-wider">
          Analysis
        </h3>
      </div>
      
      <div className="flex-1 overflow-y-auto custom-scrollbar pr-2 relative z-10">
        <p className="text-gray-300 leading-relaxed text-[15px] font-light">
          {analysis}
        </p>
      </div>
      
      <div className="mt-6 pt-4 border-t border-gray-800/60 flex justify-between items-center text-xs text-gray-500">
        <span className="flex items-center gap-1.5">
          <Clock className="w-3.5 h-3.5" />
          Model processing time
        </span>
        <span className="font-mono bg-gray-900 px-2 py-1 rounded border border-gray-800">
          {processingTime.toFixed(2)}ms
        </span>
      </div>
    </div>
  </>
  );
};

export default AIExplanation;
