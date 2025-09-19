import { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { 
  LayoutDashboard, 
  CalendarCheck, 
  MapPin, 
  Users, 
  FileBarChart, 
  ChevronLeft, 
  ChevronRight,
  Globe,
	Car
} from 'lucide-react';
import { cn } from '../lib/utils';

const navItems = [
  { name: 'Dashboard', icon: LayoutDashboard, path: '/' },
  { name: 'Incidents', icon: CalendarCheck, path: '/incidents' },
  { name: 'Units', icon: Car, path: '/units' },
  { name: 'Tourists', icon: Users, path: '/tourists' },
  { name: 'Zones and Geo-Fences', icon: MapPin, path: '/zones' },
  { name: 'Reports and FIRs', icon: FileBarChart, path: '/reports' },
];

const Sidebar = () => {
  const [isCollapsed, setIsCollapsed] = useState(false);
  const location = useLocation();

  return (
    <aside className={cn(
      "relative bg-surface h-screen flex flex-col border-r border-border transition-all duration-300 ease-in-out z-10",
      isCollapsed ? "w-20" : "w-64"
    )}>
      <div className="flex items-center h-20 border-b border-border p-4 shrink-0">
        <Globe className="text-primary h-8 w-8" />
        <span className={cn("ml-3 text-xl font-bold", isCollapsed && "hidden")}>VoyageAdmin</span>
      </div>

      <nav className="flex-grow px-4 py-6 space-y-2">
        {navItems.map((item) => (
          <Link
            key={item.name}
            to={item.path}
            className={cn(
              "flex items-center py-3 px-4 rounded-lg text-textSecondary hover:bg-border hover:text-text transition-colors relative",
              location.pathname === item.path && "bg-primary/10 text-primary font-medium"
            )}
          >
            {location.pathname === item.path && (
              <span className="absolute left-0 top-1/2 -translate-y-1/2 h-6 w-1 bg-primary rounded-r-full"></span>
            )}
            <item.icon className="h-5 w-5 shrink-0" />
            <span className={cn("ml-4", isCollapsed && "hidden")}>{item.name}</span>
          </Link>
        ))}
      </nav>

      <div className="p-4 border-t border-border">
        <button 
          onClick={() => setIsCollapsed(!isCollapsed)}
          className="w-full flex items-center justify-center py-3 px-4 rounded-lg text-textSecondary hover:bg-border hover:text-text transition-colors"
        >
          {isCollapsed ? <ChevronRight className="h-5 w-5" /> : <ChevronLeft className="h-5 w-5" />}
          <span className={cn("ml-4", isCollapsed && "hidden")}>Collapse</span>
        </button>
      </div>
    </aside>
  );
};

export default Sidebar;
