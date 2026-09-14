import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, Legend, Tooltip } from 'recharts';

const COLORS = {
  input: '#ffffff',
  setosa: '#10b981',
  versicolor: '#f59e0b',
  virginica: '#8b5cf6'
};

const FeatureRadar = ({ featureComparison, predictedSpecies }) => {
  const data = featureComparison.map(feature => ({
    subject: feature.feature.replace(' Length', ' L.').replace(' Width', ' W.'),
    fullSubject: feature.feature,
    Input: feature.input_value,
    Setosa: feature.setosa_avg,
    Versicolor: feature.versicolor_avg,
    Virginica: feature.virginica_avg,
  }));

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-gray-900 border border-gray-700 rounded-lg p-3 shadow-xl min-w-[150px]">
          <p className="text-gray-300 text-sm font-semibold mb-2 pb-2 border-b border-gray-700">
            {payload[0].payload.fullSubject}
          </p>
          {payload.map((entry, idx) => (
            <div key={idx} className="flex justify-between text-xs py-1">
              <span style={{ color: entry.color }} className="font-medium">{entry.name}:</span>
              <span className="text-gray-200 font-mono ml-3">{entry.value}cm</span>
            </div>
          ))}
        </div>
      );
    }
    return null;
  };

  return (
  <>
    <div className="bg-gray-900/50 backdrop-blur-sm border border-gray-800 rounded-xl p-6 flex flex-col shadow-xl">
      <h3 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-2">
        Feature Comparison Radar
      </h3>
      <div className="flex-1 w-full min-h-[300px]">
        <ResponsiveContainer width="100%" height="100%">
          <RadarChart cx="50%" cy="50%" outerRadius="75%" data={data} margin={{ top: 10, right: 10, bottom: 10, left: 10 }}>
            <PolarGrid stroke="#374151" strokeDasharray="3 3" />
            <PolarAngleAxis dataKey="subject" tick={{ fill: '#9ca3af', fontSize: 12 }} />
            <PolarRadiusAxis angle={30} domain={[0, 'auto']} tick={{ fill: '#6b7280', fontSize: 10 }} />
            
            <Tooltip content={<CustomTooltip />} />
            
            <Radar name="Input" dataKey="Input" stroke={COLORS.input} strokeWidth={3} fill={COLORS.input} fillOpacity={0.1} />
            
            {predictedSpecies !== 'setosa' && (
              <Radar name="Setosa" dataKey="Setosa" stroke={COLORS.setosa} fill={COLORS.setosa} fillOpacity={0.0} strokeDasharray="4 4" />
            )}
            {predictedSpecies !== 'versicolor' && (
              <Radar name="Versicolor" dataKey="Versicolor" stroke={COLORS.versicolor} fill={COLORS.versicolor} fillOpacity={0.0} strokeDasharray="4 4" />
            )}
            {predictedSpecies !== 'virginica' && (
              <Radar name="Virginica" dataKey="Virginica" stroke={COLORS.virginica} fill={COLORS.virginica} fillOpacity={0.0} strokeDasharray="4 4" />
            )}
            
            {predictedSpecies === 'setosa' && (
              <Radar name="Setosa Avg" dataKey="Setosa" stroke={COLORS.setosa} strokeWidth={2} fill={COLORS.setosa} fillOpacity={0.2} />
            )}
            {predictedSpecies === 'versicolor' && (
              <Radar name="Versicolor Avg" dataKey="Versicolor" stroke={COLORS.versicolor} strokeWidth={2} fill={COLORS.versicolor} fillOpacity={0.2} />
            )}
            {predictedSpecies === 'virginica' && (
              <Radar name="Virginica Avg" dataKey="Virginica" stroke={COLORS.virginica} strokeWidth={2} fill={COLORS.virginica} fillOpacity={0.2} />
            )}
            
            <Legend wrapperStyle={{ paddingTop: '20px', fontSize: '12px' }} />
          </RadarChart>
        </ResponsiveContainer>
      </div>
    </div>
  </> 
  );
};

export default FeatureRadar;
