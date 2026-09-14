import React from 'react';
import { Loader2, Flower2 } from 'lucide-react';

const LoadingSpinner = () => {
  return (
  <>
    <div className="flex flex-col items-center justify-center p-12 space-y-4">
      <div>
        <Loader2 className="w-8 h-8 text-indigo-400 animate-spin absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2" /> 
      </div>
      <p>Thinking...</p>
    </div>
  </>
  );
};

export default LoadingSpinner;
