import type { Memory } from '../types/memory'
import { MemoryItem } from './MemoryItem'

interface MemorySectionProps {
  title: string
  memories: Memory[]
}

export function MemorySection({ title, memories }: MemorySectionProps) {
  return (
    <section className="memory-section">
      <h3>=== {title} ===</h3>
      {memories.length > 0 ? (
        <div className="memory-section__items">
          {memories.map((memory) => (
            <MemoryItem key={memory.id} memory={memory} />
          ))}
        </div>
      ) : (
        <p className="memory-section__empty">No memories used.</p>
      )}
    </section>
  )
}
