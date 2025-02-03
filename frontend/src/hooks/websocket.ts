import { useEffect, useState } from 'react'
import { io, Socket } from 'socket.io-client'

export function useWebSocket(domain: string) {
  const [socket, setSocket] = useState<Socket | null>(null)
  const [status, setStatus] = useState<'connected' | 'disconnected' | 'connecting'>('connecting')
  useEffect(() => {
    const newSocket = io(domain, { transports: ['websocket']  })
    setSocket(newSocket)
    return () => {
      newSocket.close()
    }
  }, [domain])

  useEffect(() => {
    if (!socket) return

    socket.on('connect', () => {
      setStatus('connected')
      console.log('Connected to server')
    })

    socket.on('disconnect', () => {
      setStatus('disconnected')
      console.log('Disconnected from server')
    })
  }, [socket])

  return { socket, status }
}

export default useWebSocket