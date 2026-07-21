import { useCallback, useEffect, useState } from 'react'

export function useAsync<T>(loader: () => Promise<T>, dependencies: unknown[] = []) {
  const [data, setData] = useState<T | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const run = useCallback(async () => {
    setLoading(true); setError(null)
    try { setData(await loader()) } catch { setError('Unable to reach IncidentPilot API. Start the backend to load live data.') } finally { setLoading(false) }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, dependencies)
  useEffect(() => { void run() }, [run])
  return { data, loading, error, reload: run }
}
