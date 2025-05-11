import { useEffect, useRef, useState } from 'react'
import { Button, Card, Image, Input, Modal, Loading } from 'antd-mobile'
import useWebSocket from '../hooks/websocket'

interface RecipeHistory {
  message: string
  drinks: {
    name: string
    ingredients: {
      name: string
      percentage: number
      volume: number
    }[]
    photo: string
  }
}

type MessageType = 'assistant' | 'user'
/**
 * Represents a message with a role and content.
 * The role determines the type of content:
 * - If the role is 'user', the content is a string.
 * - If the role is 'assistant', the content is a RecipeHistory object.
 */
type Message<T extends MessageType> = {
  role: T
  content: T extends 'user' ? string : RecipeHistory
}

function Assistant() {
  const { socket, status } = useWebSocket(import.meta.env.VITE_API_URL)
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [loadingMessage, setLoadingMessage] = useState('')
  const [error, setError] = useState(false)
  const [errorMessage, setErrorMessage] = useState('')
  const [messages, setMessages] = useState<Message<MessageType>[]>([])
  const chatContainer = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (chatContainer.current) {
      chatContainer.current.scrollTop = chatContainer.current.scrollHeight
    }
  }, [messages])

  async function handleSubmit() {
    try {
      setLoading(true)

      if (!socket) return
      socket.send(JSON.stringify({ user_input: input }))
      setMessages((messages) => [...messages, { role: 'user', content: input }])
      setInput('')
    } catch (error) {
      console.log(error)
    }
  }

  function assertMessage(message: Message<MessageType>): message is Message<'assistant'> {
    return message.role === 'assistant'
  }

  useEffect(() => {
    if (!socket) return
    socket.on('open', () => {
      console.log('Connection opened')
      setLoading(false)
    })

    socket.on('welcome', (event) => {
      console.log('Welcome message received', event)
      setMessages((messages) => [...messages, { role: 'assistant', content: event }])
    })
    socket.on('error', (event) => {
      setLoading(false)
      setError(true)
      setErrorMessage(event.message)
    })
    socket.on('loading', (event) => {
      setLoading(true)
      setLoadingMessage(event.message)
    })
    socket.on('message', (event) => {
      setMessages((messages) => [...messages, { role: 'assistant', content: event }])
      setLoading(false)
      setError(false)
      setErrorMessage('')
      setLoadingMessage('')
    })
    socket.on('drink', (event) => {
      setMessages((messages) => [...messages, { role: 'assistant', content: event.data }])
      setLoading(false)
      setError(false)
      setErrorMessage('')
      setLoadingMessage('')
    })
    socket.on('new_drink', (event) => {
      setMessages((messages) => [...messages, { role: 'assistant', content: event.data }])
      setLoading(false)
      setError(false)
      setErrorMessage('')
      setLoadingMessage('')
    })
  }, [socket])

  useEffect(() => {
    if (status === 'disconnected') {
      setLoading(false)
      Modal.show({
        content: 'Disconnected from server',
        actions: [
          {
            key: 'reconnect',
            text: 'Reconnect',
          }
        ]
      })
    }
  }, [status, socket])

  return (
    <>
      <div ref={chatContainer} style={{ height: 'calc(100% - 50px)', overflowY: 'auto', marginBottom: '10px' }}>
        {messages.map((message, index) => (
          <div
            key={`${message.role}-${index}`}
            style={{
              display: 'flex',
              justifyContent: assertMessage(message) ? 'left' : 'right',
              width: '100%',
              margin: '0.5rem 0',
            }}
          >
            <div
              style={{
                textAlign: 'left',
              }}
            >
              <span style={{ fontSize: '0.875rem' }}>
                {assertMessage(message) ? 'Agent' : ''}
              </span>
              {assertMessage(message)
                ? (
                  <Card
                    style={{
                      backgroundColor: assertMessage(message) ? '#111111' : 'var(--adm-color-primary)',
                    }}
                  >
                    {message.content.message}
                    {message.content.drinks ?
                    (
                      <>
                        <p style={{ margin: 0 }}>{message.content.drinks.name}</p>
                        <Image src={message.content.drinks.photo} alt={message.content.drinks.name} />
                      </>
                    ) : (
                      <></>
                    )}
                  </Card>
                )
                : <Card
                    style={{
                      backgroundColor: assertMessage(message) ? '#111111' : 'var(--adm-color-primary)',
                    }}
                  >
                    {message.content as string}
                  </Card>
              }
            </div>
          </div>
        ))}
        {loading && (
          <div style={{ textAlign: 'center', margin: '0.5rem' }}>
            <Loading />
            <p style={{ fontSize: '0.875rem' }}>{loadingMessage}</p>
          </div>
        )}
        {error && (
          <div style={{ textAlign: 'center', margin: '0.5rem' }}>
            <p style={{ fontSize: '0.875rem' }}>{errorMessage}</p>
          </div>
        )}
      </div>

      <div style={{ width: '100%', display: 'flex', gap: '0.5rem' }}>
        <div style={{   borderRadius: '5px', padding: '0.25rem', flex: 1, backgroundColor: '#111111' }}>
          <Input
            value={input}
            placeholder="Enter your preference"
            style={{ height: '100%', }}
            onChange={setInput}
            onEnterPress={handleSubmit}
          />
        </div>
        <Button
          color="primary"
          onClick={handleSubmit}
          disabled={status === 'disconnected' || loading}
          size="small"
        >
          {loading ? 'Loading...' : 'Send'}
        </Button>
        </div>
    </>
  )
}

export default Assistant