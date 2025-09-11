import { useState, useMemo } from 'react';
import { units as mockUnits } from '../data/mockData';
import { columns } from '../components/units/columns';
import { DataTable } from '../components/incidents/DataTable';
import RealTimeAssignments from '../components/units/RealTimeAssignments';
import ActiveUnits from '../components/units/ActiveUnits';
import UnitQuickActions from '../components/units/UnitQuickActions';
import { AnimatePresence, motion } from 'framer-motion';
import { Filter, Search } from 'lucide-react';
import { Input } from '../components/ui/Input';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '../components/ui/Select';
import { Button } from '../components/ui/Button';

const unitTypes = ['Patrol Car', 'Motorcycle', 'Foot Patrol', 'K-9 Unit'];
const unitStatuses = ['Assigned', 'Unassigned', 'Inactive'];

const UnitsPage = () => {
  const [selectedUnit, setSelectedUnit] = useState(null);
  const [locationFilter, setLocationFilter] = useState('');
  const [typeFilter, setTypeFilter] = useState('all');
  const [statusFilter, setStatusFilter] = useState('all');

  const filteredUnits = useMemo(() => {
    return mockUnits.filter(unit => {
      const locationMatch = locationFilter === '' ? true : unit.locationTag.toLowerCase().includes(locationFilter.toLowerCase());
      const typeMatch = typeFilter === 'all' ? true : unit.type === typeFilter;
      const statusMatch = statusFilter === 'all' ? true : unit.status === statusFilter;
      return locationMatch && typeMatch && statusMatch;
    });
  }, [locationFilter, typeFilter, statusFilter]);
  
  const clearFilters = () => {
    setLocationFilter('');
    setTypeFilter('all');
    setStatusFilter('all');
  };

  const hasActiveFilters = locationFilter !== '' || typeFilter !== 'all' || statusFilter !== 'all';

  return (
    <div className="p-8 space-y-6 h-full flex flex-col">
      <header>
        <h1 className="text-3xl font-bold text-text">Unit Management</h1>
        <p className="text-text-secondary">Monitor, filter, and manage all operational units.</p>
      </header>

      <div className="flex-grow grid grid-cols-1 lg:grid-cols-3 gap-6 items-start">
        <div className="col-span-1 lg:col-span-2 space-y-6">
          <div className="bg-surface border border-border rounded-lg p-4 flex items-center gap-4 flex-wrap">
            <Filter size={20} className="text-text-secondary" />
            <h3 className="text-lg font-semibold">Filters</h3>
            <div className="w-px h-8 bg-border mx-2 hidden sm:block"></div>
            
            <div className="relative">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-text-secondary" />
                <Input 
                    placeholder="Filter by location..." 
                    value={locationFilter}
                    onChange={(e) => setLocationFilter(e.target.value)}
                    className="pl-10 w-[200px]"
                />
            </div>

            <Select value={typeFilter} onValueChange={setTypeFilter}>
              <SelectTrigger className="w-[180px]">
                <SelectValue placeholder="Filter by type..." />
              </SelectTrigger>
              <SelectContent className="bg-surface border-border">
                <SelectItem value="all">All Types</SelectItem>
                {unitTypes.map(s => <SelectItem key={s} value={s}>{s}</SelectItem>)}
              </SelectContent>
            </Select>

            <Select value={statusFilter} onValueChange={setStatusFilter}>
              <SelectTrigger className="w-[180px]">
                <SelectValue placeholder="Filter by status..." />
              </SelectTrigger>
              <SelectContent className="bg-surface border-border">
                <SelectItem value="all">All Statuses</SelectItem>
                {unitStatuses.map(s => <SelectItem key={s} value={s}>{s}</SelectItem>)}
              </SelectContent>
            </Select>
            
            {hasActiveFilters && (
                <Button variant="ghost" onClick={clearFilters}>
                    Clear Filters
                </Button>
            )}
          </div>

          <DataTable columns={columns} data={filteredUnits} onRowSelectionChange={setSelectedUnit} />
        </div>

        <div className="col-span-1 space-y-6">
            <RealTimeAssignments />
            <ActiveUnits />
            <AnimatePresence>
            {selectedUnit && (
                <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: 20 }}
                transition={{ duration: 0.2 }}
                >
                    <UnitQuickActions unit={selectedUnit} />
                </motion.div>
            )}
            </AnimatePresence>
        </div>
      </div>
    </div>
  );
};

export default UnitsPage;
