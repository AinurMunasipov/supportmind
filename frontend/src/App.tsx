import { useEffect, useRef, useState } from 'react'
import type { FormEvent, KeyboardEvent } from 'react'
import { sendChatMessage } from './api/chat'
import { ChatMessageItem } from './components/ChatMessageItem'
import { InspectorPanel } from './components/InspectorPanel'
import type { ChatMessage } from './types/chat'
import type { McpResult } from './types/mcp'
import type { Memory } from './types/memory'
import './App.css'

function createMessage(
  role: ChatMessage['role'],
  content: string,
): ChatMessage {
  return {
    id: crypto.randomUUID(),
    role,
    content,
    createdAt: new Date().toISOString(),
  }
}

function App() {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [message, setMessage] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [recentMemories, setRecentMemories] = useState<Memory[]>([])
  const [relevantMemories, setRelevantMemories] = useState<Memory[]>([])
  const [mcpResults, setMcpResults] = useState<McpResult[]>([])
  const chatEndRef = useRef<HTMLDivElement>(null)
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, isLoading])

  useEffect(() => {
    if (!isLoading) {
      textareaRef.current?.focus()
    }
  }, [isLoading])

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
    setRecentMemories([])
    setRelevantMemories([])
    setMcpResults([])

    try {
      const chatResponse = await sendChatMessage(trimmedMessage)
      setMessages((currentMessages) => [
        ...currentMessages,
        createMessage('assistant', chatResponse.response),
      ])
      setRecentMemories(chatResponse.recent_memories ?? [])
      setRelevantMemories(chatResponse.relevant_memories ?? [])
      setMcpResults(chatResponse.mcp_results ?? [])
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

  const handleMessageKeyDown = (
    event: KeyboardEvent<HTMLTextAreaElement>,
  ) => {
    if (event.key !== 'Enter' || event.shiftKey) {
      return
    }

    event.preventDefault()
    if (!isLoading && message.trim()) {
      event.currentTarget.form?.requestSubmit()
    }
  }

  return (
    <main className="workspace">
      <section className="app-shell" aria-label="SupportMind chat">
        <header className="app-header">
          <h1>SupportMind</h1>
          <p>AI support assistant</p>
        </header>

        <section className="chat-area" aria-label="Conversation" aria-live="polite">
          {messages.length === 0 && !isLoading ? (
            <div className="welcome-message">
              <p>
                Hi! I&apos;m SupportMind — an AI support assistant with long-term
                memory powered by CockroachDB.
              </p>
              <p>I can:</p>
              <ul>
                <li>remember previous conversations and user preferences;</li>
                <li>retrieve long-term memory when it is relevant;</li>
                <li>inspect CockroachDB databases through MCP;</li>
                <li>answer technical questions about your database;</li>
                <li>
                  integrate with Help Desk, CRM, Slack, Telegram, and other
                  support platforms.
                </li>
              </ul>
            </div>
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
                createdAt: new Date().toISOString(),
              }}
            />
          ) : null}
          <div ref={chatEndRef} />
        </section>

        <div className="composer">
          <p className="composer__status" role="status">
            {isLoading ? 'SupportMind is thinking...' : 'SupportMind is ready.'}
          </p>
          <form className="message-form" onSubmit={handleSubmit}>
            <label className="visually-hidden" htmlFor="message">
              Message
            </label>
            <textarea
              ref={textareaRef}
              id="message"
              name="message"
              rows={3}
              value={message}
              onChange={(event) => setMessage(event.target.value)}
              onKeyDown={handleMessageKeyDown}
              placeholder="Type your message..."
            />
            <button type="submit" disabled={isLoading || !message.trim()}>
              Send
            </button>
          </form>
        </div>
      </section>

      <InspectorPanel
        recentMemories={recentMemories}
        relevantMemories={relevantMemories}
        mcpResults={mcpResults}
      />
    </main>
  )
}

export default App
