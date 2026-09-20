import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from 'recharts';

const COLORS = {
  approved: '#22c55e',
  rejected: '#ef4444',
  track: '#1f2937',
};

const CIBIL_COLOR = {
  Excellent: 'text-emerald-400 bg-emerald-900/30 border-emerald-700/50',
  Good: 'text-green-400 bg-green-900/30 border-green-700/50',
  Fair: 'text-yellow-400 bg-yellow-900/30 border-yellow-700/50',
  Poor: 'text-red-400 bg-red-900/30 border-red-700/50',
};

const ApprovalGauge = ({ approved, approvalProbability, cibilRating }) => {
  const pct = Math.round((approvalProbability ?? 0) * 100);
  const color = approved ? COLORS.approved : COLORS.rejected;

  const gaugeData = [
    { value: pct, name: approved ? 'Approved' : 'Rejected' },
    { value: 100 - pct, name: 'Remaining' },
  ];

  const cibilClass = CIBIL_COLOR[cibilRating] ?? 'text-gray-400 bg-gray-800 border-gray-600';

  return (
    <div className="bg-gray-900/80 backdrop-blur border border-gray-800 rounded-2xl p-5 flex flex-col items-center gap-3">
      <h3 className="text-sm font-semibold text-gray-400 uppercase tracking-wider w-full">
        Approval Decision
      </h3>

      <div className="relative w-48 h-48">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={gaugeData}
              cx="50%"
              cy="50%"
              startAngle={90}
              endAngle={-270}
              innerRadius={55}
              outerRadius={75}
              dataKey="value"
              strokeWidth={0}
            >
              <Cell fill={color} />
              <Cell fill={COLORS.track} />
            </Pie>
            <Tooltip formatter={(v) => `${v}%`} />
          </PieChart>
        </ResponsiveContainer>

        {/* Center label */}
        <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
          <span className="text-3xl font-bold" style={{ color }}>{pct}%</span>
          <span className="text-xs font-medium mt-1" style={{ color }}>
            {approved ? '✓ Approved' : '✗ Rejected'}
          </span>
        </div>
      </div>

      {/* CIBIL Rating Badge */}
      <div className={`px-4 py-1.5 rounded-full border text-sm font-semibold ${cibilClass}`}>
        CIBIL: {cibilRating}
      </div>

      <p className="text-xs text-gray-500 text-center">
        RandomForest model confidence based on your financial profile
      </p>
    </div>
  );
};

export default ApprovalGauge;

