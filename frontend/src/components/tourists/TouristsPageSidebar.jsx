import ActiveUnits from '../units/ActiveUnits';
import ActiveTouristsWidget from './ActiveTouristsWidget';
import LocationRankingWidget from './LocationRankingWidget';
import TouristActions from './TouristActions';

const TouristsPageSidebar = ({ selectedTourist }) => {
  return (
    <aside className="w-full lg:w-96 flex-shrink-0 space-y-6">
      {selectedTourist ? (
        <TouristActions tourist={selectedTourist} />
      ) : (
        <div className="bg-surface border border-border rounded-lg p-4 text-center">
            <p className="text-text-secondary text-sm">Select a tourist to see actions.</p>
        </div>
      )}
      <ActiveTouristsWidget />
      <ActiveUnits />
      <LocationRankingWidget />
    </aside>
  );
};

export default TouristsPageSidebar;
