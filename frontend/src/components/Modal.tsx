import type { ReactNode } from 'react'
import { X } from 'lucide-react'
export function Modal({ title, onClose, children }: { title: string; onClose: () => void; children: ReactNode }) { return <div className="modal-backdrop" role="presentation" onMouseDown={onClose}><section className="modal" role="dialog" aria-modal="true" aria-label={title} onMouseDown={(event) => event.stopPropagation()}><header><h2>{title}</h2><button className="icon-button" onClick={onClose} aria-label="Close dialog"><X size={18} /></button></header>{children}</section></div> }
