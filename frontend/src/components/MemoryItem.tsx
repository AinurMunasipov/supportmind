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
      <dl>
        <div>
          <dt>Role</dt>
          <dd>{memory.role}</dd>
        </div>
        <div>
          <dt>Content</dt>
          <dd>{memory.content}</dd>
        </div>
        <div>
          <dt>Created at</dt>
          <dd>
            <time dateTime={memory.created_at}>
              {formatCreatedAt(memory.created_at)}
            </time>
          </dd>
        </div>
        <div>
          <dt>Importance</dt>
          <dd>{memory.importance}</dd>
        </div>
        {memory.summary ? (
          <div>
            <dt>Summary</dt>
            <dd>{memory.summary}</dd>
          </div>
        ) : null}
      </dl>
    </article>
  )
}
