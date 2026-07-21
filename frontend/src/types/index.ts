export type Severity = 'critical' | 'high' | 'medium' | 'low'
export type IncidentStatus = 'investigating' | 'monitoring' | 'resolved'

export interface Incident {
  id: number
  title: string
  severity: Severity
  status: IncidentStatus
  service: string
  summary: string
  first_seen: string
  last_seen: string
  occurrence_count: number
  root_cause_confidence: number
}

export interface LogEvent {
  id: number
  timestamp: string
  level: string
  service: string
  message: string
  endpoint?: string
  request_id?: string
  correlation_id?: string
  status_code?: number
  latency_ms?: number
  trace?: string
}

export interface DashboardData {
  open_incidents: number
  critical_incidents: number
  events_processed: number
  mean_time_to_detect: string
  service_health: { service: string; status: string; availability: number; latency: number }[]
  logs: LogEvent[]
  incidents: Incident[]
  frequency: { day: string; incidents: number }[]
  error_distribution: { name: string; value: number }[]
}

export interface IncidentDetail {
  incident: Incident
  events: LogEvent[]
  evidence: { id: number; assertion: string; relevance: number; created_at: string }[]
  stack_trace: { exception?: string; message?: string; frames: { file: string; line: number; function: string }[] }
}

export interface Analysis {
  incident_id: number
  executive_summary: string
  timeline: { timestamp: string; event: string; level: string }[]
  root_cause: string
  confidence: number
  affected_services: string[]
  suggested_fixes: string[]
  next_steps: string[]
  evidence: { assertion: string; relevance: number }[]
}
