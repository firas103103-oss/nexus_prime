import { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { motion } from 'framer-motion'
import { Send, Mail, Shield, Lock, Terminal } from 'lucide-react'
import './Contact.css'

function Contact() {
  const { t } = useTranslation()
  const [formData, setFormData] = useState({
    name: '',
    organization: '',
    email: '',
    department: 'sales',
    message: ''
  })
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [isSubmitted, setIsSubmitted] = useState(false)

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setIsSubmitting(true)
    await new Promise(resolve => setTimeout(resolve, 2000))
    setIsSubmitting(false)
    setIsSubmitted(true)
  }

  return (
    <div className="contact-page">
      <section className="contact-hero">
        <div className="contact-background">
          <div className="matrix-rain" />
          <div className="grid-floor" />
        </div>
        
        <motion.div 
          className="contact-hero-content"
          initial={{ opacity: 0, y: 50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
        >
          <div className="secure-badge">
            <Lock size={16} />
            <span>ENCRYPTED CHANNEL</span>
          </div>
          <h1 className="section-title">{t('contact.title')}</h1>
          <p className="section-subtitle">{t('contact.subtitle')}</p>
        </motion.div>
      </section>

      <section className="contact-section section">
        <div className="contact-container">
          <motion.div 
            className="contact-form-wrapper"
            initial={{ opacity: 0, x: -50 }}
            whileInView={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
          >
            <div className="terminal-header">
              <div className="terminal-dots">
                <span className="dot red" />
                <span className="dot yellow" />
                <span className="dot green" />
              </div>
              <span className="terminal-title">SECURE_TRANSMISSION.exe</span>
            </div>
            
            {!isSubmitted ? (
              <form onSubmit={handleSubmit} className="contact-form">
                <div className="form-line">
                  <span className="prompt">{'>>'}</span>
                  <span className="label">{t('contact.form.name')}:</span>
                </div>
                <div className="form-group">
                  <input
                    type="text"
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                    placeholder={t('contact.form.namePlaceholder')}
                    required
                  />
                </div>

                <div className="form-line">
                  <span className="prompt">{'>>'}</span>
                  <span className="label">{t('contact.form.organization')}:</span>
                </div>
                <div className="form-group">
                  <input
                    type="text"
                    name="organization"
                    value={formData.organization}
                    onChange={handleChange}
                    placeholder={t('contact.form.organizationPlaceholder')}
                    required
                  />
                </div>

                <div className="form-line">
                  <span className="prompt">{'>>'}</span>
                  <span className="label">{t('contact.form.email')}:</span>
                </div>
                <div className="form-group">
                  <input
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    placeholder={t('contact.form.emailPlaceholder')}
                    required
                  />
                </div>

                <div className="form-line">
                  <span className="prompt">{'>>'}</span>
                  <span className="label">{t('contact.form.department')}:</span>
                </div>
                <div className="form-group">
                  <select 
                    name="department" 
                    value={formData.department} 
                    onChange={handleChange}
                  >
                    <option value="sales">{t('contact.form.sales')}</option>
                    <option value="security">{t('contact.form.security')}</option>
                    <option value="partnership">{t('contact.form.partnership')}</option>
                  </select>
                </div>

                <div className="form-line">
                  <span className="prompt">{'>>'}</span>
                  <span className="label">{t('contact.form.message')}:</span>
                </div>
                <div className="form-group">
                  <textarea
                    name="message"
                    value={formData.message}
                    onChange={handleChange}
                    placeholder={t('contact.form.messagePlaceholder')}
                    rows={4}
                    required
                  />
                </div>

                <motion.button 
                  type="submit" 
                  className="submit-btn"
                  disabled={isSubmitting}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                >
                  {isSubmitting ? (
                    <>
                      <span className="loading-dots">TRANSMITTING</span>
                    </>
                  ) : (
                    <>
                      <Send size={18} />
                      {t('contact.form.submit')}
                    </>
                  )}
                </motion.button>
              </form>
            ) : (
              <motion.div 
                className="success-message"
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
              >
                <div className="success-icon">
                  <Shield size={48} />
                </div>
                <h3>TRANSMISSION SUCCESSFUL</h3>
                <p>Your message has been encrypted and transmitted to the X-BIO secure network.</p>
                <p className="response-time">Expected response within 24-48 hours.</p>
              </motion.div>
            )}
          </motion.div>

          <motion.div 
            className="contact-info"
            initial={{ opacity: 0, x: 50 }}
            whileInView={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            viewport={{ once: true }}
          >
            <div className="info-card glass-panel">
              <h3>{t('contact.info.title')}</h3>
              
              <div className="info-item">
                <div className="info-icon">
                  <Terminal size={24} />
                </div>
                <div className="info-content">
                  <span className="info-label">{t('contact.info.ambassador')}</span>
                  <span className="info-value">NEXUS</span>
                </div>
              </div>
              
              <div className="info-item">
                <div className="info-icon">
                  <Mail size={24} />
                </div>
                <div className="info-content">
                  <span className="info-label">Secure Email</span>
                  <a href="mailto:nexus.rel@xbio103.org" className="info-value email">
                    {t('contact.info.email')}
                  </a>
                </div>
              </div>
              
              <div className="security-note">
                <Lock size={16} />
                <p>{t('contact.info.note')}</p>
              </div>
            </div>
            
            <div className="routing-options glass-panel">
              <h4>ROUTING OPTIONS</h4>
              <div className="route-list">
                <div className="route-item">
                  <span className="route-code">SAL-001</span>
                  <span className="route-name">{t('contact.form.sales')}</span>
                </div>
                <div className="route-item">
                  <span className="route-code">SEC-002</span>
                  <span className="route-name">{t('contact.form.security')}</span>
                </div>
                <div className="route-item">
                  <span className="route-code">PAR-003</span>
                  <span className="route-name">{t('contact.form.partnership')}</span>
                </div>
              </div>
            </div>
          </motion.div>
        </div>
      </section>
    </div>
  )
}

export default Contact
