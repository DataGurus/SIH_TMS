import { Users } from 'lucide-react';
import { tourists } from '../../data/mockData';
import { cn } from '../../lib/utils';

const getSafetyColor = (score) => {
  if (score < 50) return 'bg-error';
  if (score < 80) return 'bg-warning';
  return 'bg-success';
};

const ActiveTouristsWidget = () => {
  const activeTourists = tourists.slice(0, 10);

  return (
    <div className="bg-surface border border-border rounded-lg p-4 flex flex-col h-96">
      <div className="flex items-center mb-4">
        <Users className="w-5 h-5 mr-3 text-primary" />
        <h3 className="font-bold text-text">
          Real-time Active Tourists ({tourists.length})
        </h3>
      </div>
      <div className="flex-1 overflow-y-auto pr-2 -mr-2">
        <ul className="space-y-4">
          {activeTourists.map((tourist) => (
            <li key={tourist.id} className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <img
                  src={tourist.avatar}
                  alt={tourist.name}
                  className="w-10 h-10 rounded-full object-cover"
                />
                <div>
                  <p className="font-semibold text-sm text-text">{tourist.name}</p>
                  <p className="text-xs text-text-secondary">{tourist.displayId}</p>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-sm font-medium text-text-secondary">{tourist.safetyScore}</span>
                <div className={cn('w-2.5 h-2.5 rounded-full', getSafetyColor(tourist.safetyScore))} />
              </div>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default ActiveTouristsWidget;
