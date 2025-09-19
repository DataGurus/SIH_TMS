import { AlertTriangle, FileText, ShieldCheck } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/Card';
import { Button } from '../ui/Button';

const QuickActions = () => {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Quick Actions</CardTitle>
      </CardHeader>
      <CardContent className="flex flex-col gap-3">
        <Button variant="secondary" className="justify-start gap-3">
          <AlertTriangle size={16} />
          <span>Dispatch Units</span>
        </Button>
        <Button variant="secondary" className="justify-start gap-3">
          <FileText size={16} />
          <span>File e-FIR</span>
        </Button>
        <Button variant="secondary" className="justify-start gap-3">
          <ShieldCheck size={16} />
          <span>Close Case</span>
        </Button>
      </CardContent>
    </Card>
  );
};

export default QuickActions;
