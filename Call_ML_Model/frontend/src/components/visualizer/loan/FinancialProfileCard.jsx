import { User, Briefcase, GraduationCap, AlertTriangle, CheckCircle } from 'lucide-react';

const fmt = (v) => {
  if (v >= 1e7) return `₹${(v / 1e7).toFixed(2)} Cr`;
  if (v >= 1e5) return `₹${(v / 1e5).toFixed(2)} L`;
  return `₹${Number(v).toLocaleString()}`;
};

const RiskBadge = ({ label, description }) => {
  const isPositive = description?.toLowerCase().startsWith('positive');
  return (
    <div className={`flex items-start gap-2 p-2.5 rounded-lg border text-xs ${
      isPositive
        ? 'bg-emerald-900/20 border-emerald-800/40 text-emerald-300'
        : 'bg-red-900/20 border-red-800/40 text-red-300'
    }`}>
      {isPositive
        ? <CheckCircle className="w-3.5 h-3.5 mt-0.5 shrink-0" />
        : <AlertTriangle className="w-3.5 h-3.5 mt-0.5 shrink-0" />
      }
      <div>
        <span className="font-semibold capitalize">{label.replace(/_/g, ' ')}: </span>
        <span className="opacity-80">{description}</span>
      </div>
    </div>
  );
};

const FinancialProfileCard = ({ inputFeatures, riskFactors, financialSummary }) => {
  if (!inputFeatures) return null;

  return (
    <div className="bg-gray-900/80 backdrop-blur border border-gray-800 rounded-2xl p-5 flex flex-col gap-4">
      <h3 className="text-sm font-semibold text-gray-400 uppercase tracking-wider">
        Applicant Profile
      </h3>

      {/* Profile chips */}
      <div className="grid grid-cols-2 gap-2 text-xs">
        <div className="flex items-center gap-2 bg-gray-800/60 rounded-lg px-3 py-2">
          <User className="w-3.5 h-3.5 text-indigo-400" />
          <span className="text-gray-300">{inputFeatures.no_of_dependents} dependent{inputFeatures.no_of_dependents !== 1 ? 's' : ''}</span>
        </div>
        <div className="flex items-center gap-2 bg-gray-800/60 rounded-lg px-3 py-2">
          <GraduationCap className="w-3.5 h-3.5 text-purple-400" />
          <span className="text-gray-300">{inputFeatures.education}</span>
        </div>
        <div className="flex items-center gap-2 bg-gray-800/60 rounded-lg px-3 py-2">
          <Briefcase className="w-3.5 h-3.5 text-blue-400" />
          <span className="text-gray-300">
            {inputFeatures.self_employed === 'Yes' ? 'Self-employed' : 'Salaried'}
          </span>
        </div>
        <div className="flex items-center gap-2 bg-gray-800/60 rounded-lg px-3 py-2">
          <span className="text-yellow-400 text-xs font-bold">₹</span>
          <span className="text-gray-300">{fmt(inputFeatures.income_annum)} p.a.</span>
        </div>
      </div>

      {/* Loan summary row */}
      {financialSummary && (
        <div className="grid grid-cols-2 gap-2 text-xs border-t border-gray-800 pt-3">
          <div className="text-center">
            <p className="text-gray-500 mb-0.5">Loan Amount</p>
            <p className="text-white font-semibold">{fmt(financialSummary.loan_amount)}</p>
          </div>
          <div className="text-center">
            <p className="text-gray-500 mb-0.5">Loan Term</p>
            <p className="text-white font-semibold">{financialSummary.loan_term_years} yrs</p>
          </div>
          <div className="text-center">
            <p className="text-gray-500 mb-0.5">Loan/Income</p>
            <p className="text-white font-semibold">{financialSummary.loan_to_income_ratio}×</p>
          </div>
          <div className="text-center">
            <p className="text-gray-500 mb-0.5">Asset Cover</p>
            <p className="text-white font-semibold">{financialSummary.asset_coverage_ratio}×</p>
          </div>
        </div>
      )}

      {/* Risk factors */}
      {riskFactors && (
        <div className="flex flex-col gap-2 border-t border-gray-800 pt-3">
          <p className="text-xs text-gray-500 uppercase tracking-wider font-semibold">Risk Factors</p>
          {Object.entries(riskFactors).map(([key, val]) => (
            <RiskBadge key={key} label={key} description={val} />
          ))}
        </div>
      )}
    </div>
  );
};

export default FinancialProfileCard;

