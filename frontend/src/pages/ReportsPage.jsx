import { useState, useMemo } from 'react';
import { incidents } from '../data/mockData';
import IncidentCard from '../components/reports/IncidentCard';
import IncidentDetailsPanel from '../components/reports/IncidentDetailsPanel';
import Pagination from '../components/reports/Pagination';
import { FileBarChart, Search, Filter } from 'lucide-react';
import { Button } from '../components/ui/Button';

const CARDS_PER_PAGE = 8;

const ReportsPage = () => {
  const [selectedIncident, setSelectedIncident] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);

  const totalPages = Math.ceil(incidents.length / CARDS_PER_PAGE);

  const currentIncidents = useMemo(() => {
    const startIndex = (currentPage - 1) * CARDS_PER_PAGE;
    const endIndex = startIndex + CARDS_PER_PAGE;
    return incidents.slice(startIndex, endIndex);
  }, [currentPage]);

  const handleSelectIncident = (incident) => {
    if (selectedIncident?.id === incident.id) {
      setSelectedIncident(null); // Deselect if clicking the same card
    } else {
      setSelectedIncident(incident);
    }
  };

  return (
    <div className="flex h-full">
      <div className="flex-1 flex flex-col p-4">
        <header className="mb-6">
          <h1 className="text-3xl font-bold text-text flex items-center gap-3">
            <FileBarChart className="w-8 h-8 text-primary" />
            Reports & FIRs
          </h1>
          <p className="text-text-secondary mt-1">
            Review and manage all filed incidents and reports.
          </p>
        </header>

        <div className="flex items-center justify-between mb-6">
            {/* Search and Filter can be implemented here */}
            <div></div>
            <div className="flex items-center gap-2">
                <Button variant="outline">
                    <Filter className="w-4 h-4 mr-2" />
                    Filter
                </Button>
            </div>
        </div>

        <main className="flex-1">
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {currentIncidents.map((incident) => (
              <IncidentCard
                key={incident.id}
                incident={incident}
                isSelected={selectedIncident?.id === incident.id}
                onSelect={handleSelectIncident}
              />
            ))}
          </div>
        </main>

        {totalPages > 1 && (
          <Pagination
            currentPage={currentPage}
            totalPages={totalPages}
            onPageChange={setCurrentPage}
          />
        )}
      </div>
      {selectedIncident && (
        <IncidentDetailsPanel
          incident={selectedIncident}
          onClose={() => setSelectedIncident(null)}
        />
      )}
    </div>
  );
};

export default ReportsPage;
