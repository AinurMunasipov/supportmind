import type { McpResult } from '../types/mcp'
import { McpToolItem } from './McpToolItem'
import './McpInspector.css'

interface McpInspectorProps {
  results: McpResult[]
}

export function McpInspector({ results }: McpInspectorProps) {
  return (
    <section className="mcp-inspector" aria-labelledby="mcp-inspector-title">
      <header className="inspector-content-header">
        <h2 id="mcp-inspector-title">MCP Inspector</h2>
        <p>MCP tools executed for this request.</p>
      </header>
      {results.length > 0 ? (
        <div className="mcp-inspector__items">
          {results.map((result, index) => (
            <McpToolItem key={`${result.tool}-${index}`} result={result} />
          ))}
        </div>
      ) : (
        <p className="inspector-empty-state">No MCP tools executed.</p>
      )}
    </section>
  )
}
