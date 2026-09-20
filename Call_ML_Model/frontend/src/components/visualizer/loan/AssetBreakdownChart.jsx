import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip,
  Legend, ReferenceLine, ResponsiveContainer,
} from 'recharts';

const fmt = (v) => {
  if (v >= 1e7) return `₹${(v / 1e7).toFixed(1)}Cr`;
  if (v >= 1e5) return `₹${(v / 1e5).toFixed(1)}L`;
  return `₹${v.toLocaleString()}`;
};

const AssetBreakdownChart = ({ financialSummary, inputFeatures }) => {
  if (!financialSummary || !inputFeatures) return null;

  const assets = [
    {
      name: 'Residential',
      value: inputFeatures.residential_assets_value ?? 0,
      fill: '#6366f1',
    },
    {
      name: 'Commercial',
      value: inputFeatures.commercial_assets_value ?? 0,
      fill: '#8b5cf6',
    },
    {
      name: 'Luxury',
      value: inputFeatures.luxury_assets_value ?? 0,
      fill: '#a78bfa',
    },
    {
      name: 'Bank',
      value: inputFeatures.bank_asset_value ?? 0,
      fill: '#c4b5fd',
    },
  ];

  const loanAmount = financialSummary.loan_amount ?? 0;
  const chartData = assets.map((a) => ({ ...a, loan: loanAmount }));

  return (
    <div className="bg-gray-900/80 backdrop-blur border border-gray-800 rounded-2xl p-5">
      <h3 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-4">
        Asset vs Loan Breakdown
      </h3>

      <ResponsiveContainer width="100%" height={220}>
        <BarChart data={chartData} margin={{ top: 5, right: 10, left: 10, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#1f2937" />
          <XAxis dataKey="name" tick={{ fill: '#6b7280', fontSize: 11 }} />
          <YAxis tickFormatter={fmt} tick={{ fill: '#6b7280', fontSize: 10 }} width={58} />
          <Tooltip
            formatter={(v) => fmt(v)}
            contentStyle={{ backgroundColor: '#111827', border: '1px solid #374151', borderRadius: 8 }}
            labelStyle={{ color: '#d1d5db' }}
          />
          <Legend wrapperStyle={{ color: '#9ca3af', fontSize: 11 }} />
          <ReferenceLine
            y={loanAmount}
            stroke="#ef4444"
            strokeDasharray="4 2"
            label={{ value: 'Loan', fill: '#ef4444', fontSize: 10, position: 'insideTopRight' }}
          />
          <Bar dataKey="value" name="Asset Value" radius={[4, 4, 0, 0]}>
            {chartData.map((entry, i) => (
              <rect key={i} fill={entry.fill} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>

      {/* Coverage ratio summary */}
      <div className="flex justify-between mt-3 text-xs text-gray-500">
        <span>Total Assets: <span className="text-indigo-400 font-medium">{fmt(financialSummary.total_assets ?? 0)}</span></span>
        <span>Loan: <span className="text-red-400 font-medium">{fmt(loanAmount)}</span></span>
        <span>Coverage: <span className="text-white font-semibold">{financialSummary.asset_coverage_ratio ?? 0}×</span></span>
      </div>
    </div>
  );
};

export default AssetBreakdownChart;

