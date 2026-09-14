import { PieChart, Pie, Cell, ResponsiveContainer } from 'recharts';

const COLORS = {
  setosa: '#10b981',
  versicolor: '#f59e0b',
  virginica: '#8b5cf6',
  background: '#1f2937'
};

const ConfidenceGauge = ({ confidence, species }) => {
  const percentage = confidence * 100;
  
  let label = "Low";
  if (percentage >= 90) label = "Very High";
  else if (percentage >= 75) label = "High";
  else if (percentage >= 50) label = "Moderate";

  const data = [
    { name: 'Confidence', value: percentage },
    { name: 'Remaining', value: 100 - percentage }
  ];

  const speciesColor = COLORS[species?.toLowerCase()] || '#6366f1';

  return (
    <>
    <div className="bg-gray-900/50 backdrop-blur-sm border border-gray-800 rounded-xl p-6 flex flex-col items-center justify-center shadow-xl relative overflow-hidden">
      <h3 className="text-sm font-semibold text-gray-400 uppercase tracking-wider self-start mb-2 w-full text-left z-10">
        Prediction Confidence
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
              <Cell fill={speciesColor} className="drop-shadow-lg" style={{ filter: `drop-shadow(0px 0px 8px ${speciesColor}80)` }} />
              <Cell fill={COLORS.background} />
            </Pie>
          </PieChart>
        </ResponsiveContainer>
        <div className="absolute inset-0 flex flex-col items-center justify-end pb-8">
          <span className="text-4xl font-bold text-white tracking-tight">
            {percentage.toFixed(1)}%
          </span>
          <span className="text-sm text-gray-400 mt-1 font-medium">{label} Confidence</span>
        </div>
      </div>
      
      <div className="mt-2 text-center w-full">
        <p className="text-sm text-gray-500 mb-2">Predicted Species</p>
        <div 
          className="inline-block px-4 py-1.5 rounded-full border bg-opacity-20 backdrop-blur-md font-semibold tracking-wide uppercase text-sm"
          style={{ 
            color: speciesColor, 
            borderColor: `${speciesColor}60`, 
            backgroundColor: `${speciesColor}20` 
          }}
        >
          Iris {species}
        </div>
      </div>
    </div>
   </> 
  );
};

export default ConfidenceGauge;
