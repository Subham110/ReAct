import { PieChart, Pie, Cell, ResponsiveContainer } from 'recharts';

const SurvivalGauge = ({ survived, survivalProbability }) => {
  const percentage = (survivalProbability ?? 0) * 100;

  let label = 'Very Low';
  if (percentage >= 80) label = 'Very High';
  else if (percentage >= 60) label = 'High';
  else if (percentage >= 40) label = 'Moderate';
  else if (percentage >= 20) label = 'Low';

  const data = [
    { name: 'Probability', value: percentage },
    { name: 'Remaining', value: 100 - percentage },
  ];

  const outcomeColor = survived ? '#10b981' : '#ef4444';
  const outcomeLabel = survived ? 'SURVIVED' : 'PERISHED';

  return (
    <div className="bg-gray-900/50 backdrop-blur-sm border border-gray-800 rounded-xl p-6 flex flex-col items-center justify-center shadow-xl relative overflow-hidden">
      <h3 className="text-sm font-semibold text-gray-400 uppercase tracking-wider self-start mb-2 w-full text-left z-10">
        Survival Prediction
      </h3>

      <div className="w-full h-[220px] relative mt-4">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={data}
              cx="50%"
              cy="70%"
              startAngle={180}
              endAngle={0}
              innerRadius={70}
              outerRadius={95}
              paddingAngle={0}
              dataKey="value"
              stroke="none"
              cornerRadius={4}
            >
              <Cell
                fill={outcomeColor}
                className="drop-shadow-lg"
                style={{ filter: `drop-shadow(0px 0px 8px ${outcomeColor}80)` }}
              />
              <Cell fill="#1f2937" />
            </Pie>
          </PieChart>
        </ResponsiveContainer>
        <div className="absolute inset-0 flex flex-col items-center justify-end pb-8">
          <span className="text-4xl font-bold text-white tracking-tight">
            {percentage.toFixed(1)}%
          </span>
          <span className="text-sm text-gray-400 mt-1 font-medium">
            {label} Probability
          </span>
        </div>
      </div>

      <div className="mt-2 text-center w-full">
        <p className="text-sm text-gray-500 mb-2">Predicted Outcome</p>
        <div
          className="inline-block px-4 py-1.5 rounded-full border font-semibold tracking-wide uppercase text-sm"
          style={{
            color: outcomeColor,
            borderColor: `${outcomeColor}60`,
            backgroundColor: `${outcomeColor}20`,
          }}
        >
          {outcomeLabel}
        </div>
      </div>
    </div>
  );
};

export default SurvivalGauge;
