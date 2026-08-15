interface ChatResponse {
  response: string
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

export async function sendChatMessage(message: string): Promise<string> {
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

  return (payload as ChatResponse).response
}
