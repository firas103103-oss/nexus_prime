import { useState, useEffect } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { motion, AnimatePresence } from 'framer-motion'
import { Menu, X, Globe } from 'lucide-react'
import './Navbar.css'

function Navbar() {
  const { t, i18n } = useTranslation()
  const location = useLocation()
  const [isScrolled, setIsScrolled] = useState(false)
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false)

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 50)
    }
    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  const toggleLanguage = () => {
    const newLang = i18n.language === 'en' ? 'ar' : 'en'
    i18n.changeLanguage(newLang)
  }

  const navLinks = [
    { path: '/', label: t('nav.gateway') },
    { path: '/origins', label: t('nav.origins') },
    { path: '/tech', label: t('nav.tech') },
    { path: '/sentinel', label: t('nav.sentinel') },
    { path: '/boardroom', label: t('nav.boardroom') },
    { path: '/contact', label: t('nav.contact') }
  ]

  return (
    <motion.nav 
      className={`navbar ${isScrolled ? 'scrolled' : ''}`}
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <div className="navbar-container">
        <Link to="/" className="navbar-logo">
          <motion.div 
            className="logo-icon"
            animate={{ 
              boxShadow: ['0 0 20px rgba(0,255,136,0.3)', '0 0 40px rgba(0,255,136,0.6)', '0 0 20px rgba(0,255,136,0.3)']
            }}
            transition={{ duration: 2, repeat: Infinity }}
          >
            <span>X</span>
          </motion.div>
          <span className="logo-text">X-BIO</span>
        </Link>

        <div className="navbar-links">
          {navLinks.map((link) => (
            <Link
              key={link.path}
              to={link.path}
              className={`nav-link ${location.pathname === link.path ? 'active' : ''}`}
            >
              <span>{link.label}</span>
              {location.pathname === link.path && (
                <motion.div
                  className="active-indicator"
                  layoutId="activeIndicator"
                  transition={{ type: 'spring', stiffness: 300, damping: 30 }}
                />
              )}
            </Link>
          ))}
        </div>

        <div className="navbar-actions">
          <button className="lang-toggle" onClick={toggleLanguage}>
            <Globe size={18} />
            <span>{i18n.language === 'en' ? 'عربي' : 'EN'}</span>
          </button>

          <button 
            className="mobile-menu-btn"
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
          >
            {isMobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>
      </div>

      <AnimatePresence>
        {isMobileMenuOpen && (
          <motion.div 
            className="mobile-menu"
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.3 }}
          >
            {navLinks.map((link, index) => (
              <motion.div
                key={link.path}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
              >
                <Link
                  to={link.path}
                  className={`mobile-nav-link ${location.pathname === link.path ? 'active' : ''}`}
                  onClick={() => setIsMobileMenuOpen(false)}
                >
                  {link.label}
                </Link>
              </motion.div>
            ))}
          </motion.div>
        )}
      </AnimatePresence>
    </motion.nav>
  )
}

export default Navbar
