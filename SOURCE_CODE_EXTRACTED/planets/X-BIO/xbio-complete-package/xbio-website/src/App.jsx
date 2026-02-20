import { Routes, Route } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { useEffect } from 'react'
import Navbar from './components/Navbar'
import Footer from './components/Footer'
import Gateway from './pages/Gateway'
import Origins from './pages/Origins'
import Tech from './pages/Tech'
import Sentinel from './pages/Sentinel'
import Contact from './pages/Contact'

function App() {
  const { i18n } = useTranslation()

  useEffect(() => {
    document.body.dir = i18n.language === 'ar' ? 'rtl' : 'ltr'
  }, [i18n.language])

  return (
    <div className="app">
      <Navbar />
      <main>
        <Routes>
          <Route path="/" element={<Gateway />} />
          <Route path="/origins" element={<Origins />} />
          <Route path="/tech" element={<Tech />} />
          <Route path="/sentinel" element={<Sentinel />} />
          <Route path="/contact" element={<Contact />} />
        </Routes>
      </main>
      <Footer />
    </div>
  )
}

export default App
