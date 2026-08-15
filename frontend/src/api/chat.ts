import type { McpResult } from '../types/mcp'
import type { Memory } from '../types/memory'

export interface ChatResponse {
  response: string
  recent_memories?: Memory[]
  relevant_memories?: Memory[]
  mcp_results?: McpResult[]
}

function getApiBaseUrl(): string {
  const configuredUrl = import.meta.env.VITE_API_URL?.trim()
  if (!configuredUrl) {
    throw new Error('VITE_API_URL is not configured.')
  }

  return import.meta.env.DEV ? '/api' : configuredUrl.replace(/\/+$/, '')
}

function getErrorDetail(payload: unknown): string | null {
  if (
    typeof payload === 'object' &&
    payload !== null &&
    'detail' in payload &&
    typeof payload.detail === 'string'
  ) {
    return payload.detail
  }

  return null
}

export async function sendChatMessage(message: string): Promise<ChatResponse> {
  const response = await fetch(`${getApiBaseUrl()}/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      user_id: 'demo',
      message,
    }),
  })

  let payload: unknown
  try {
    payload = await response.json()
  } catch {
    payload = null
  }

  if (!response.ok) {
    const detail = getErrorDetail(payload)
    throw new Error(detail ?? `SupportMind request failed (${response.status}).`)
  }

  if (
    typeof payload !== 'object' ||
    payload === null ||
    !('response' in payload) ||
    typeof payload.response !== 'string'
  ) {
    throw new Error('SupportMind returned an invalid response.')
  }

  const chatResponse = payload as ChatResponse
  return {
    response: chatResponse.response,
    recent_memories: Array.isArray(chatResponse.recent_memories)
      ? chatResponse.recent_memories
      : [],
    relevant_memories: Array.isArray(chatResponse.relevant_memories)
      ? chatResponse.relevant_memories
      : [],
    mcp_results: Array.isArray(chatResponse.mcp_results)
      ? chatResponse.mcp_results
      : [],
  }
}
