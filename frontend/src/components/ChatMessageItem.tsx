import type { ChatMessage } from '../types/chat'

interface ChatMessageItemProps {
  message: ChatMessage
}

const roleLabels: Record<ChatMessage['role'], string> = {
  user: 'User',
  assistant: 'Assistant',
  error: 'Error',
}

function removeMarkdownFormatting(content: string): string {
  return content
    .replace(/```[^\n]*\n?/g, '')
    .replace(/`([^`\n]+)`/g, '$1')
    .replace(/\*\*([^*]+)\*\*/g, '$1')
    .replace(/__([^_]+)__/g, '$1')
    .replace(/```|`|\*\*|__/g, '')
}

export function ChatMessageItem({ message }: ChatMessageItemProps) {
  const timestamp = new Date(message.createdAt).toLocaleTimeString([], {
    hour: '2-digit',
    minute: '2-digit',
  })
  const content =
    message.role === 'assistant'
      ? removeMarkdownFormatting(message.content)
      : message.content

  return (
    <article className={`chat-message chat-message--${message.role}`}>
      <header className="chat-message__meta">
        <span className="chat-message__role">{roleLabels[message.role]}</span>
        <time dateTime={message.createdAt}>{timestamp}</time>
      </header>
      <p>{content}</p>
    </article>
  )
}
