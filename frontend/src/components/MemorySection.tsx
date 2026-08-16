import type { Memory } from '../types/memory'
import { MemoryItem } from './MemoryItem'

interface MemorySectionProps {
  title: string
  memories: Memory[]
  emptyMessage: string
}

export function MemorySection({
  title,
  memories,
  emptyMessage,
}: MemorySectionProps) {
  return (
    <section className="memory-section">
      <h3>{title}</h3>
      {memories.length > 0 ? (
        <div className="memory-section__items">
          {memories.map((memory) => (
            <MemoryItem key={memory.id} memory={memory} />
          ))}
        </div>
      ) : (
        <p className="memory-section__empty">{emptyMessage}</p>
      )}
    </section>
  )
}
