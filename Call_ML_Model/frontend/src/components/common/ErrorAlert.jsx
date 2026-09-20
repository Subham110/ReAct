import React from 'react';
import { AlertCircle, X, RefreshCw } from 'lucide-react';

const ErrorAlert = ({ message, onRetry, onDismiss }) => {
  if (!message) return null;

  return (
  <>
    <div>
      <AlertCircle className="w-5 h-5 text-rose-500 mt-0.5 flex-shrink-0" />
      <div className="flex-1">
        <h3 className="text-rose-400 font-semibold text-sm mb-1">Analysis Error</h3>
        <p className="text-white-200/80 text-sm">{message}</p>
        
        {onRetry && (<button onClick={onRetry}className="mt-3 flex items-center gap-1.5 text-xs font-medium text-rose-300 hover:text-rose-200 bg-rose-900/30 hover:bg-rose-900/50 px-3 py-1.5 rounded-lg transition-colors border border-rose-800/50">
            <RefreshCw className="w-3.5 h-3.5" />
            Try Again
          </button>
        )}

      </div>
      {onDismiss && (<button onClick={onDismiss}
          className="text-rose-500/70 hover:text-rose-400 hover:bg-rose-900/30 p-1.5 rounded-lg transition-colors">
          <X className="w-4 h-4" />
        </button>
      )}

    </div>
  </>
  );
};

export default ErrorAlert;
