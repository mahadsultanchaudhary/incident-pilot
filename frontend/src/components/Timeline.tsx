import type { Analysis } from '../types'
import { relativeTime } from '../utils/format'

export function Timeline({ items }: { items: Analysis['timeline'] }) { return <ol className="timeline">{items.map((item, index) => <li key={`${item.timestamp}-${index}`}><i className={`dot ${item.level.toLowerCase()}`} /><div><time>{relativeTime(item.timestamp)}</time><p>{item.event}</p></div></li>)}</ol> }
