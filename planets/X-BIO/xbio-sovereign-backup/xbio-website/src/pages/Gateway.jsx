import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { motion, useScroll, useTransform } from 'framer-motion'
import { ChevronDown, Eye, Ear, Wind, Shield } from 'lucide-react'
import SentinelModel from '../components/SentinelModel'
import './Gateway.css'

function Gateway() {
  const { t } = useTranslation()
  const [isExploded, setIsExploded] = useState(false)
  const { scrollYProgress } = useScroll()
  const opacity = useTransform(scrollYProgress, [0, 0.3], [1, 0])
  const scale = useTransform(scrollYProgress, [0, 0.3], [1, 0.8])

  const features = [
    {
      icon: <Eye size={40} />,
      title: t('whyXbio.feature1Title'),
      desc: t('whyXbio.feature1Desc')
    },
    {
      icon: <Shield size={40} />,
      title: t('whyXbio.feature2Title'),
      desc: t('whyXbio.feature2Desc')
    },
    {
      icon: <Wind size={40} />,
      title: t('whyXbio.feature3Title'),
      desc: t('whyXbio.feature3Desc')
    }
  ]

  return (
    <div className="gateway-page">
      <section className="hero-section">
        <div className="hero-background">
          <div className="grid-overlay" />
          <div className="scan-line" />
        </div>
        
        <motion.div 
          className="hero-content"
          style={{ opacity, scale }}
        >
          <motion.div 
            className="hero-logo"
            initial={{ scale: 0, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ duration: 1, delay: 0.2 }}
          >
            <div className="logo-pulse">
              <span>X</span>
            </div>
          </motion.div>
          
          <motion.h1 
            className="hero-title"
            initial={{ y: 50, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ duration: 0.8, delay: 0.5 }}
          >
            {t('hero.tagline')}
            <br />
            <span className="highlight">{t('hero.taglineHighlight')}</span>
          </motion.h1>
          
          <motion.p 
            className="hero-subtitle"
            initial={{ y: 30, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ duration: 0.8, delay: 0.7 }}
          >
            {t('hero.subtitle')}
          </motion.p>
          
          <motion.div 
            className="hero-buttons"
            initial={{ y: 30, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ duration: 0.8, delay: 0.9 }}
          >
            <Link to="/tech" className="btn-primary">{t('hero.exploreBtn')}</Link>
            <Link to="/contact" className="btn-secondary">{t('hero.contactBtn')}</Link>
          </motion.div>
        </motion.div>
        
        <motion.div 
          className="hero-3d-container"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 1, delay: 1 }}
        >
          <SentinelModel isExploded={isExploded} />
          <button 
            className="explode-btn"
            onClick={() => setIsExploded(!isExploded)}
          >
            {isExploded ? t('gateway.collapse') : t('gateway.explodeView')}
          </button>
        </motion.div>
        
        <motion.div 
          className="scroll-indicator"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1.5 }}
        >
          <span>{t('gateway.scrollExplore')}</span>
          <ChevronDown className="bounce" size={24} />
        </motion.div>
      </section>
      
      <section className="why-section section">
        <motion.div
          initial={{ opacity: 0, y: 50 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
        >
          <h2 className="section-title">{t('whyXbio.title')}</h2>
          <div className="cyber-line" />
        </motion.div>
        
        <div className="features-grid">
          {features.map((feature, index) => (
            <motion.div
              key={index}
              className="feature-card glass-panel"
              initial={{ opacity: 0, y: 50 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: index * 0.2 }}
              viewport={{ once: true }}
              whileHover={{ 
                scale: 1.02, 
                borderColor: 'rgba(0, 255, 136, 0.5)',
                boxShadow: '0 0 30px rgba(0, 255, 136, 0.2)'
              }}
            >
              <div className="feature-icon">{feature.icon}</div>
              <h3>{feature.title}</h3>
              <p>{feature.desc}</p>
            </motion.div>
          ))}
        </div>
      </section>
      
      <section className="cta-section">
        <div className="cta-background">
          <div className="cta-glow" />
        </div>
        <motion.div
          className="cta-content"
          initial={{ opacity: 0, scale: 0.9 }}
          whileInView={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
        >
          <h2>{t('gateway.ctaTitle')}</h2>
          <p>{t('gateway.ctaSubtitle')}</p>
          <div className="cta-buttons">
            <Link to="/sentinel" className="btn-primary">{t('gateway.viewSentinel')}</Link>
            <Link to="/contact" className="btn-secondary">{t('gateway.contactUs')}</Link>
          </div>
        </motion.div>
      </section>
    </div>
  )
}

export default Gateway
