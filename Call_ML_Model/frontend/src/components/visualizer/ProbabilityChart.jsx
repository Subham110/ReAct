import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';

const COLORS = {
  setosa: '#10b981', // emerald-500
  versicolor: '#f59e0b', // amber-500
  virginica: '#8b5cf6' // violet-500
};

const ProbabilityChart = ({ probabilities, predictedSpecies }) => {
  const data = probabilities.map(p => ({
    name: p.species.charAt(0).toUpperCase() + p.species.slice(1),
    speciesKey: p.species,
    value: p.probability * 100,
    label: `${(p.probability * 100).toFixed(1)}%`
  }));

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-gray-900 border border-gray-700 rounded-lg p-3 shadow-xl">
          <p className="text-gray-300 text-sm font-medium">{payload[0].payload.name}</p>
          <p className="text-xl font-bold" style={{ color: payload[0].payload.fill }}>
            {payload[0].value.toFixed(1)}%
          </p>
        </div>
      );
    }
    return null;
  };

  return (
  <>
    <div className="bg-gray-900/50 backdrop-blur-sm border border-gray-800 rounded-xl p-6 flex flex-col shadow-xl">
      <h3 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-6">
        Species Probability Distribution
      </h3>
      <div className="flex-1 min-h-[250px] w-full">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            layout="vertical"
            data={data}
            margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
          >
            <XAxis type="number" domain={[0, 100]} hide />
            <YAxis 
              dataKey="name" 
              type="category" 
              axisLine={false} 
              tickLine={false} 
              tick={{ fill: '#9ca3af', fontSize: 14 }}
              width={80}
            />
            <Tooltip content={<CustomTooltip />} cursor={{ fill: 'rgba(255,255,255,0.05)' }} />
            <Bar dataKey="value" radius={[0, 6, 6, 0]} barSize={32} animationDuration={1000}>
              {data.map((entry, index) => (
                <Cell 
                  key={`cell-${index}`} 
                  fill={COLORS[entry.speciesKey] || '#6366f1'} 
                  fillOpacity={entry.speciesKey === predictedSpecies ? 1 : 0.4}
                />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  </>
  );
};

export default ProbabilityChart;
