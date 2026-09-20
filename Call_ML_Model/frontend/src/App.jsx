import React from 'react';
import Header from './components/common/Header';
import ChatInput from './components/chat/ChatInput';
import LoadingSpinner from './components/common/LoadingSpinner';
import ErrorAlert from './components/common/ErrorAlert';
import { IrisAIVisualizer, TitanicAIVisualizer, LoanAIVisualizer } from './components/visualizer';
import { useBotanicalAgent } from './hooks/useBotanicalAgent';

function App() {
  const { loading, error, result, domain, processingTime, analyze } = useBotanicalAgent();

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-950 via-gray-900 to-white flex flex-col text-gray-100">
      <Header />
      <main className="flex-grow container mx-auto px-4 py-6 max-w-6xl flex flex-col">
        <div className="flex flex-col justify-between flex-1 gap-6 w-full min-h-[calc(100vh-140px)]">
          {/* Visualization Area */}
          <div className="flex-1 flex flex-col justify-center">
            {error && (
              <div className="mb-6">
                <ErrorAlert message={error} />
              </div>
            )}

            {loading && (
              <div className="py-12 flex justify-center items-center">
                <LoadingSpinner />
              </div>
            )}

            {result && !loading && domain === 'iris' && (
              <IrisAIVisualizer result={result} processingTime={processingTime} />
            )}

            {result && !loading && domain === 'titanic' && (
              <TitanicAIVisualizer result={result} processingTime={processingTime} />
            )}

            {result && !loading && domain === 'loan' && (
              <LoanAIVisualizer result={result} processingTime={processingTime} />
            )}
          </div>

          {/* Input Bar — always at bottom */}
          <div className="sticky bottom-4 z-30 pt-2">
            <ChatInput onSubmit={analyze} loading={loading} />
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
