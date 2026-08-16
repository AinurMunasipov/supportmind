import type { Memory } from '../types/memory'
import { MemorySection } from './MemorySection'
import './MemoryInspector.css'

interface MemoryInspectorProps {
  recentMemories: Memory[]
  relevantMemories: Memory[]
}

export function MemoryInspector({
  recentMemories,
  relevantMemories,
}: MemoryInspectorProps) {
  return (
    <section className="memory-inspector" aria-labelledby="memory-inspector-title">
      <header className="inspector-content-header">
        <h2 id="memory-inspector-title">Memory Inspector</h2>
        <p>Retrieved memory for the current response.</p>
      </header>
      <div className="memory-inspector__content">
        <MemorySection
          title="Recent Memory"
          memories={recentMemories}
          emptyMessage="No recent memories."
        />
        <MemorySection
          title="Relevant Memory"
          memories={relevantMemories}
          emptyMessage="No relevant memories."
        />
      </div>
    </section>
  )
}
