import { Button } from '../ui/Button';
import { cn } from '../../lib/utils';
import { Shield, MessageSquareWarning, Send } from 'lucide-react';

const getSafetyColor = (score) => {
  if (score < 50) return 'text-error';
  if (score < 80) return 'text-warning';
  return 'text-success';
};

const TouristActions = ({ tourist }) => {
  return (
    <div className="bg-surface border border-border rounded-lg p-6 space-y-6">
      <div className="flex flex-col items-center text-center">
        <img
          src={tourist.avatar}
          alt={tourist.name}
          className="w-24 h-24 rounded-full object-cover border-4 border-border mb-4"
        />
        <h3 className="text-xl font-bold text-text">{tourist.name}</h3>
        <p className="text-sm text-text-secondary">{tourist.displayId} &middot; {tourist.locationTag}</p>
      </div>

      <div className="bg-background p-4 rounded-lg flex items-center justify-between">
        <div className="flex items-center gap-2">
            <Shield className={cn("w-5 h-5", getSafetyColor(tourist.safetyScore))} />
            <span className="text-sm text-text-secondary">Safety Score</span>
        </div>
        <span className={cn("text-lg font-bold", getSafetyColor(tourist.safetyScore))}>
          {tourist.safetyScore}
        </span>
      </div>

      <div className="space-y-3">
        <h4 className="text-sm font-semibold text-text-secondary uppercase tracking-wider">Actions</h4>
        <Button variant="outline" className="w-full justify-start gap-3">
            <MessageSquareWarning className="w-4 h-4" />
            Send Alert
        </Button>
        <Button variant="outline" className="w-full justify-start gap-3">
            <Send className="w-4 h-4" />
            Assign Unit
        </Button>
        <Button variant="default" className="w-full">
            View Full Profile
        </Button>
      </div>
    </div>
  );
};

export default TouristActions;
