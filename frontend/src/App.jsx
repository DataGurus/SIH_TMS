import { Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import DashboardPage from './pages/DashboardPage';
import IncidentsPage from './pages/IncidentsPage';
import UnitsPage from './pages/UnitsPage';
import TouristsPage from './pages/TouristsPage';
import ZonesPage from './pages/ZonesPage';
import ReportsPage from './pages/ReportsPage';

function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<DashboardPage />} />
        <Route path="incidents" element={<IncidentsPage />} />
        <Route path="units" element={<UnitsPage />} />
        <Route path="tourists" element={<TouristsPage />} />
        <Route path="zones" element={<ZonesPage />} />
        <Route path="reports" element={<ReportsPage />} />
      </Route>
    </Routes>
  );
}

export default App;
