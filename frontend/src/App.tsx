import { useLayoutEffect, useState } from 'react'
import { Outlet, useLocation, useNavigate } from 'react-router'
import { NavBar, TabBar } from 'antd-mobile'
import { AppOutline, MessageOutline } from 'antd-mobile-icons'
import './App.css'

function App() {
  const [enableDarkMode] = useState(true)
  const navigator = useNavigate()
  const location = useLocation()

  useLayoutEffect(() => {
    document.documentElement.setAttribute(
      'data-prefers-color-scheme',
      enableDarkMode ? 'dark' : 'light'
    )
  }, [enableDarkMode])

  return (
    <div style={{ maxWidth: '414px', height: '100vh', overflow: 'hidden', display: 'flex', flexDirection: 'column', padding: '0 0.5rem' }}>
      <NavBar>
        Sip Studio
      </NavBar>
      
      <div style={{ height: 'calc(100% - 100px)' }}>
        <Outlet />
      </div>
      
      <TabBar activeKey={location.pathname}>
        {[
          {
            key: '/',
            title: 'Home',
            icon: <AppOutline />,
          },
          {
            key: '/assistant',
            title: 'Assistant',
            icon: <MessageOutline />,
          },
        ].map((item) => (
          <TabBar.Item key={item.key} icon={item.icon} title={item.title} onClick={() => navigator(item.key)} />
        ))}
      </TabBar>
    </div>
  )
}

export default App
