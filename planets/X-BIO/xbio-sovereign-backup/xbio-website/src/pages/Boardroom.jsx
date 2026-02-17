import { motion } from 'framer-motion'
import { useTranslation } from 'react-i18next'
import { Users, Cpu, Shield, Brain, Radio, Target } from 'lucide-react'
import './Boardroom.css'

function Boardroom() {
  const { t } = useTranslation()

  const agents = [
    { name: "SENTINEL PRIME", role: t('boardroom.agents.sentinelPrime'), tier: "SUPREME", icon: <Cpu size={24} />, division: "Supreme Command" },
    { name: "DR. JOE", role: t('boardroom.agents.drJoe'), tier: "HEAD", icon: <Brain size={24} />, division: "R&D Division" },
    { name: "ENG. VECTOR", role: t('boardroom.agents.engVector'), tier: "OFFICER", icon: <Cpu size={24} />, division: "R&D Division" },
    { name: "DR. QUANT", role: t('boardroom.agents.drQuant'), tier: "HEAD", icon: <Brain size={24} />, division: "R&D Division" },
    { name: "DR. SIGMA", role: t('boardroom.agents.drSigma'), tier: "OFFICER", icon: <Target size={24} />, division: "R&D Division" },
    { name: "CMDR. SWIFT", role: t('boardroom.agents.cmdrSwift'), tier: "HEAD", icon: <Radio size={24} />, division: "Operations Division" },
    { name: "OFFICER HERTZ", role: t('boardroom.agents.officerHertz'), tier: "OFFICER", icon: <Radio size={24} />, division: "Operations Division" },
    { name: "CHIEF FORGE", role: t('boardroom.agents.chiefForge'), tier: "OFFICER", icon: <Cpu size={24} />, division: "Operations Division" },
    { name: "THE WARDEN", role: t('boardroom.agents.theWarden'), tier: "HEAD", icon: <Shield size={24} />, division: "Security & Legal" },
    { name: "COUNSELOR LOGIC", role: t('boardroom.agents.counselorLogic'), tier: "HEAD", icon: <Shield size={24} />, division: "Security & Legal" },
    { name: "WARDEN PRIME", role: t('boardroom.agents.wardenPrime'), tier: "OFFICER", icon: <Shield size={24} />, division: "Security & Legal" },
    { name: "MR. LEDGER", role: t('boardroom.agents.mrLedger'), tier: "EXECUTIVE", icon: <Target size={24} />, division: "Commercial & Admin" },
    { name: "CHIEF SOURCE", role: t('boardroom.agents.chiefSource'), tier: "OFFICER", icon: <Target size={24} />, division: "Commercial & Admin" },
    { name: "COUNSELOR PACT", role: t('boardroom.agents.counselorPact'), tier: "HEAD", icon: <Shield size={24} />, division: "Commercial & Admin" },
    { name: "AMBASSADOR NEXUS", role: t('boardroom.agents.ambassadorNexus'), tier: "HEAD", icon: <Users size={24} />, division: "Commercial & Admin" },
    { name: "AMBASSADOR NOVA", role: t('boardroom.agents.ambassadorNova'), tier: "HEAD", icon: <Users size={24} />, division: "Commercial & Admin" },
    { name: "ADMIN ORACLE", role: t('boardroom.agents.adminOracle'), tier: "HEAD", icon: <Brain size={24} />, division: "Commercial & Admin" },
    { name: "X-BIO CORE", role: t('boardroom.agents.xbioCore'), tier: "SYSTEM", icon: <Cpu size={24} />, division: "System" }
  ]

  const getTierColor = (tier) => {
    switch(tier) {
      case 'SUPREME': return '#ffd700'
      case 'EXECUTIVE': return '#00ff88'
      case 'HEAD': return '#00aaff'
      case 'OFFICER': return '#ff8800'
      case 'SYSTEM': return '#aa44ff'
      default: return '#00ff88'
    }
  }

  return (
    <div className="boardroom-page">
      <section className="boardroom-hero">
        <motion.div
          className="hero-badge"
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5 }}
        >
          <Users size={20} />
          {t('boardroom.badge')}
        </motion.div>
        
        <motion.h1
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
        >
          {t('boardroom.title')}
        </motion.h1>
        
        <motion.p
          className="hero-subtitle"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.3 }}
        >
          {t('boardroom.subtitle')}
        </motion.p>
      </section>

      <section className="agents-section">
        <motion.h2
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          transition={{ duration: 0.5 }}
        >
          {t('boardroom.agentsTitle')}
        </motion.h2>

        <div className="agents-grid">
          {agents.map((agent, index) => (
            <motion.div
              key={agent.name}
              className="agent-card"
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.4, delay: index * 0.05 }}
              whileHover={{ scale: 1.02, boxShadow: `0 0 30px ${getTierColor(agent.tier)}40` }}
            >
              <div className="agent-icon" style={{ color: getTierColor(agent.tier) }}>
                {agent.icon}
              </div>
              <div className="agent-info">
                <h3>{agent.name}</h3>
                <p>{agent.role}</p>
              </div>
              <span className="tier-badge" style={{ 
                backgroundColor: `${getTierColor(agent.tier)}20`,
                color: getTierColor(agent.tier),
                borderColor: getTierColor(agent.tier)
              }}>
                {agent.tier}
              </span>
            </motion.div>
          ))}
        </div>
      </section>

      <section className="features-section">
        <motion.h2
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          transition={{ duration: 0.5 }}
        >
          {t('boardroom.featuresTitle')}
        </motion.h2>

        <div className="features-grid">
          <motion.div 
            className="feature-card"
            initial={{ opacity: 0, x: -20 }}
            whileInView={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5 }}
          >
            <h3>{t('boardroom.feature1Title')}</h3>
            <p>{t('boardroom.feature1Desc')}</p>
          </motion.div>
          <motion.div 
            className="feature-card"
            initial={{ opacity: 0, x: 20 }}
            whileInView={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.1 }}
          >
            <h3>{t('boardroom.feature2Title')}</h3>
            <p>{t('boardroom.feature2Desc')}</p>
          </motion.div>
          <motion.div 
            className="feature-card"
            initial={{ opacity: 0, x: -20 }}
            whileInView={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
          >
            <h3>{t('boardroom.feature3Title')}</h3>
            <p>{t('boardroom.feature3Desc')}</p>
          </motion.div>
          <motion.div 
            className="feature-card"
            initial={{ opacity: 0, x: 20 }}
            whileInView={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.3 }}
          >
            <h3>{t('boardroom.feature4Title')}</h3>
            <p>{t('boardroom.feature4Desc')}</p>
          </motion.div>
        </div>
      </section>

      <section className="access-section">
        <motion.div
          className="access-card"
          initial={{ opacity: 0, scale: 0.95 }}
          whileInView={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5 }}
        >
          <h2>{t('boardroom.accessTitle')}</h2>
          <p>{t('boardroom.accessDesc')}</p>
          <div className="access-info">
            <code>streamlit run main.py --server.port 5000</code>
          </div>
        </motion.div>
      </section>
    </div>
  )
}

export default Boardroom
