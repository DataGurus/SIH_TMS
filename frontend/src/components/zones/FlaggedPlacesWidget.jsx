import { MapPin, Flag, Trash2, ShieldAlert, Ban, ShieldCheck } from 'lucide-react';

const ZONE_TYPE_CONFIG = {
  'high-risk': { icon: ShieldAlert, color: 'text-error', order: 1, label: 'High Risk' },
  'no-entry': { icon: Ban, color: 'text-text-secondary', order: 2, label: 'No Entry' },
  'safe': { icon: ShieldCheck, color: 'text-success', order: 3, label: 'Safe Zone' },
};

const FlaggedPlacesWidget = ({ zones, onSelectZone, onDeleteZone }) => {
  const sortedZones = [...zones].sort((a, b) => {
    const configA = ZONE_TYPE_CONFIG[a.type];
    const configB = ZONE_TYPE_CONFIG[b.type];

    if (configA.order !== configB.order) {
      return configA.order - configB.order;
    }

    if (a.type === 'high-risk') {
      return b.radius - a.radius; // Sort by radius descending for high-risk
    }

    return a.name.localeCompare(b.name);
  });

  return (
    <div className="bg-surface border border-border rounded-lg p-4 flex flex-col h-full">
      <div className="flex items-center mb-4">
        <Flag className="w-5 h-5 mr-3 text-primary" />
        <h3 className="font-bold text-text">Flagged Places ({zones.length})</h3>
      </div>
      <div className="flex-1 overflow-y-auto pr-2 -mr-2">
        <ul className="space-y-2">
          {sortedZones.map((zone) => {
            const config = ZONE_TYPE_CONFIG[zone.type];
            const Icon = config.icon;
            return (
              <li
                key={zone.id}
                className="flex items-center justify-between p-2 rounded-md hover:bg-background group transition-colors"
              >
                <div 
                  className="flex items-center gap-3 cursor-pointer flex-1"
                  onClick={() => onSelectZone(zone)}
                >
                  <Icon className={`w-5 h-5 ${config.color} flex-shrink-0`} />
                  <div className="flex-1 overflow-hidden">
                    <p className="font-semibold text-sm text-text truncate">{zone.name}</p>
                    <p className="text-xs text-text-secondary">{zone.radius}m radius • {config.label}</p>
                  </div>
                </div>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    onDeleteZone(zone.id);
                  }}
                  className="ml-2 p-1.5 rounded-md text-text-secondary hover:bg-error/20 hover:text-error opacity-0 group-hover:opacity-100 transition-all"
                  aria-label={`Delete ${zone.name}`}
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </li>
            );
          })}
        </ul>
      </div>
    </div>
  );
};

export default FlaggedPlacesWidget;
