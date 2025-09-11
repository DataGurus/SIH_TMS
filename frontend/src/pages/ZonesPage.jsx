import { useState } from 'react';
import { zones as initialZones } from '../data/mockData';
import MapComponent from '../components/zones/MapComponent';
import ZoneEditor from '../components/zones/ZoneEditor';
import FlaggedPlacesWidget from '../components/zones/FlaggedPlacesWidget';

const ZonesPage = () => {
  const [zones, setZones] = useState(initialZones);
  const [selectedZone, setSelectedZone] = useState(zones[0] || null);

  const handleUpdateZone = (updatedZone) => {
    setZones(zones.map((z) => (z.id === updatedZone.id ? updatedZone : z)));
    setSelectedZone(updatedZone);
  };

  const handleDeleteZone = (zoneId) => {
    setZones((prevZones) => prevZones.filter((z) => z.id !== zoneId));
    if (selectedZone?.id === zoneId) {
      setSelectedZone(null);
    }
  };

  return (
    <div className="flex h-full gap-8">
      <div className="flex-1 flex flex-col gap-8">
        <div className="flex-1 rounded-lg overflow-hidden border border-border min-h-[400px]">
          <MapComponent zones={zones} onSelectZone={setSelectedZone} selectedZone={selectedZone} />
        </div>
        <div className="bg-surface border border-border rounded-lg p-6">
          <h2 className="text-xl font-bold mb-4 text-text">Zone Editor</h2>
          {selectedZone ? (
            <ZoneEditor zone={selectedZone} onUpdate={handleUpdateZone} />
          ) : (
            <p className="text-text-secondary">Select a zone on the map to edit its details.</p>
          )}
        </div>
      </div>
      <aside className="w-96 flex-shrink-0">
        <FlaggedPlacesWidget zones={zones} onSelectZone={setSelectedZone} onDeleteZone={handleDeleteZone} />
      </aside>
    </div>
  );
};

export default ZonesPage;
