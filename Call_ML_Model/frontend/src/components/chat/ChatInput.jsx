import { useState } from 'react';
import { Send } from 'lucide-react';

const ChatInput = ({ onSubmit, loading }) => {
  const [input, setInput] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim() && !loading) {
      onSubmit(input);
    }
  };

  const fillPreset = (text) => {
    setInput(text);
  };

  return (
  <>
    <div className="bg-white/10 backdrop-blur-sm border border-gray-800 rounded-xl p-4 shadow-xl">
      <div className="flex flex-wrap gap-2 mb-3">
        <span className="text-xs text-gray-500 uppercase tracking-wider font-semibold mr-2 flex items-center">
          Quick Samples
        </span>

        {/*Iris Presets */}
        <button 
          onClick={() => fillPreset("Classify: sepal 5.1, 3.5, petal 1.4, 0.2")}
          className="text-xs bg-gray-800 hover:bg-gray-700/60 text-white/80 hover:text-green-300 border border-gray-700 hover:border-green-700/50 px-3 py-1.5 rounded-full transition-colors">
          Iris
        </button>
        {/* Titanic Presets */}
        <button 
          onClick={() => fillPreset("Would Jack survive? 3rd class, male, age 20, fare 5, no cabin, embarked S")}
          className="text-xs bg-gray-800 hover:bg-gray-700/60 text-white/80 hover:text-red-300 border border-gray-700 hover:border-red-700/50 px-3 py-1.5 rounded-full transition-colors">
         Titanic
        </button>
      </div>

      <form onSubmit={handleSubmit} className="flex gap-2">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Enter iris measurements or describe a Titanic passenger..."
          disabled={loading}
          className="flex-1 bg-white/10 border border-white/20 text-gray-100 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500 transition-all placeholder:text-black/60 disabled:opacity-50"
        />
        <button
          type="submit"
          disabled={!input.trim() || loading}
          className="bg-indigo-600 hover:bg-indigo-500 text-white px-5 py-3 rounded-xl font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2 shadow-lg shadow-indigo-900/20"
        >
          <Send className="w-4 h-4" />
          <span className="hidden sm:inline">Analyze</span>
        </button>
      </form>
    </div>
  </>
  );
};

export default ChatInput;
