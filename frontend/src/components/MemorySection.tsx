import type { Memory } from '../types/memory'
import { MemoryItem } from './MemoryItem'

interface MemorySectionProps {
  title: string
  description: string
  memories: Memory[]
  emptyMessage: string
}

export function MemorySection({
  title,
  description,
  memories,
  emptyMessage,
}: MemorySectionProps) {
  return (
    <section className="memory-section">
      <header className="inspector-content-header">
        <h2>{title}</h2>
        <p>{description}</p>
      </header>
      <div className="memory-section__body">
        {memories.length > 0 ? (
          <div className="memory-section__items">
            {memories.map((memory) => (
              <MemoryItem key={memory.id} memory={memory} />
            ))}
          </div>
        ) : (
          <p className="memory-section__empty">{emptyMessage}</p>
        )}
      </div>
    </section>
  )
}
