import { Zap } from 'lucide-react';
import { realTimeAssignments, units } from '../../data/mockData';
import { formatDistanceToNow } from 'date-fns';

const RealTimeAssignments = () => {
  return (
    <div className="bg-surface border border-border rounded-lg p-4 h-full">
      <div className="flex items-center gap-3 mb-4">
        <Zap className="text-primary" />
        <h3 className="text-lg font-semibold text-text">Real-time Assignments</h3>
      </div>
      <div className="space-y-3">
        {realTimeAssignments.map((assignment) => {
          const unit = units.find(u => u.id === assignment.unitId);
          return (
            <div key={assignment.unitId} className="flex items-center justify-between text-sm">
              <div className="flex items-center gap-2">
                <img src={unit?.avatar} alt={unit?.unitHead} className="h-6 w-6 rounded-full" />
                <p><span className="font-bold">{assignment.unitId}</span> assigned to <span className="font-bold">{assignment.incidentId}</span></p>
              </div>
              <p className="text-text-secondary">{formatDistanceToNow(assignment.timestamp, { addSuffix: true })}</p>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default RealTimeAssignments;
