export function LoadingState({ label = 'Loading operational data' }: { label?: string }) { return <div className="state loading"><span className="spinner" />{label}</div> }
export function EmptyState({ label }: { label: string }) { return <div className="state">{label}</div> }
