import clsx from 'clsx'
import { titleCase } from '../utils/format'

export function StatusBadge({ value }: { value: string }) {
  return <span className={clsx('status-badge', `status-${value.toLowerCase()}`)}>{titleCase(value)}</span>
}
