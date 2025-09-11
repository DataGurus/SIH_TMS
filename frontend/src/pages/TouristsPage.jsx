import { useState, useMemo } from 'react';
import { tourists as allTourists } from '../data/mockData';
import { columns } from '../components/tourists/columns';
import { TouristsTable } from '../components/tourists/TouristsTable';
import TouristsPageSidebar from '../components/tourists/TouristsPageSidebar';
import { Button } from '../components/ui/Button';
import { cn } from '../lib/utils';

const TouristsPage = () => {
  const [tourists, setTourists] = useState(allTourists);
  const [selectedTourist, setSelectedTourist] = useState(null);
  const [activeFilter, setActiveFilter] = useState('all');

  const handleRowSelection = (selectedRows) => {
    // For this UI, we only care about the first selected tourist for the action panel
    setSelectedTourist(selectedRows.length > 0 ? selectedRows[0] : null);
  };

  const handleFilterChange = (filter) => {
    setActiveFilter(filter);
  };

  const filteredTourists = useMemo(() => {
    let sortedTourists = [...allTourists];
    switch (activeFilter) {
      case 'lessSafe':
        return sortedTourists.sort((a, b) => a.safetyScore - b.safetyScore);
      case 'activeIncident':
        return sortedTourists.filter(t => t.incidentId !== null).sort((a, b) => a.safetyScore - b.safetyScore);
      case 'restrictedZone':
        return sortedTourists.filter(t => t.isNearRestrictedZone);
      case 'all':
      default:
        return allTourists;
    }
  }, [activeFilter]);

  return (
    <div className="flex flex-col lg:flex-row gap-6 p-6 bg-background text-text">
      <main className="flex-1">
        <div className="mb-4">
          <h1 className="text-2xl font-bold mb-2">Active Tourists</h1>
          <p className="text-text-secondary">Monitor and manage all active tourists in real-time.</p>
        </div>
        <div className="flex items-center gap-2 mb-4">
            <Button 
                variant={activeFilter === 'all' ? 'default' : 'outline'} 
                onClick={() => handleFilterChange('all')}
                className={cn(activeFilter !== 'all' && "text-text-secondary")}
            >
                All Tourists
            </Button>
            <Button 
                variant={activeFilter === 'lessSafe' ? 'default' : 'outline'} 
                onClick={() => handleFilterChange('lessSafe')}
                className={cn(activeFilter !== 'lessSafe' && "text-text-secondary")}
            >
                Less Safe First
            </Button>
            <Button 
                variant={activeFilter === 'activeIncident' ? 'default' : 'outline'} 
                onClick={() => handleFilterChange('activeIncident')}
                className={cn(activeFilter !== 'activeIncident' && "text-text-secondary")}
            >
                Active Incident First
            </Button>
            <Button 
                variant={activeFilter === 'restrictedZone' ? 'default' : 'outline'} 
                onClick={() => handleFilterChange('restrictedZone')}
                className={cn(activeFilter !== 'restrictedZone' && "text-text-secondary")}
            >
                Near Restricted Zones
            </Button>
        </div>
        <TouristsTable columns={columns} data={filteredTourists} onRowSelectionChange={handleRowSelection} />
      </main>
      <TouristsPageSidebar selectedTourist={selectedTourist} />
    </div>
  );
};

export default TouristsPage;
