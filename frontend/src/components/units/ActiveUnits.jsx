import { Siren } from 'lucide-react';
import { units } from '../../data/mockData';
import { cn } from '../../lib/utils';

const getStatusColor = (status) => {
  switch (status) {
    case 'Assigned':
      return 'bg-primary';
    case 'Unassigned':
      return 'bg-success';
    case 'Inactive':
      return 'bg-text-secondary';
    default:
      return 'bg-gray-500';
  }
};

const ActiveUnits = () => {
  return (
    <div className="bg-surface border border-border rounded-lg p-4">
      <div className="flex items-center mb-4">
        <Siren className="w-5 h-5 mr-3 text-primary" />
        <h3 className="font-bold text-text">Active Units ({units.length})</h3>
      </div>
      <ul className="space-y-4">
        {units.slice(0, 4).map((unit) => (
          <li key={unit.id} className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <img
                src={unit.avatar}
                alt={unit.unitHead}
                className="w-10 h-10 rounded-full object-cover"
              />
              <div>
                <p className="font-semibold text-sm text-text">{unit.unitHead}</p>
                <p className="text-xs text-text-secondary">{unit.type}</p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-xs font-medium text-text-secondary">{unit.status}</span>
              <div className={cn('w-2.5 h-2.5 rounded-full', getStatusColor(unit.status))} />
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ActiveUnits;
