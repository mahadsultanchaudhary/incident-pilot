import { useMemo, useState } from 'react'
import { Search } from 'lucide-react'
import type { LogEvent } from '../types'
import { relativeTime } from '../utils/format'

export function LogViewer({ logs }: { logs: LogEvent[] }) {
  const [query, setQuery] = useState('')
  const filtered = useMemo(() => logs.filter((log) => `${log.service} ${log.message}`.toLowerCase().includes(query.toLowerCase())), [logs, query])
  return <><label className="search-field compact"><Search size={15} /><input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Filter log stream" /></label><div className="log-stream">{filtered.slice(0, 9).map((log) => <div className="log-row" key={log.id}><time>{relativeTime(log.timestamp)}</time><span className={`log-level ${log.level.toLowerCase()}`}>{log.level}</span><span className="log-service">{log.service}</span><span className="log-message">{log.message}</span></div>)}</div></>
}
