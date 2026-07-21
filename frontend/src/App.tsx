import { BrowserRouter, Route, Routes } from 'react-router-dom'
import { AppLayout } from './layouts/AppLayout'
import { DashboardPage } from './pages/DashboardPage'
import { IncidentDetailPage } from './pages/IncidentDetailPage'
import { IncidentsPage } from './pages/IncidentsPage'
import { InvestigationPage } from './pages/InvestigationPage'
import { SettingsPage } from './pages/SettingsPage'
import './App.css'

export default function App() {
  return <BrowserRouter><AppLayout><Routes>
    <Route path="/" element={<DashboardPage />} />
    <Route path="/incidents" element={<IncidentsPage />} />
    <Route path="/incidents/:id" element={<IncidentDetailPage />} />
    <Route path="/investigation" element={<InvestigationPage />} />
    <Route path="/settings" element={<SettingsPage />} />
  </Routes></AppLayout></BrowserRouter>
}
