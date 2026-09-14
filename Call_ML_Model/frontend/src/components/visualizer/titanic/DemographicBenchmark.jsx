import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell, ReferenceLine } from 'recharts';

/**
 * Historical Titanic survival rates by demographic group.
 * Source: Encyclopedia Titanica and various historical analyses.
 */
const HISTORICAL_RATES = {
  '1st Class': 0.63,
  '2nd Class': 0.47,
  '3rd Class': 0.24,
  'Female':    0.74,
  'Male':      0.19,
  'Child':     0.52,
  'Adult':     0.36,
};

const DemographicBenchmark = ({ passengerProfile, survived, survivalProbability }) => {
  if (!passengerProfile) return null;

  const classLabel = `${passengerProfile.class || 3}${['st', 'nd', 'rd'][((passengerProfile.class || 3) - 1)]} Class`;
  const sexLabel = passengerProfile.sex === 'female' ? 'Female' : 'Male';
  const ageLabel = (passengerProfile.age || 30) < 16 ? 'Child' : 'Adult';

  const benchmarks = [
    { group: classLabel, rate: HISTORICAL_RATES[classLabel] ?? 0.35 },
    { group: sexLabel, rate: HISTORICAL_RATES[sexLabel] ?? 0.36 },
    { group: ageLabel, rate: HISTORICAL_RATES[ageLabel] ?? 0.36 },
  ];

  const data = benchmarks.map(b => ({
    name: b.group,
    historical: +(b.rate * 100).toFixed(1),
    passenger: +(survivalProbability * 100).toFixed(1),
  }));

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-gray-900 border border-gray-700 rounded-lg p-3 shadow-xl min-w-[160px]">
          <p className="text-gray-300 text-sm font-semibold mb-2 pb-2 border-b border-gray-700">
            {payload[0].payload.name}
          </p>
          {payload.map((entry, idx) => (
            <div key={idx} className="flex justify-between text-xs py-1">
              <span style={{ color: entry.color }} className="font-medium">
                {entry.name === 'historical' ? '1912 Avg' : 'This Passenger'}:
              </span>
              <span className="text-gray-200 font-mono ml-3">{entry.value}%</span>
            </div>
          ))}
        </div>
      );
    }
    return null;
  };

  return (
    <div className="bg-gray-900/50 backdrop-blur-sm border border-gray-800 rounded-xl p-6 flex flex-col shadow-xl">
      <h3 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-6">
        Demographic Benchmark
      </h3>
      <div className="flex-1 min-h-[250px] w-full">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={data}
            margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
          >
            <XAxis
              dataKey="name"
              axisLine={false}
              tickLine={false}
              tick={{ fill: '#9ca3af', fontSize: 13 }}
            />
            <YAxis
              domain={[0, 100]}
              axisLine={false}
              tickLine={false}
              tick={{ fill: '#6b7280', fontSize: 11 }}
              tickFormatter={(v) => `${v}%`}
            />
            <Tooltip content={<CustomTooltip />} cursor={{ fill: 'rgba(255,255,255,0.05)' }} />
            <ReferenceLine y={50} stroke="#374151" strokeDasharray="3 3" />
            <Bar
              dataKey="historical"
              name="historical"
              fill="#64748b"
              radius={[4, 4, 0, 0]}
              barSize={28}
              animationDuration={800}
            />
            <Bar
              dataKey="passenger"
              name="passenger"
              radius={[4, 4, 0, 0]}
              barSize={28}
              animationDuration={1000}
            >
              {data.map((_, index) => (
                <Cell
                  key={`cell-${index}`}
                  fill={survived ? '#10b981' : '#ef4444'}
                />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
      <div className="flex gap-4 mt-3 text-xs text-gray-500 justify-center">
        <span className="flex items-center gap-1.5">
          <span className="w-3 h-3 rounded-sm bg-slate-500 inline-block"></span>
          1912 Historical Average
        </span>
        <span className="flex items-center gap-1.5">
          <span className={`w-3 h-3 rounded-sm inline-block ${survived ? 'bg-emerald-500' : 'bg-red-500'}`}></span>
          This Passenger
        </span>
      </div>
    </div>
  );
};

export default DemographicBenchmark;
