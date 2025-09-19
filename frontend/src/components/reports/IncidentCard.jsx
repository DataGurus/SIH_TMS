import { Card, CardContent, CardHeader, CardTitle } from '../ui/Card';
import { cn } from '../../lib/utils';
import { User, MapPin, Calendar } from 'lucide-react';

const statusColorMap = {
  'Filed Fir': 'bg-error',
  'Not filed FIr': 'bg-gray-500',
  'Completed': 'bg-success',
  'Successful': 'bg-success',
  'Unsuccessful': 'bg-gray-500',
};

const IncidentCard = ({ incident, isSelected, onSelect }) => {
  const statusColor = statusColorMap[incident.status] || 'bg-gray-400';

  return (
    <Card
      className={cn(
        'cursor-pointer transition-all duration-300 hover:border-primary hover:shadow-lg hover:-translate-y-1',
        isSelected ? 'border-primary ring-2 ring-primary' : 'border-border'
      )}
      onClick={() => onSelect(incident)}
    >
      <CardHeader className="flex-row items-center justify-between pb-2">
        <CardTitle className="text-sm font-bold text-primary">{incident.id.toUpperCase()}</CardTitle>
        <div className={cn('w-3 h-3 rounded-full', statusColor)}></div>
      </CardHeader>
      <CardContent>
        <div className="space-y-3 text-sm">
          <div className="flex items-center gap-2">
            <User className="w-4 h-4 text-text-secondary" />
            <span className="font-medium text-text truncate">{incident.touristName}</span>
          </div>
          <div className="flex items-center gap-2">
            <MapPin className="w-4 h-4 text-text-secondary" />
            <span className="text-text-secondary truncate">{incident.locationTag}</span>
          </div>
          <div className="flex items-center gap-2">
            <Calendar className="w-4 h-4 text-text-secondary" />
            <span className="text-text-secondary">{new Date(incident.dateIssued).toLocaleDateString()}</span>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default IncidentCard;
