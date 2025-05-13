
import { useEffect, useRef, useState } from 'react'
import { io, Socket } from 'socket.io-client'

export function useWebSocket(domain: string) {
  const [status, setStatus] = useState<'connected' | 'disconnected' | 'connecting'>('connecting')
  const socket = useRef<Socket | null>(null)
  useEffect(() => {
    if (socket.current) return
    socket.current = io(domain, {
      auth: {
        token: 'token'
      },
      transports: ['websocket']
    })
  }, [domain])

  useEffect(() => {
    if (!socket.current) return

    socket.current.on('connect', () => {
      setStatus('connected')
      console.log('Connected to server')
    })

    socket.current.on('disconnect', () => {
      setStatus('disconnected')
      console.log('Disconnected from server')
    })
  }, [])

  useEffect(() => {
    if (!socket.current) return
    if (status === 'connected') {
      socket.current.emit('init')
    }
  }, [status])

  return { socket: socket.current, status }
}

export default useWebSocket