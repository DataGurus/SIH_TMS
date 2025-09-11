import { useState, useEffect } from 'react';
import { Input } from '../ui/Input';
import { Label } from '../ui/Label';
import { Button } from '../ui/Button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../ui/Select';

const ZoneEditor = ({ zone, onUpdate }) => {
  const [name, setName] = useState(zone.name);
  const [radius, setRadius] = useState(zone.radius);
  const [type, setType] = useState(zone.type);

  useEffect(() => {
    setName(zone.name);
    setRadius(zone.radius);
    setType(zone.type);
  }, [zone]);

  const handleSaveChanges = () => {
    onUpdate({
      ...zone,
      name,
      radius,
      type,
    });
  };

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        handleSaveChanges();
      }}
      className="space-y-4"
    >
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="space-y-2">
          <Label htmlFor="zone-name">Zone Name</Label>
          <Input id="zone-name" value={name} onChange={(e) => setName(e.target.value)} />
        </div>
        <div className="space-y-2">
          <Label htmlFor="zone-radius">Radius (meters)</Label>
          <Input
            id="zone-radius"
            type="number"
            value={radius}
            onChange={(e) => setRadius(Number(e.target.value))}
          />
        </div>
        <div className="space-y-2">
          <Label htmlFor="zone-type">Zone Type</Label>
          <Select value={type} onValueChange={(value) => setType(value)}>
            <SelectTrigger id="zone-type">
              <SelectValue placeholder="Select type" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="safe">Safe</SelectItem>
              <SelectItem value="high-risk">High Risk</SelectItem>
              <SelectItem value="no-entry">No Entry</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </div>
      <div className="flex justify-end">
        <Button type="submit">Save Changes</Button>
      </div>
    </form>
  );
};

export default ZoneEditor;
