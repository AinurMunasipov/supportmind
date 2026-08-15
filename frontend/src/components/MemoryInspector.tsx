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
        <p>Memory context used for the current request.</p>
      </header>
      <div className="memory-inspector__content">
        <MemorySection title="Recent Memory" memories={recentMemories} />
        <MemorySection title="Relevant Memory" memories={relevantMemories} />
      </div>
    </section>
  )
}
