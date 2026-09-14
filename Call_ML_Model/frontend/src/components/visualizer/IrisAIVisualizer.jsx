import React from 'react';
import { useBotanicalAgent } from '../../hooks/useBotanicalAgent';
import ChatInput from '../chat/ChatInput';
import LoadingSpinner from '../common/LoadingSpinner';
import ErrorAlert from '../common/ErrorAlert';
import ConfidenceGauge from './ConfidenceGauge';
import ProbabilityChart from './ProbabilityChart';
import FeatureRadar from './FeatureRadar';
import AIExplanation from './AIExplanation';
import { Flower2 } from 'lucide-react';

const IrisAIVisualizer = () => {
  const { loading, error, result, processingTime, analyze } = useBotanicalAgent();

  return (
    <div className="flex flex-col justify-between flex-1 gap-6 w-full min-h-[calc(100vh-140px)]">
      {/* Visualizations & Content Area (Top / Middle) */}
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

        {!result && !loading && !error && (
          <div className="flex flex-col items-center justify-center text-center p-8 border border-dashed border-gray-800 rounded-2xl bg-gray-900/20 my-auto">
            <div className="p-4 bg-indigo-500/10 rounded-2xl border border-indigo-500/20 mb-4">
              <Flower2 className="w-12 h-12 text-indigo-400" />
            </div>
            <h2 className="text-xl font-semibold text-gray-200 mb-2">Ready for Classification</h2>
            <p className="text-sm text-gray-400 max-w-md">
              Enter sepal and petal measurements below or choose a quick sample to analyze iris flower species.
            </p>
          </div>
        )}

        {result && !loading && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
            <ConfidenceGauge 
              confidence={result.prediction.confidence} 
              species={result.prediction.species} 
            />
            <ProbabilityChart 
              probabilities={result.probabilities} 
              predictedSpecies={result.prediction.species} 
            />
            <FeatureRadar 
              featureComparison={result.feature_comparison} 
              predictedSpecies={result.prediction.species}
            />
            <AIExplanation 
              analysis={result.analysis} 
              processingTime={processingTime} 
            />
          </div>
        )}
      </div>

      {/* Input Section (Positioned at the Bottom) */}
      <div className="sticky bottom-4 z-30 pt-2">
        <ChatInput onSubmit={analyze} loading={loading} />
      </div>
    </div>
  );
};

export default IrisAIVisualizer;
