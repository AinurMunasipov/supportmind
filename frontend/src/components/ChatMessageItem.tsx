import type { ChatMessage } from '../types/chat'

interface ChatMessageItemProps {
  message: ChatMessage
}

const roleLabels: Record<ChatMessage['role'], string> = {
  user: 'User',
  assistant: 'Assistant',
  error: 'Error',
}

export function ChatMessageItem({ message }: ChatMessageItemProps) {
  return (
    <article className={`chat-message chat-message--${message.role}`}>
      <span className="chat-message__role">{roleLabels[message.role]}</span>
      <p>{message.content}</p>
    </article>
  )
}
