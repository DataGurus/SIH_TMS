import { MapPin, Paperclip, Users } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/Card';
import { Button } from '../ui/Button';
import { format } from 'date-fns';

const IncidentDetails = ({ incident }) => {
  return (
    <Card className="flex-grow">
      <CardHeader>
        <CardTitle>Incident Details</CardTitle>
      </CardHeader>
      <CardContent className="space-y-6 text-sm">
        <div className="flex items-start gap-4">
          <img src={incident.touristAvatar} alt={incident.touristName} className="h-12 w-12 rounded-full object-cover" />
          <div>
            <p className="font-semibold text-text">{incident.touristName}</p>
            <p className="text-text-secondary font-mono">{incident.touristId}</p>
          </div>
        </div>

        <div>
          <p className="font-semibold text-text-secondary mb-1">Description</p>
          <p className="text-text">{incident.details.description}</p>
        </div>

        <div className="grid grid-cols-2 gap-4">
            <div>
                <p className="font-semibold text-text-secondary mb-1">Date & Time</p>
                <p className="text-text">{format(new Date(incident.details.timestamp), 'MMM d, yyyy, h:mm a')}</p>
            </div>
            <div>
                <p className="font-semibold text-text-secondary mb-1">Location</p>
                <p className="text-text flex items-center gap-1"><MapPin size={14}/> {incident.locationTag}</p>
            </div>
        </div>

        <div>
          <p className="font-semibold text-text-secondary mb-1">Involved Parties</p>
          <div className="flex items-center gap-2 text-text">
            <Users size={16} />
            <span>{incident.details.involvedParties.join(', ')}</span>
          </div>
        </div>

        {incident.details.evidence.length > 0 && (
          <div>
            <p className="font-semibold text-text-secondary mb-1">Evidence</p>
            <div className="flex flex-col gap-2">
              {incident.details.evidence.map((item, index) => (
                <a
                  key={index}
                  href={item.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center gap-2 text-primary hover:underline"
                >
                  <Paperclip size={16} />
                  <span>{item.type.charAt(0).toUpperCase() + item.type.slice(1)} Attachment</span>
                </a>
              ))}
            </div>
          </div>
        )}

        <Button className="w-full mt-4">
          Generate Report
        </Button>
      </CardContent>
    </Card>
  );
};

export default IncidentDetails;
