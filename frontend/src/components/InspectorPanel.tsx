import type { McpResult } from '../types/mcp'
import type { Memory } from '../types/memory'
import { McpInspector } from './McpInspector'
import { MemoryInspector } from './MemoryInspector'
import './InspectorPanel.css'

interface InspectorPanelProps {
  recentMemories: Memory[]
  relevantMemories: Memory[]
  mcpResults: McpResult[]
}

export function InspectorPanel({
  recentMemories,
  relevantMemories,
  mcpResults,
}: InspectorPanelProps) {
  return (
    <aside className="inspector-panel" aria-label="Request inspectors">
      <MemoryInspector
        recentMemories={recentMemories}
        relevantMemories={relevantMemories}
      />
      <McpInspector results={mcpResults} />
    </aside>
  )
}
