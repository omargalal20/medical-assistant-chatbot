import './globals.css'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Chat from '@/pages/chat/chat'
import Layout from '@/components/layout/layout'

function App() {

  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<Chat />} />
        </Routes>
      </Layout>
  </BrowserRouter>
  )
}

export default App
