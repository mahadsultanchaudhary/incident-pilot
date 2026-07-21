import { api } from '../api/client'
import type { Analysis, DashboardData, Incident, IncidentDetail } from '../types'

export const incidentService = {
  dashboard: () => api.get<DashboardData>('/dashboard').then((res) => res.data),
  list: () => api.get<Incident[]>('/incidents').then((res) => res.data),
  detail: (id: number) => api.get<IncidentDetail>(`/incidents/${id}`).then((res) => res.data),
  analyze: (incidentId: number) => api.post<Analysis>('/analyze', { incident_id: incidentId }).then((res) => res.data),
  chat: (incidentId: number, question: string) => api.post<{ answer: string }>('/chat', { incident_id: incidentId, question }).then((res) => res.data),
  postmortem: (incidentId: number) => api.post<{ markdown: string }>('/postmortem', { incident_id: incidentId }).then((res) => res.data),
}
