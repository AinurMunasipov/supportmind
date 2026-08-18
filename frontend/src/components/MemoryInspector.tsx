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
    <>
      <MemorySection
        title="Recent Memory"
        description="Recent conversation context."
        memories={recentMemories}
        emptyMessage="No recent memories."
      />
      <MemorySection
        title="Relevant Memory"
        description="Retrieved memory for the current response."
        memories={relevantMemories}
        emptyMessage="No relevant memories."
      />
    </>
  )
}
