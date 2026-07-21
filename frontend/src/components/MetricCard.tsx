import type { LucideIcon } from 'lucide-react'

export function MetricCard({ label, value, detail, icon: Icon, tone = 'blue' }: { label: string; value: string | number; detail: string; icon: LucideIcon; tone?: string }) {
  return <article className="metric-card"><div className={`metric-icon ${tone}`}><Icon size={19} /></div><div><p className="metric-label">{label}</p><strong>{value}</strong><span className="metric-detail">{detail}</span></div></article>
}
