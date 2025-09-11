import { MapContainer, TileLayer, Circle, Popup, useMap } from 'react-leaflet';

const ZONE_COLORS = {
  'safe': { color: '#10b981', fillColor: '#10b981' },
  'high-risk': { color: '#ef4444', fillColor: '#ef4444' },
  'no-entry': { color: '#a3a3a3', fillColor: '#a3a3a3' },
};

const ChangeView = ({ center, zoom }) => {
  const map = useMap();
  map.setView(center, zoom);
  return null;
};

const MapComponent = ({ zones, selectedZone, onSelectZone }) => {
  const parisCenter = [48.8566, 2.3522];

  return (
    <MapContainer center={parisCenter} zoom={12} scrollWheelZoom={true} style={{ height: '100%', width: '100%', background: '#171717' }}>
      {selectedZone && <ChangeView center={selectedZone.center} zoom={14} />}
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
        url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
      />
      {zones.map((zone) => {
        const { color, fillColor } = ZONE_COLORS[zone.type];
        const isSelected = selectedZone?.id === zone.id;
        return (
          <Circle
            key={zone.id}
            center={zone.center}
            radius={zone.radius}
            pathOptions={{
              color: color,
              fillColor: fillColor,
              fillOpacity: isSelected ? 0.5 : 0.2,
              weight: isSelected ? 3 : 1,
            }}
            eventHandlers={{
              click: () => onSelectZone(zone),
            }}
          >
            <Popup>
              <div className="text-text-primary">
                <h4 className="font-bold">{zone.name}</h4>
                <p>Status: <span className="capitalize">{zone.type.replace('-', ' ')}</span></p>
                <p>Radius: {zone.radius}m</p>
              </div>
            </Popup>
          </Circle>
        );
      })}
    </MapContainer>
  );
};

export default MapComponent;
