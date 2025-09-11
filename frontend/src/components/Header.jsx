import { Bell, ChevronDown } from 'lucide-react';

const Header = () => {
  return (
    <header className="bg-surface h-20 flex items-center justify-end px-8 border-b border-border">
      {/* Right side controls */}
      <div className="flex items-center space-x-6">
        <div className="relative">
          <Bell className="h-6 w-6 text-text-secondary hover:text-text cursor-pointer transition-colors" />
          <span className="absolute -top-1 -right-1 h-2.5 w-2.5 bg-accent rounded-full border-2 border-surface"></span>
        </div>
        
        <div className="h-10 w-px bg-border"></div>

        <div className="flex items-center space-x-3 cursor-pointer">
          <img 
            src="https://i.pravatar.cc/150?u=admin" 
            alt="Admin"
            className="h-10 w-10 rounded-full object-cover border-2 border-primary/50"
          />
          <div>
            <p className="font-semibold text-sm">Admin User</p>
            <p className="text-xs text-text-secondary">Super Admin</p>
          </div>
          <ChevronDown className="h-4 w-4 text-text-secondary" />
        </div>
      </div>
    </header>
  );
};

export default Header;
