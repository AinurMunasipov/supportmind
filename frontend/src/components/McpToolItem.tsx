import type { McpResult } from '../types/mcp'

interface McpToolItemProps {
  result: McpResult
}

function formatContent(content: string): string {
  try {
    return JSON.stringify(JSON.parse(content), null, 2)
  } catch {
    return content
  }
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
      <pre>{formatContent(result.content)}</pre>
    </article>
  )
}
