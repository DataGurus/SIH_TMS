import { X, User, MapPin, Calendar, FileText, Link as LinkIcon, Edit, Shield, FileUp, Trash2 } from 'lucide-react';
import { Button } from '../ui/Button';

const IncidentDetailsPanel = ({ incident, onClose }) => {
  return (
    <div className="w-[400px] bg-surface border-l border-border flex flex-col h-full flex-shrink-0">
      <div className="p-6 border-b border-border flex items-center justify-between">
        <h3 className="text-lg font-bold text-text">Incident Details</h3>
        <Button variant="ghost" size="icon" onClick={onClose}>
          <X className="w-5 h-5" />
        </Button>
      </div>
      <div className="flex-1 p-6 overflow-y-auto space-y-6">
        <div className="flex items-center gap-4">
          <img src={incident.touristAvatar} alt={incident.touristName} className="w-16 h-16 rounded-full object-cover border-2 border-primary" />
          <div>
            <p className="font-bold text-text">{incident.touristName}</p>
            <p className="text-sm text-text-secondary">Tourist ID: {incident.touristId.slice(0, 8)}</p>
          </div>
        </div>

        <div>
          <h4 className="font-semibold text-text mb-2">Summary</h4>
          <div className="space-y-2 text-sm text-text-secondary">
            <p><strong className="text-text-secondary font-medium">Status:</strong> {incident.status}</p>
            <p><strong className="text-text-secondary font-medium">Location:</strong> {incident.locationTag}</p>
            <p><strong className="text-text-secondary font-medium">Date:</strong> {new Date(incident.dateIssued).toLocaleString()}</p>
          </div>
        </div>

        <div>
          <h4 className="font-semibold text-text mb-2">Description</h4>
          <p className="text-sm text-text-secondary bg-background p-3 rounded-md">{incident.details.description}</p>
        </div>

        <div>
          <h4 className="font-semibold text-text mb-2">Evidence</h4>
          {incident.details.evidence.length > 0 ? (
            <ul className="space-y-2">
              {incident.details.evidence.map((e, i) => (
                <li key={i} className="flex items-center gap-2 text-sm text-primary hover:underline">
                  <LinkIcon className="w-4 h-4" />
                  <a href={e.url} target="_blank" rel="noopener noreferrer">
                    {e.type.charAt(0).toUpperCase() + e.type.slice(1)} Evidence #{i + 1}
                  </a>
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-sm text-text-secondary italic">No evidence submitted.</p>
          )}
        </div>
      </div>
      <div className="p-6 border-t border-border grid grid-cols-2 gap-3">
        <Button variant="outline"><Edit className="w-4 h-4 mr-2" /> Update Status</Button>
        <Button variant="outline"><Shield className="w-4 h-4 mr-2" /> Assign Unit</Button>
        <Button variant="outline"><FileUp className="w-4 h-4 mr-2" /> Export PDF</Button>
        <Button variant="destructive"><Trash2 className="w-4 h-4 mr-2" /> Close Case</Button>
      </div>
    </div>
  );
};

export default IncidentDetailsPanel;
