import type { McpResult } from '../types/mcp'

interface McpToolItemProps {
  result: McpResult
}

export function McpToolItem({ result }: McpToolItemProps) {
  return (
    <article className="mcp-tool-item">
      <header className="mcp-tool-item__header">
        <strong>{result.tool}</strong>
        <span
          className={`mcp-tool-item__status mcp-tool-item__status--${result.success ? 'success' : 'error'}`}
        >
          {result.success ? 'Success' : 'Failed'}
        </span>
      </header>
      <pre>{result.content}</pre>
    </article>
  )
}
