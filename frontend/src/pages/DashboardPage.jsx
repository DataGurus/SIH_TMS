const DashboardPage = () => {
  return (
    <div className="relative h-full w-full rounded-lg overflow-hidden border border-border shadow-2xl shadow-primary/10">
      {/* Background Map Image */}
      <img
        src="https://images.pexels.com/photos/1581554/pexels-photo-1581554.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2"
        alt="Map Placeholder"
        className="absolute inset-0 w-full h-full object-cover opacity-20"
      />
      {/* Overlay Gradient */}
      <div className="absolute inset-0 bg-gradient-to-t from-background via-background/60 to-transparent"></div>
      
      {/* Placeholder Content */}
      <div className="relative h-full flex items-center justify-center">
        <div className="text-center p-10 bg-surface/70 backdrop-blur-md rounded-xl border border-border">
          <h1 className="text-4xl font-bold text-primary mb-3">Live Map View</h1>
          <p className="text-textSecondary max-w-md">
            Real-time tracking of units, incidents, and geo-fenced zones will be displayed on this interactive map.
          </p>
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;
