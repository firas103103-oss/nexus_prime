import { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { motion, AnimatePresence } from 'framer-motion'
import { Eye, Ear, Wind, Shield, Zap, Lock, ChevronRight } from 'lucide-react'
import './Tech.css'

function Tech() {
  const { t } = useTranslation()
  const [activeSense, setActiveSense] = useState('eye')

  const senses = {
    eye: {
      icon: <Eye size={48} />,
      name: t('tech.senses.eye.name'),
      desc: t('tech.senses.eye.desc'),
      color: '#ff4444',
      features: [
        t('tech.senses.eye.feature1'),
        t('tech.senses.eye.feature2'),
        t('tech.senses.eye.feature3')
      ]
    },
    ear: {
      icon: <Ear size={48} />,
      name: t('tech.senses.ear.name'),
      desc: t('tech.senses.ear.desc'),
      color: '#00ccff',
      features: [
        t('tech.senses.ear.feature1'),
        t('tech.senses.ear.feature2'),
        t('tech.senses.ear.feature3')
      ]
    },
    nose: {
      icon: <Wind size={48} />,
      name: t('tech.senses.nose.name'),
      desc: t('tech.senses.nose.desc'),
      color: '#ffaa00',
      features: [
        t('tech.senses.nose.feature1'),
        t('tech.senses.nose.feature2'),
        t('tech.senses.nose.feature3')
      ]
    }
  }

  return (
    <div className="tech-page">
      <section className="tech-hero">
        <div className="tech-background">
          <div className="circuit-pattern" />
        </div>
        <motion.div 
          className="tech-hero-content"
          initial={{ opacity: 0, y: 50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
        >
          <h1 className="section-title">{t('tech.title')}</h1>
          <p className="section-subtitle">{t('tech.subtitle')}</p>
        </motion.div>
      </section>

      <section className="senses-section section">
        <motion.h2 
          className="section-title"
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
        >
          {t('tech.senses.title')}
        </motion.h2>
        
        <div className="senses-container">
          <div className="senses-tabs">
            {Object.entries(senses).map(([key, sense]) => (
              <motion.button
                key={key}
                className={`sense-tab ${activeSense === key ? 'active' : ''}`}
                onClick={() => setActiveSense(key)}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                style={{ '--sense-color': sense.color }}
              >
                <span className="sense-icon">{sense.icon}</span>
                <span className="sense-name">{sense.name}</span>
              </motion.button>
            ))}
          </div>
          
          <AnimatePresence mode="wait">
            <motion.div
              key={activeSense}
              className="sense-content glass-panel"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
              style={{ '--sense-color': senses[activeSense].color }}
            >
              <div className="sense-visual">
                <div className="sense-orb" style={{ background: `radial-gradient(circle, ${senses[activeSense].color}40, transparent)` }}>
                  <motion.div 
                    className="sense-icon-large"
                    animate={{ 
                      boxShadow: [
                        `0 0 30px ${senses[activeSense].color}40`,
                        `0 0 60px ${senses[activeSense].color}80`,
                        `0 0 30px ${senses[activeSense].color}40`
                      ]
                    }}
                    transition={{ duration: 2, repeat: Infinity }}
                    style={{ borderColor: senses[activeSense].color, color: senses[activeSense].color }}
                  >
                    {senses[activeSense].icon}
                  </motion.div>
                </div>
                <div className="pulse-rings">
                  {[...Array(3)].map((_, i) => (
                    <motion.div
                      key={i}
                      className="pulse-ring"
                      style={{ borderColor: senses[activeSense].color }}
                      animate={{ scale: [1, 2], opacity: [0.5, 0] }}
                      transition={{ duration: 2, repeat: Infinity, delay: i * 0.5 }}
                    />
                  ))}
                </div>
              </div>
              
              <div className="sense-info">
                <h3 style={{ color: senses[activeSense].color }}>{senses[activeSense].name}</h3>
                <p className="sense-desc">{senses[activeSense].desc}</p>
                <ul className="sense-features">
                  {senses[activeSense].features.map((feature, index) => (
                    <motion.li
                      key={index}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: index * 0.1 }}
                    >
                      <ChevronRight size={16} style={{ color: senses[activeSense].color }} />
                      {feature}
                    </motion.li>
                  ))}
                </ul>
              </div>
            </motion.div>
          </AnimatePresence>
        </div>
      </section>

      <section className="defense-section">
        <div className="section">
          <motion.div
            className="defense-container"
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
          >
            <div className="defense-visual">
              <motion.div 
                className="silo-animation"
                animate={{ rotate: 360 }}
                transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
              >
                <div className="silo-ring ring-1" />
                <div className="silo-ring ring-2" />
                <div className="silo-ring ring-3" />
              </motion.div>
              <div className="silo-core">
                <Zap size={48} />
              </div>
            </div>
            
            <div className="defense-content">
              <h2 className="section-title">{t('tech.defense.title')}</h2>
              <p className="defense-desc">{t('tech.defense.desc')}</p>
              <div className="defense-stats">
                <div className="stat">
                  <span className="stat-value">{'<'}100ms</span>
                  <span className="stat-label">Response Time</span>
                </div>
                <div className="stat">
                  <span className="stat-value">360°</span>
                  <span className="stat-label">Coverage</span>
                </div>
                <div className="stat">
                  <span className="stat-value">12</span>
                  <span className="stat-label">Countermeasures</span>
                </div>
              </div>
            </div>
          </motion.div>
        </div>
      </section>

      <section className="sei-section section">
        <motion.div
          className="sei-container glass-panel"
          initial={{ opacity: 0, y: 50 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
        >
          <div className="sei-icon">
            <Lock size={64} />
          </div>
          <div className="sei-content">
            <h2>{t('tech.sei.title')}</h2>
            <p>{t('tech.sei.desc')}</p>
            <div className="sei-pillars">
              <div className="sei-pillar">
                <span className="pillar-letter">S</span>
                <span className="pillar-word">Sovereign</span>
              </div>
              <div className="sei-pillar">
                <span className="pillar-letter">E</span>
                <span className="pillar-word">Ethical</span>
              </div>
              <div className="sei-pillar">
                <span className="pillar-letter">I</span>
                <span className="pillar-word">Integrity</span>
              </div>
            </div>
          </div>
        </motion.div>
      </section>
    </div>
  )
}

export default Tech
