import { useEffect, useRef, useState } from 'react'
import type { FormEvent } from 'react'
import { sendChatMessage } from './api/chat'
import { ChatMessageItem } from './components/ChatMessageItem'
import type { ChatMessage } from './types/chat'
import './App.css'

function createMessage(
  role: ChatMessage['role'],
  content: string,
): ChatMessage {
  return {
    id: crypto.randomUUID(),
    role,
    content,
  }
}

function App() {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [message, setMessage] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const chatEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, isLoading])

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()

    const trimmedMessage = message.trim()
    if (!trimmedMessage || isLoading) {
      return
    }

    setMessages((currentMessages) => [
      ...currentMessages,
      createMessage('user', trimmedMessage),
    ])
    setMessage('')
    setIsLoading(true)

    try {
      const assistantResponse = await sendChatMessage(trimmedMessage)
      setMessages((currentMessages) => [
        ...currentMessages,
        createMessage('assistant', assistantResponse),
      ])
    } catch (error) {
      const errorMessage =
        error instanceof Error
          ? error.message
          : 'Something went wrong while contacting SupportMind.'
      setMessages((currentMessages) => [
        ...currentMessages,
        createMessage('error', errorMessage),
      ])
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <main className="app-shell">
      <header className="app-header">
        <h1>SupportMind</h1>
        <p>AI support assistant</p>
      </header>

      <section className="chat-area" aria-label="Conversation" aria-live="polite">
        {messages.length === 0 && !isLoading ? (
          <p className="empty-state">Start a conversation with SupportMind.</p>
        ) : null}

        {messages.map((chatMessage) => (
          <ChatMessageItem key={chatMessage.id} message={chatMessage} />
        ))}

        {isLoading ? (
          <ChatMessageItem
            message={{
              id: 'thinking',
              role: 'assistant',
              content: 'Thinking...',
            }}
          />
        ) : null}
        <div ref={chatEndRef} />
      </section>

      <form className="message-form" onSubmit={handleSubmit}>
        <label className="visually-hidden" htmlFor="message">
          Message
        </label>
        <textarea
          id="message"
          name="message"
          rows={3}
          value={message}
          onChange={(event) => setMessage(event.target.value)}
          placeholder="Type your message..."
        />
        <button type="submit" disabled={isLoading || !message.trim()}>
          Send
        </button>
      </form>
    </main>
  )
}

export default App
