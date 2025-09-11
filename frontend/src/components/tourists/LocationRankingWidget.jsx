import { BarChart, ArrowUp, ArrowDown, Minus } from 'lucide-react';
import { locationRankings } from '../../data/mockData';

const TrendIcon = ({ trend }) => {
  switch (trend) {
    case 'up':
      return <ArrowUp className="w-4 h-4 text-success" />;
    case 'down':
      return <ArrowDown className="w-4 h-4 text-error" />;
    case 'stable':
      return <Minus className="w-4 h-4 text-text-secondary" />;
  }
};

const LocationRankingWidget = () => {
  return (
    <div className="bg-surface border border-border rounded-lg p-4">
      <div className="flex items-center mb-4">
        <BarChart className="w-5 h-5 mr-3 text-primary" />
        <h3 className="font-bold text-text">Location Rankings</h3>
      </div>
      <ul className="space-y-3">
        {locationRankings.map((loc) => (
          <li key={loc.rank} className="flex items-center justify-between text-sm">
            <div className="flex items-center gap-3">
              <span className="font-bold text-text-secondary w-6 text-center">{loc.rank}</span>
              <p className="font-medium text-text">{loc.location}</p>
            </div>
            <div className="flex items-center gap-3">
              <span className="text-text-secondary">{loc.touristCount}</span>
              <TrendIcon trend={loc.trend} />
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default LocationRankingWidget;
