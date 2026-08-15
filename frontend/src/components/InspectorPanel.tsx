import { useState } from 'react'
import type { McpResult } from '../types/mcp'
import type { Memory } from '../types/memory'
import { McpInspector } from './McpInspector'
import { MemoryInspector } from './MemoryInspector'
import './InspectorPanel.css'

type InspectorTab = 'memory' | 'mcp'

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
  const [activeTab, setActiveTab] = useState<InspectorTab>('memory')

  return (
    <aside className="inspector-panel" aria-label="Request inspectors">
      <div className="inspector-tabs" role="tablist" aria-label="Inspector type">
        <button
          id="memory-tab"
          type="button"
          role="tab"
          aria-selected={activeTab === 'memory'}
          aria-controls="memory-panel"
          onClick={() => setActiveTab('memory')}
        >
          Memory
        </button>
        <button
          id="mcp-tab"
          type="button"
          role="tab"
          aria-selected={activeTab === 'mcp'}
          aria-controls="mcp-panel"
          onClick={() => setActiveTab('mcp')}
        >
          MCP
        </button>
      </div>

      <div
        id="memory-panel"
        className="inspector-view"
        role="tabpanel"
        aria-labelledby="memory-tab"
        hidden={activeTab !== 'memory'}
      >
        <MemoryInspector
          recentMemories={recentMemories}
          relevantMemories={relevantMemories}
        />
      </div>
      <div
        id="mcp-panel"
        className="inspector-view"
        role="tabpanel"
        aria-labelledby="mcp-tab"
        hidden={activeTab !== 'mcp'}
      >
        <McpInspector results={mcpResults} />
      </div>
    </aside>
  )
}
