import ApprovalGauge from './ApprovalGauge';
import AssetBreakdownChart from './AssetBreakdownChart';
import FinancialProfileCard from './FinancialProfileCard';
import AIExplanation from '../common/AIExplanation';


const LoanAIVisualizer = ({ result, processingTime }) => {
  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
      {/* 1. Top-Left: Approval Probability Gauge */}
      <ApprovalGauge
        approved={result.approved}
        approvalProbability={result.approval_probability}
        cibilRating={result.cibil_rating}
      />

      {/* 2. Top-Right: Applicant Profile & Risk Factors */}
      <FinancialProfileCard
        inputFeatures={result.input_features}
        riskFactors={result.risk_factors}
        financialSummary={result.financial_summary}
      />

      {/* 3. Bottom-Left: Asset Breakdown Chart */}
      <AssetBreakdownChart
        financialSummary={result.financial_summary}
        inputFeatures={result.input_features}
      />

      {/* 4. Bottom-Right: AI Analytical Reasoning */}
      <AIExplanation
        analysis={result.analysis}
        processingTime={processingTime}
      />
    </div>
  );
};

export default LoanAIVisualizer;

