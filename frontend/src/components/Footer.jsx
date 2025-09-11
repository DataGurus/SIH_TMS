const StatItem = ({ label, value }) => (
  <div>
    <p className="text-xs text-text-secondary uppercase tracking-wider">{label}</p>
    <p className="text-xl font-semibold text-text">{value}</p>
  </div>
);

const Footer = () => {
  return (
    <footer className="border-t border-border bg-surface/80 backdrop-blur-sm z-10">
      <div className="mx-auto px-8 py-3 flex items-center justify-between">
        {/* Left Side: Stats */}
        <div className="flex items-center gap-x-8">
          <StatItem label="Active Tourists" value="1,287" />
          <div className="w-px h-8 bg-border"></div>
          <StatItem label="Open Incidents" value="14" />
          <div className="w-px h-8 bg-border"></div>
          <StatItem label="Avg. Response Time" value="6.2 min" />
          <div className="w-px h-8 bg-border"></div>
          <StatItem label="Overall Safety Score" value="98.5%" />
        </div>

        {/* Right Side: Status Indicator */}
        <div className="flex items-center gap-4">
          <div className="text-right">
            <span className="text-sm font-medium text-success">System Status</span>
            <p className="text-xs text-text-secondary">All Systems Operational</p>
          </div>
          <div className="w-24 h-2 bg-success/20 rounded-full overflow-hidden">
             <div 
               className="h-full bg-success rounded-full shadow-[0_0_8px_theme(colors.success)]" 
               style={{ width: '98.5%' }} // This can be driven by the safety score
             ></div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
