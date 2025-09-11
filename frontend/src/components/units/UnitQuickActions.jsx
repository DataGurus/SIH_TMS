import { Phone, Radio } from 'lucide-react';
import { Button } from '../ui/Button';

const UnitQuickActions = ({ unit }) => {
  return (
    <div className="bg-surface border border-border rounded-lg p-4 h-full">
      <div className="flex items-center gap-3 mb-4">
        <img src={unit.avatar} alt={unit.unitHead} className="h-10 w-10 rounded-full" />
        <div>
            <h3 className="text-lg font-semibold text-text">Actions for {unit.id}</h3>
            <p className="text-sm text-text-secondary">{unit.unitHead}</p>
        </div>
      </div>
      <div className="space-y-3">
        <Button className="w-full justify-start gap-3">
          <Phone size={16} />
          Call Unit Head
        </Button>
        <Button variant="secondary" className="w-full justify-start gap-3">
          <Radio size={16} />
          Contact via Walkie Talkie
        </Button>
      </div>
    </div>
  );
};

export default UnitQuickActions;
