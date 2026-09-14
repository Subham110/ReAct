import { User, Ship, MapPin, Users, Ticket, DoorOpen } from 'lucide-react';

const CLASS_LABELS = { 1: '1st Class', 2: '2nd Class', 3: '3rd Class' };
const EMBARKED_LABELS = { S: 'Southampton', C: 'Cherbourg', Q: 'Queenstown' };

const PassengerProfileCard = ({ passengerProfile, riskFactors }) => {
  if (!passengerProfile) return null;

  const traits = [
    { icon: User, label: 'Title', value: passengerProfile.title || '—' },
    { icon: Ticket, label: 'Class', value: CLASS_LABELS[passengerProfile.class] || '—' },
    { icon: User, label: 'Age', value: passengerProfile.age ? `${passengerProfile.age} years` : 'Unknown' },
    { icon: Users, label: 'Sex', value: passengerProfile.sex?.charAt(0).toUpperCase() + passengerProfile.sex?.slice(1) || '—' },
    { icon: Users, label: 'Family Size', value: passengerProfile.family_size ?? '—' },
    { icon: DoorOpen, label: 'Cabin', value: passengerProfile.has_cabin ? 'Yes' : 'No' },
    { icon: MapPin, label: 'Embarked', value: EMBARKED_LABELS[passengerProfile.embarked] || passengerProfile.embarked || '—' },
    { icon: Ship, label: 'Fare', value: passengerProfile.fare != null ? `£${passengerProfile.fare.toFixed(2)}` : '—' },
  ];

  const factors = riskFactors ? Object.entries(riskFactors) : [];

  return (
    <div className="bg-gray-900/50 backdrop-blur-sm border border-gray-800 rounded-xl p-6 flex flex-col shadow-xl">
      <h3 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-4">
        Passenger Profile
      </h3>

      {/* Trait Grid */}
      <div className="grid grid-cols-2 gap-3 mb-5">
        {traits.map(({ icon: Icon, label, value }) => (
          <div key={label} className="flex items-center gap-2 text-sm">
            <Icon className="w-4 h-4 text-gray-500 flex-shrink-0" />
            <span className="text-gray-500">{label}:</span>
            <span className="text-gray-200 font-medium truncate">{value}</span>
          </div>
        ))}
      </div>

      {/* Risk Factors */}
      {factors.length > 0 && (
        <>
          <div className="border-t border-gray-800 pt-4 mt-auto">
            <h4 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3">
              Risk Factors
            </h4>
            <div className="space-y-2 max-h-[180px] overflow-y-auto custom-scrollbar pr-1">
              {factors.map(([key, description]) => {
                const isPositive = description.toLowerCase().includes('positive');
                const isNegative = description.toLowerCase().includes('negative');

                return (
                  <div
                    key={key}
                    className={`flex items-start gap-2 text-xs rounded-lg px-3 py-2 border ${
                      isPositive
                        ? 'bg-emerald-950/30 border-emerald-800/40 text-emerald-300'
                        : isNegative
                        ? 'bg-red-950/30 border-red-800/40 text-red-300'
                        : 'bg-gray-800/40 border-gray-700/40 text-gray-400'
                    }`}
                  >
                    <span className="font-semibold shrink-0 capitalize mt-0.5">
                      {key.replace(/_/g, ' ')}:
                    </span>
                    <span className="font-light leading-relaxed">{description}</span>
                  </div>
                );
              })}
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default PassengerProfileCard;
