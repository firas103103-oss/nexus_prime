import { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { motion, AnimatePresence } from 'framer-motion'
import { Link } from 'react-router-dom'
import { Cpu, Radio, Battery, Wifi, Zap, Building2, FlaskConical, Home, Warehouse, ChevronDown, ChevronUp } from 'lucide-react'
import SentinelModel from '../components/SentinelModel'
import './Sentinel.css'

function Sentinel() {
  const { t } = useTranslation()
  const [expandedFaq, setExpandedFaq] = useState(null)

  const specs = [
    { icon: <Cpu size={24} />, label: t('product.specs.processor') },
    { icon: <Radio size={24} />, label: t('product.specs.sensors') },
    { icon: <Battery size={24} />, label: t('product.specs.battery') },
    { icon: <Wifi size={24} />, label: t('product.specs.connectivity') },
    { icon: <Zap size={24} />, label: t('product.specs.response') }
  ]

  const scenarios = [
    { icon: <Building2 size={32} />, label: t('product.scenarios.facility') },
    { icon: <Warehouse size={32} />, label: t('product.scenarios.storage') },
    { icon: <FlaskConical size={32} />, label: t('product.scenarios.lab') },
    { icon: <Home size={32} />, label: t('product.scenarios.residential') }
  ]

  const faqs = [
    { q: t('product.faq.q1'), a: t('product.faq.a1') },
    { q: t('product.faq.q2'), a: t('product.faq.a2') },
    { q: t('product.faq.q3'), a: t('product.faq.a3') }
  ]

  return (
    <div className="sentinel-page">
      <section className="sentinel-hero">
        <div className="sentinel-hero-bg">
          <div className="hex-pattern" />
        </div>
        
        <div className="sentinel-hero-content">
          <motion.div 
            className="hero-text"
            initial={{ opacity: 0, x: -50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8 }}
          >
            <div className="product-badge">CLASS 7 COGNITIVE DEVICE</div>
            <h1 className="section-title">{t('product.title')}</h1>
            <p className="section-subtitle">{t('product.subtitle')}</p>
            
            <div className="hero-cta">
              <Link to="/contact" className="btn-primary">{t('product.cta.preorder')}</Link>
              <Link to="/contact" className="btn-secondary">{t('product.cta.demo')}</Link>
            </div>
          </motion.div>
          
          <motion.div 
            className="hero-3d"
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.8, delay: 0.2 }}
          >
            <SentinelModel />
          </motion.div>
        </div>
      </section>

      <section className="specs-section section">
        <motion.h2 
          className="section-title"
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
        >
          {t('product.specs.title')}
        </motion.h2>
        
        <div className="specs-grid">
          {specs.map((spec, index) => (
            <motion.div
              key={index}
              className="spec-card glass-panel"
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              viewport={{ once: true }}
              whileHover={{ scale: 1.02, borderColor: 'rgba(0, 255, 136, 0.5)' }}
            >
              <div className="spec-icon">{spec.icon}</div>
              <span className="spec-label">{spec.label}</span>
            </motion.div>
          ))}
        </div>
      </section>

      <section className="scenarios-section">
        <div className="section">
          <motion.h2 
            className="section-title"
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
          >
            {t('product.scenarios.title')}
          </motion.h2>
          
          <div className="scenarios-grid">
            {scenarios.map((scenario, index) => (
              <motion.div
                key={index}
                className="scenario-card"
                initial={{ opacity: 0, scale: 0.9 }}
                whileInView={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                viewport={{ once: true }}
                whileHover={{ 
                  y: -10,
                  boxShadow: '0 20px 40px rgba(0, 255, 136, 0.2)'
                }}
              >
                <div className="scenario-icon">{scenario.icon}</div>
                <span className="scenario-label">{scenario.label}</span>
                <div className="scenario-glow" />
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      <section className="faq-section section">
        <motion.h2 
          className="section-title"
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
        >
          {t('product.faq.title')}
        </motion.h2>
        
        <div className="faq-container">
          {faqs.map((faq, index) => (
            <motion.div
              key={index}
              className={`faq-item glass-panel ${expandedFaq === index ? 'expanded' : ''}`}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.4, delay: index * 0.1 }}
              viewport={{ once: true }}
            >
              <button 
                className="faq-question"
                onClick={() => setExpandedFaq(expandedFaq === index ? null : index)}
              >
                <span>{faq.q}</span>
                {expandedFaq === index ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
              </button>
              <AnimatePresence>
                {expandedFaq === index && (
                  <motion.div
                    className="faq-answer"
                    initial={{ height: 0, opacity: 0 }}
                    animate={{ height: 'auto', opacity: 1 }}
                    exit={{ height: 0, opacity: 0 }}
                    transition={{ duration: 0.3 }}
                  >
                    <p>{faq.a}</p>
                  </motion.div>
                )}
              </AnimatePresence>
            </motion.div>
          ))}
        </div>
      </section>

      <section className="cta-section-product">
        <motion.div
          className="cta-content"
          initial={{ opacity: 0, scale: 0.9 }}
          whileInView={{ opacity: 1, scale: 1 }}
          viewport={{ once: true }}
        >
          <h2>{t('sentinel.ctaTitle')}</h2>
          <p>{t('sentinel.ctaSubtitle')}</p>
          <div className="cta-buttons">
            <Link to="/contact" className="btn-primary">{t('product.cta.preorder')}</Link>
            <Link to="/contact" className="btn-secondary">{t('product.cta.demo')}</Link>
          </div>
        </motion.div>
      </section>
    </div>
  )
}

export default Sentinel
