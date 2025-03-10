import { useEffect, useRef, useState } from 'react'
import { Button, Card, Image, Input, Modal, Space, Spin } from 'antd'
import './App.css'
import useWebSocket from './hooks/websocket'

interface RecipeHistory {
  message: string
  recipe: {
    name: string
    ingredients: {
      name: string
      percentage: number
      volume: number
    }[]
    img: string
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

function App() {
  const { socket, status } = useWebSocket('http://127.0.0.1:8000')
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
      console.log('Connected to server')
      setLoading(false)
    })

    socket.on('welcome', (event) => {
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
    }
  }, [status])

  return (
    <div style={{ width: '414px', padding: '0 1rem' }}>
      <h1 style={{ fontSize: '2.5rem',  margin: '0 0 1rem 0' }}>Siiiiip AI</h1>
      <div ref={chatContainer} style={{ height: 'calc(100vh - 120px)', overflowY: 'auto' }}>
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
                textAlign: assertMessage(message) ? 'left' : 'right',
              }}
            >
              <span style={{ fontSize: '0.875rem' }}>
                {assertMessage(message) ? 'Agent' : ''}
              </span>
              {assertMessage(message)
                ? (
                  <Card
                    styles={{
                      body: {
                        padding: '0.5rem'
                      }
                    }}
                  >
                    {message.content.message}
                    {message.content.recipe ?
                    (
                      <>
                        <p style={{ margin: 0 }}>{message.content.recipe.name}</p>
                        <ul style={{ textAlign: 'left' }}>
                          {message.content.recipe.ingredients.map((ingredient) => (
                            <li key={ingredient.name}>
                            {ingredient.name} - {ingredient.volume}ml ({ingredient.percentage}%)
                            </li>
                          ))}
                        </ul>
                        <Image src={message.content.recipe.img} alt={message.content.recipe.name} />
                      </>
                    ) : (
                      <></>
                    )}
                  </Card>
                )
                : <Card
                    styles={{
                      body: {
                        padding: '0.5rem'
                      }
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
            <Spin />
            <p style={{ fontSize: '0.875rem' }}>{loadingMessage}</p>
          </div>
        )}
        {error && (
          <div style={{ textAlign: 'center', margin: '0.5rem' }}>
            <p style={{ fontSize: '0.875rem' }}>{errorMessage}</p>
          </div>
        )}
      </div>
      <Space.Compact style={{ width: '100%' }}>
        <Input
          value={input}
          placeholder="Enter your prompt"
          onChange={(e) => setInput(e.target.value)}
          style={{ marginBottom: 10 }}
          onPressEnter={handleSubmit}
        />
        <Button
          type="primary"
          onClick={handleSubmit}
          disabled={status === 'disconnected' || loading}
        >
          {loading ? 'Loading...' : 'Submit'}
        </Button>
      </Space.Compact>

      <Modal
        open={status === 'disconnected'} 
        okButtonProps={{ loading: status === 'connecting' }}
        okText="Reconnect"
        onOk={() => socket?.connect()}
        cancelButtonProps={{
          style: {
            display: 'none'
          }
        }}
        closable={false}
      >
        <p>Disconnected from server</p>
      </Modal>
    </div>
  )
}

export default App
