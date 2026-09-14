import SurvivalGauge from './SurvivalGauge';
import PassengerProfileCard from './PassengerProfileCard';
import DemographicBenchmark from './DemographicBenchmark';
import AIExplanation from '../common/AIExplanation';


const TitanicAIVisualizer = ({ result, processingTime }) => {
  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
      {/* 1. Top-Left: Survival Probability Gauge */}
      <SurvivalGauge
        survived={result.survived}
        survivalProbability={result.survival_probability ?? result.confidence ?? 0}
      />

      {/* 2. Top-Right: Passenger Profile & Risk Factors */}
      <PassengerProfileCard
        passengerProfile={result.passenger_profile}
        riskFactors={result.risk_factors}
      />

      {/* 3. Bottom-Left: Demographic Benchmark Bars */}
      <DemographicBenchmark
        passengerProfile={result.passenger_profile}
        survived={result.survived}
        survivalProbability={result.survival_probability ?? result.confidence ?? 0}
      />

      {/* 4. Bottom-Right: AI Analytical Reasoning */}
      <AIExplanation
        analysis={result.analysis}
        processingTime={processingTime}
      />
    </div>
  );
};

export default TitanicAIVisualizer;
