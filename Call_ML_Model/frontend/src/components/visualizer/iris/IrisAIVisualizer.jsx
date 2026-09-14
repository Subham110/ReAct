import ConfidenceGauge from './ConfidenceGauge';
import ProbabilityChart from './ProbabilityChart';
import FeatureRadar from './FeatureRadar';
import AIExplanation from '../common/AIExplanation';


const IrisAIVisualizer = ({ result, processingTime }) => {
  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
      {/* 1. Top-Left: Radial Confidence Gauge */}
      <ConfidenceGauge 
        confidence={result.prediction.confidence} 
        species={result.prediction.species} 
      />
       {/* 2. Top-Right: Horizontal Probability Distribution Bars */}
      <ProbabilityChart 
        probabilities={result.probabilities} 
        predictedSpecies={result.prediction.species} 
      />
      {/* 3. Bottom-Left: 4-Axis Feature Comparison Radar */}
      <FeatureRadar 
        featureComparison={result.feature_comparison} 
        predictedSpecies={result.prediction.species}
      />
      {/* 4. Bottom-Right: AI Analytical Reasoning Breakdown */}
      <AIExplanation 
        analysis={result.analysis} 
        processingTime={processingTime} 
      />
    </div>
  );
};

export default IrisAIVisualizer;
