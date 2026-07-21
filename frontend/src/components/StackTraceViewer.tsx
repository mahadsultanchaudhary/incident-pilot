import type { IncidentDetail } from '../types'

export function StackTraceViewer({ detail }: { detail: IncidentDetail }) { const trace = detail.events.find((event) => event.trace)?.trace; return <div className="stack-trace"><div className="exception-name">{detail.stack_trace.exception || 'No trace captured'}</div><p>{detail.stack_trace.message}</p>{trace ? <pre>{trace}</pre> : <p className="muted">No stack trace is available for this incident.</p>}</div> }
