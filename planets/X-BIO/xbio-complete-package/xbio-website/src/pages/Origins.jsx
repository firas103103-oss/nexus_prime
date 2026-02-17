import { useTranslation } from 'react-i18next'
import { motion } from 'framer-motion'
import { User, Cpu, FlaskConical, Shield, Target, Lightbulb } from 'lucide-react'
import './Origins.css'

function Origins() {
  const { t } = useTranslation()

  const teamMembers = [
    {
      id: 'architect',
      icon: <User size={48} />,
      name: t('origins.architect.name'),
      role: t('origins.architect.role'),
      title: t('origins.architect.title'),
      desc: t('origins.architect.desc'),
      clearance: 'LEVEL 10',
      status: 'ACTIVE'
    },
    {
      id: 'sentinel',
      icon: <Cpu size={48} />,
      name: t('origins.sentinel.name'),
      role: t('origins.sentinel.role'),
      title: t('origins.sentinel.title'),
      desc: t('origins.sentinel.desc'),
      clearance: 'LEVEL 9',
      status: 'ONLINE'
    },
    {
      id: 'drjoe',
      icon: <FlaskConical size={48} />,
      name: t('origins.drjoe.name'),
      role: t('origins.drjoe.role'),
      title: t('origins.drjoe.title'),
      desc: t('origins.drjoe.desc'),
      clearance: 'LEVEL 8',
      status: 'ACTIVE'
    }
  ]

  const values = [
    {
      icon: <Shield size={32} />,
      title: t('origins.values.ethics'),
      desc: t('origins.values.ethicsDesc')
    },
    {
      icon: <Target size={32} />,
      title: t('origins.values.integrity'),
      desc: t('origins.values.integrityDesc')
    },
    {
      icon: <Lightbulb size={32} />,
      title: t('origins.values.innovation'),
      desc: t('origins.values.innovationDesc')
    }
  ]

  const timeline = [
    { year: t('origins.timeline.t2020.year'), event: t('origins.timeline.t2020.event'), desc: t('origins.timeline.t2020.desc') },
    { year: t('origins.timeline.t2021.year'), event: t('origins.timeline.t2021.event'), desc: t('origins.timeline.t2021.desc') },
    { year: t('origins.timeline.t2022.year'), event: t('origins.timeline.t2022.event'), desc: t('origins.timeline.t2022.desc') },
    { year: t('origins.timeline.t2023.year'), event: t('origins.timeline.t2023.event'), desc: t('origins.timeline.t2023.desc') },
    { year: t('origins.timeline.t2024.year'), event: t('origins.timeline.t2024.event'), desc: t('origins.timeline.t2024.desc') }
  ]

  return (
    <div className="origins-page">
      <section className="origins-hero">
        <div className="origins-background">
          <div className="data-streams" />
        </div>
        <motion.div 
          className="origins-hero-content"
          initial={{ opacity: 0, y: 50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
        >
          <h1 className="section-title">{t('origins.title')}</h1>
          <p className="section-subtitle">{t('origins.subtitle')}</p>
        </motion.div>
      </section>

      <section className="team-section section">
        <motion.h2 
          className="classified-header"
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
        >
          <span className="classified-tag">CLASSIFIED</span>
          {t('origins.team')}
        </motion.h2>
        
        <div className="team-grid">
          {teamMembers.map((member, index) => (
            <motion.div
              key={member.id}
              className="personnel-file glass-panel"
              initial={{ opacity: 0, y: 50, rotateX: -10 }}
              whileInView={{ opacity: 1, y: 0, rotateX: 0 }}
              transition={{ duration: 0.6, delay: index * 0.2 }}
              viewport={{ once: true }}
              whileHover={{ 
                scale: 1.02,
                boxShadow: '0 0 40px rgba(0, 255, 136, 0.2)'
              }}
            >
              <div className="file-header">
                <div className="file-id">FILE #{String(index + 1).padStart(3, '0')}</div>
                <div className={`file-status ${member.status.toLowerCase()}`}>{member.status}</div>
              </div>
              
              <div className="file-photo">
                <div className="photo-frame">
                  {member.icon}
                </div>
                <div className="clearance-badge">{member.clearance}</div>
              </div>
              
              <div className="file-info">
                <h3 className="personnel-name">{member.name}</h3>
                <p className="personnel-role">{member.role}</p>
                <p className="personnel-title">{member.title}</p>
                <div className="cyber-line" />
                <p className="personnel-desc">{member.desc}</p>
              </div>
              
              <div className="file-footer">
                <div className="scan-effect" />
              </div>
            </motion.div>
          ))}
        </div>
      </section>

      <section className="timeline-section">
        <div className="section">
          <motion.h2 
            className="section-title"
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
          >
            {t('origins.timeline.title')}
          </motion.h2>
          
          <div className="timeline">
            {timeline.map((item, index) => (
              <motion.div
                key={index}
                className="timeline-item"
                initial={{ opacity: 0, x: index % 2 === 0 ? -50 : 50 }}
                whileInView={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                viewport={{ once: true }}
              >
                <div className="timeline-marker">
                  <span className="year">{item.year}</span>
                </div>
                <div className="timeline-content glass-panel">
                  <h4>{item.event}</h4>
                  <p>{item.desc}</p>
                </div>
              </motion.div>
            ))}
            <div className="timeline-line" />
          </div>
        </div>
      </section>

      <section className="values-section section">
        <motion.h2 
          className="section-title"
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
        >
          {t('origins.values.title')}
        </motion.h2>
        
        <div className="values-grid">
          {values.map((value, index) => (
            <motion.div
              key={index}
              className="value-card"
              initial={{ opacity: 0, scale: 0.9 }}
              whileInView={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.5, delay: index * 0.15 }}
              viewport={{ once: true }}
              whileHover={{ y: -5 }}
            >
              <div className="value-icon">{value.icon}</div>
              <h3>{value.title}</h3>
              <p>{value.desc}</p>
            </motion.div>
          ))}
        </div>
      </section>
    </div>
  )
}

export default Origins
