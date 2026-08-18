import type { Memory } from '../types/memory'

interface MemoryItemProps {
  memory: Memory
}

function formatCreatedAt(createdAt: string): string {
  const date = new Date(createdAt)
  return Number.isNaN(date.getTime()) ? createdAt : date.toLocaleString()
}

export function MemoryItem({ memory }: MemoryItemProps) {
  return (
    <article className="memory-item">
      <header className="memory-item__header">
        <strong>{memory.role}</strong>
        <time dateTime={memory.created_at}>
          {formatCreatedAt(memory.created_at)}
        </time>
      </header>
      {memory.summary ? (
        <div className="memory-item__summary">
          <span>Summary</span>
          <p>{memory.summary}</p>
        </div>
      ) : (
        <p className="memory-item__content">{memory.content}</p>
      )}
    </article>
  )
}
