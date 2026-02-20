import { Link } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { motion } from 'framer-motion'
import './Footer.css'

function Footer() {
  const { t } = useTranslation()

  return (
    <footer className="footer">
      <div className="footer-glow" />
      <div className="footer-container">
        <div className="footer-main">
          <div className="footer-brand">
            <motion.div 
              className="footer-logo"
              whileHover={{ scale: 1.05 }}
            >
              <div className="logo-icon">
                <span>X</span>
              </div>
              <span className="logo-text">X-BIO GROUP</span>
            </motion.div>
            <p className="footer-tagline">{t('footer.tagline')}</p>
          </div>
          
          <div className="footer-links">
            <div className="footer-links-column">
              <h4>{t('footer.navigation')}</h4>
              <Link to="/">{t('nav.gateway')}</Link>
              <Link to="/origins">{t('nav.origins')}</Link>
              <Link to="/tech">{t('nav.tech')}</Link>
              <Link to="/sentinel">{t('nav.sentinel')}</Link>
              <Link to="/contact">{t('nav.contact')}</Link>
            </div>
            <div className="footer-links-column">
              <h4>{t('footer.legal')}</h4>
              <a href="#">{t('footer.privacy')}</a>
              <a href="#">{t('footer.terms')}</a>
            </div>
          </div>
        </div>
        
        <div className="footer-bottom">
          <div className="cyber-line" />
          <p className="copyright">{t('footer.copyright')}</p>
        </div>
      </div>
    </footer>
  )
}

export default Footer
