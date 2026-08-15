export type ChatMessageRole = 'user' | 'assistant' | 'error'

export interface ChatMessage {
  id: string
  role: ChatMessageRole
  content: string
  createdAt: string
}
