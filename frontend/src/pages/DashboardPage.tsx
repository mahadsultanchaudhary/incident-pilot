import { ArrowUpRight, Clock3, ShieldAlert, Siren } from 'lucide-react'
import { Link } from 'react-router-dom'
import { ErrorChart, FrequencyChart } from '../components/Charts'
import { LogViewer } from '../components/LogViewer'
import { LoadingState } from '../components/LoadingState'
import { MetricCard } from '../components/MetricCard'
import { Panel } from '../components/Panel'
import { StatusBadge } from '../components/StatusBadge'
import { useAsync } from '../hooks/useAsync'
import { incidentService } from '../services/incidentService'
import { relativeTime } from '../utils/format'

export function DashboardPage() {
  const { data, loading, error, reload } = useAsync(incidentService.dashboard)
  if (loading) return <LoadingState />
  if (!data) return <div className="api-error"><strong>Live telemetry unavailable</strong><p>{error}</p><button className="button primary" onClick={() => void reload()}>Retry connection</button></div>
  return <div className="dashboard"><div className="page-heading"><div><p>Production environment</p><h2>System signal at a glance</h2></div><button className="button secondary" onClick={() => void reload()}>Refresh data</button></div><div className="metrics-grid"><MetricCard label="Open incidents" value={data.open_incidents} detail="Active investigations" icon={Siren} tone="red" /><MetricCard label="Critical impact" value={data.critical_incidents} detail="Requires immediate action" icon={ShieldAlert} tone="orange" /><MetricCard label="Events processed" value={data.events_processed.toLocaleString()} detail="Last 24 hours" icon={ArrowUpRight} tone="blue" /><MetricCard label="Mean time to detect" value={data.mean_time_to_detect} detail="17% faster than last week" icon={Clock3} tone="green" /></div><div className="dashboard-grid primary-grid"><Panel title="Incident frequency" action={<span className="subtle">Last 7 days</span>}><FrequencyChart data={data.frequency} /></Panel><Panel title="Error distribution"><ErrorChart data={data.error_distribution} /></Panel><Panel title="Service health" className="health-panel"><div className="service-list">{data.service_health.map((service) => <div className="service-row" key={service.service}><span className={`health-dot ${service.status}`} /><strong>{service.service}</strong><span>{service.availability.toFixed(2)}%</span><small>{service.latency}ms</small></div>)}</div></Panel></div><div className="dashboard-grid lower-grid"><Panel title="Live log stream" action={<span className="live-label"><i /> Live</span>}><LogViewer logs={data.logs} /></Panel><Panel title="Recent incidents" action={<Link to="/incidents" className="text-action">View all</Link>}><div className="incident-list">{data.incidents.map((incident) => <Link className="incident-row" to={`/incidents/${incident.id}`} key={incident.id}><div><StatusBadge value={incident.severity} /><strong>{incident.title}</strong><span>{incident.service} · {relativeTime(incident.last_seen)}</span></div><div className="incident-right"><b>{incident.occurrence_count} events</b><ArrowUpRight size={16} /></div></Link>)}</div></Panel></div></div>
}
