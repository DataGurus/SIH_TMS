import { useState, useMemo } from 'react';
import { incidents as mockIncidents } from '../data/mockData';
import { columns } from '../components/incidents/columns';
import { DataTable } from '../components/incidents/DataTable';
import QuickActions from '../components/incidents/QuickActions';
import IncidentDetails from '../components/incidents/IncidentDetails';
import { AnimatePresence, motion } from 'framer-motion';
import { Calendar as CalendarIcon, Filter } from 'lucide-react';
import { format } from 'date-fns';
import { cn } from '../lib/utils';
import { Button } from '../components/ui/Button';
import { Calendar } from '../components/ui/Calendar';
import { Popover, PopoverContent, PopoverTrigger } from '../components/ui/Popover';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '../components/ui/Select';

const incidentStatuses = ['Filed Fir', 'Not filed FIr', 'Completed', 'Successful', 'Unsuccessful'];

const IncidentsPage = () => {
  const [selectedIncident, setSelectedIncident] = useState(null);
  const [date, setDate] = useState();
  const [status, setStatus] = useState('all');

  const filteredIncidents = useMemo(() => {
    return mockIncidents.filter(incident => {
      const dateMatch = date ? format(new Date(incident.dateIssued), 'yyyy-MM-dd') === format(date, 'yyyy-MM-dd') : true;
      const statusMatch = status === 'all' ? true : incident.status === status;
      return dateMatch && statusMatch;
    });
  }, [date, status]);

  return (
    <div className="p-8 space-y-6 h-full flex flex-col">
      <header>
        <h1 className="text-3xl font-bold text-text">Incidents Management</h1>
        <p className="text-text-secondary">Track, manage, and resolve incidents in real-time.</p>
      </header>

      <div className="flex-grow grid grid-cols-1 lg:grid-cols-3 gap-6 items-start">
        <div className={cn("col-span-1 lg:col-span-3 transition-all duration-300", { 'lg:col-span-2': selectedIncident })}>
          <div className="bg-surface border border-border rounded-lg p-4 mb-6 flex items-center gap-4">
            <Filter size={20} className="text-text-secondary" />
            <h3 className="text-lg font-semibold">Filters</h3>
            <div className="w-px h-8 bg-border mx-2"></div>
            <Popover>
              <PopoverTrigger asChild>
                <Button
                  variant={"outline"}
                  className={cn(
                    "w-[280px] justify-start text-left font-normal",
                    !date && "text-text-secondary"
                  )}
                >
                  <CalendarIcon className="mr-2 h-4 w-4" />
                  {date ? format(date, "PPP") : <span>Pick a date</span>}
                </Button>
              </PopoverTrigger>
              <PopoverContent className="w-auto p-0 bg-surface border-border">
                <Calendar
                  mode="single"
                  selected={date}
                  onSelect={setDate}
                  initialFocus
                />
              </PopoverContent>
            </Popover>

            <Select value={status} onValueChange={setStatus}>
              <SelectTrigger className="w-[280px]">
                <SelectValue placeholder="Filter by status..." />
              </SelectTrigger>
              <SelectContent className="bg-surface border-border">
                <SelectItem value="all">All Statuses</SelectItem>
                {incidentStatuses.map(s => <SelectItem key={s} value={s}>{s}</SelectItem>)}
              </SelectContent>
            </Select>
            
            {(date || status !== 'all') && (
                <Button variant="ghost" onClick={() => { setDate(undefined); setStatus('all'); }}>
                    Clear Filters
                </Button>
            )}
          </div>

          <DataTable columns={columns} data={filteredIncidents} onRowSelectionChange={setSelectedIncident} />
        </div>

        <AnimatePresence>
          {selectedIncident && (
            <motion.div
              className="col-span-1 space-y-6"
              initial={{ opacity: 0, x: 50 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: 50 }}
              transition={{ duration: 0.3 }}
            >
              <QuickActions />
              <IncidentDetails incident={selectedIncident} />
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
};

export default IncidentsPage;
