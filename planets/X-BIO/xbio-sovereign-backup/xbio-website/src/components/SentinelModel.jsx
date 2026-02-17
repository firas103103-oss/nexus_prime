import { useRef, useState, useEffect, Suspense } from 'react'
import { Canvas, useFrame } from '@react-three/fiber'
import { OrbitControls, Float, MeshDistortMaterial } from '@react-three/drei'
import { motion } from 'framer-motion'
import './SentinelModel.css'

function CoreSphere({ isExploded }) {
  const meshRef = useRef()
  
  useFrame((state) => {
    if (meshRef.current) {
      meshRef.current.rotation.y += 0.005
    }
  })
  
  return (
    <Float speed={2} rotationIntensity={0.5} floatIntensity={0.5}>
      <mesh ref={meshRef} position={[0, 0, 0]}>
        <sphereGeometry args={[1, 64, 64]} />
        <MeshDistortMaterial
          color="#00ff88"
          attach="material"
          distort={0.3}
          speed={2}
          roughness={0.2}
          metalness={0.8}
          emissive="#00ff88"
          emissiveIntensity={0.3}
        />
      </mesh>
    </Float>
  )
}

function EyeModule({ isExploded }) {
  const position = isExploded ? [2.5, 1, 0] : [0, 0.8, 0.8]
  
  return (
    <Float speed={3} rotationIntensity={0.3}>
      <group position={position}>
        <mesh>
          <sphereGeometry args={[0.25, 32, 32]} />
          <meshStandardMaterial 
            color="#ff4444" 
            emissive="#ff4444"
            emissiveIntensity={0.5}
            metalness={0.9}
            roughness={0.1}
          />
        </mesh>
        <mesh position={[0, 0, 0.2]}>
          <ringGeometry args={[0.15, 0.2, 32]} />
          <meshStandardMaterial 
            color="#ffffff" 
            emissive="#ffffff"
            emissiveIntensity={0.3}
          />
        </mesh>
      </group>
    </Float>
  )
}

function EarModule({ isExploded, side }) {
  const xPos = side === 'left' ? -0.9 : 0.9
  const explodedX = side === 'left' ? -2.5 : 2.5
  const position = isExploded ? [explodedX, 0, -1] : [xPos, 0, 0]
  
  return (
    <Float speed={2.5} rotationIntensity={0.2}>
      <group position={position}>
        <mesh rotation={[0, side === 'left' ? Math.PI / 2 : -Math.PI / 2, 0]}>
          <torusGeometry args={[0.2, 0.05, 16, 32]} />
          <meshStandardMaterial 
            color="#00ccff" 
            emissive="#00ccff"
            emissiveIntensity={0.5}
            metalness={0.8}
            roughness={0.2}
          />
        </mesh>
        <mesh rotation={[0, side === 'left' ? Math.PI / 2 : -Math.PI / 2, 0]}>
          <torusGeometry args={[0.3, 0.03, 16, 32]} />
          <meshStandardMaterial 
            color="#00ccff" 
            emissive="#00ccff"
            emissiveIntensity={0.3}
            metalness={0.8}
            roughness={0.2}
          />
        </mesh>
      </group>
    </Float>
  )
}

function NoseModule({ isExploded }) {
  const position = isExploded ? [0, -2, 1.5] : [0, -0.5, 0.7]
  
  return (
    <Float speed={2} rotationIntensity={0.4}>
      <group position={position}>
        <mesh>
          <coneGeometry args={[0.15, 0.4, 6]} />
          <meshStandardMaterial 
            color="#ffaa00" 
            emissive="#ffaa00"
            emissiveIntensity={0.5}
            metalness={0.7}
            roughness={0.3}
          />
        </mesh>
      </group>
    </Float>
  )
}

function OuterRing() {
  const ringRef = useRef()
  
  useFrame((state) => {
    if (ringRef.current) {
      ringRef.current.rotation.z += 0.003
      ringRef.current.rotation.x = Math.sin(state.clock.elapsedTime * 0.5) * 0.1
    }
  })
  
  return (
    <group ref={ringRef}>
      <mesh>
        <torusGeometry args={[1.8, 0.02, 16, 100]} />
        <meshStandardMaterial 
          color="#00ff88" 
          emissive="#00ff88"
          emissiveIntensity={0.3}
          metalness={1}
          roughness={0}
          transparent
          opacity={0.8}
        />
      </mesh>
      <mesh rotation={[Math.PI / 2, 0, 0]}>
        <torusGeometry args={[1.6, 0.015, 16, 100]} />
        <meshStandardMaterial 
          color="#00ff88" 
          emissive="#00ff88"
          emissiveIntensity={0.2}
          metalness={1}
          roughness={0}
          transparent
          opacity={0.5}
        />
      </mesh>
    </group>
  )
}

function Particles() {
  const particlesRef = useRef()
  const count = 100
  
  const positions = new Float32Array(count * 3)
  for (let i = 0; i < count; i++) {
    const radius = 2 + Math.random() * 2
    const theta = Math.random() * Math.PI * 2
    const phi = Math.random() * Math.PI
    
    positions[i * 3] = radius * Math.sin(phi) * Math.cos(theta)
    positions[i * 3 + 1] = radius * Math.sin(phi) * Math.sin(theta)
    positions[i * 3 + 2] = radius * Math.cos(phi)
  }
  
  useFrame((state) => {
    if (particlesRef.current) {
      particlesRef.current.rotation.y += 0.001
    }
  })
  
  return (
    <points ref={particlesRef}>
      <bufferGeometry>
        <bufferAttribute
          attach="attributes-position"
          count={count}
          array={positions}
          itemSize={3}
        />
      </bufferGeometry>
      <pointsMaterial
        size={0.03}
        color="#00ff88"
        transparent
        opacity={0.6}
        sizeAttenuation
      />
    </points>
  )
}

function Scene({ isExploded }) {
  return (
    <>
      <ambientLight intensity={0.2} />
      <pointLight position={[10, 10, 10]} intensity={1} color="#00ff88" />
      <pointLight position={[-10, -10, -10]} intensity={0.5} color="#00ccff" />
      <spotLight position={[0, 5, 0]} intensity={0.5} color="#ffffff" angle={0.5} />
      
      <CoreSphere isExploded={isExploded} />
      <EyeModule isExploded={isExploded} />
      <EarModule isExploded={isExploded} side="left" />
      <EarModule isExploded={isExploded} side="right" />
      <NoseModule isExploded={isExploded} />
      <OuterRing />
      <Particles />
      
      <OrbitControls 
        enableZoom={false}
        enablePan={false}
        autoRotate
        autoRotateSpeed={0.5}
        maxPolarAngle={Math.PI / 1.5}
        minPolarAngle={Math.PI / 3}
      />
    </>
  )
}

function FallbackVisual({ isExploded }) {
  return (
    <div className="sentinel-fallback">
      <motion.div 
        className="fallback-outer-ring"
        animate={{ rotate: 360 }}
        transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
      />
      <motion.div 
        className="fallback-inner-ring"
        animate={{ rotate: -360 }}
        transition={{ duration: 15, repeat: Infinity, ease: "linear" }}
      />
      <motion.div 
        className="fallback-core"
        animate={{ 
          scale: [1, 1.1, 1],
          boxShadow: [
            '0 0 30px rgba(0, 255, 136, 0.5)',
            '0 0 60px rgba(0, 255, 136, 0.8)',
            '0 0 30px rgba(0, 255, 136, 0.5)'
          ]
        }}
        transition={{ duration: 2, repeat: Infinity }}
      >
        <span>X</span>
      </motion.div>
      
      {isExploded && (
        <>
          <motion.div 
            className="fallback-sense eye"
            initial={{ x: 0, y: 0 }}
            animate={{ x: 80, y: -60 }}
            transition={{ duration: 0.5 }}
          />
          <motion.div 
            className="fallback-sense ear-left"
            initial={{ x: 0, y: 0 }}
            animate={{ x: -100, y: 0 }}
            transition={{ duration: 0.5 }}
          />
          <motion.div 
            className="fallback-sense ear-right"
            initial={{ x: 0, y: 0 }}
            animate={{ x: 100, y: 0 }}
            transition={{ duration: 0.5 }}
          />
          <motion.div 
            className="fallback-sense nose"
            initial={{ x: 0, y: 0 }}
            animate={{ x: 0, y: 80 }}
            transition={{ duration: 0.5 }}
          />
        </>
      )}
      
      <div className="fallback-particles">
        {[...Array(20)].map((_, i) => (
          <motion.div
            key={i}
            className="particle"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
            }}
            animate={{
              opacity: [0.2, 0.8, 0.2],
              scale: [0.5, 1, 0.5]
            }}
            transition={{
              duration: 2 + Math.random() * 2,
              repeat: Infinity,
              delay: Math.random() * 2
            }}
          />
        ))}
      </div>
    </div>
  )
}

function SentinelModel({ isExploded = false, className = '' }) {
  const [webglSupported, setWebglSupported] = useState(true)
  
  useEffect(() => {
    try {
      const canvas = document.createElement('canvas')
      const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl')
      setWebglSupported(!!gl)
    } catch (e) {
      setWebglSupported(false)
    }
  }, [])

  if (!webglSupported) {
    return (
      <div className={`sentinel-model ${className}`} style={{ width: '100%', height: '100%' }}>
        <FallbackVisual isExploded={isExploded} />
      </div>
    )
  }

  return (
    <div className={`sentinel-model ${className}`} style={{ width: '100%', height: '100%' }}>
      <Suspense fallback={<FallbackVisual isExploded={isExploded} />}>
        <Canvas
          camera={{ position: [0, 0, 5], fov: 45 }}
          gl={{ antialias: true, alpha: true }}
          style={{ background: 'transparent' }}
          onCreated={({ gl }) => {
            if (!gl.capabilities.isWebGL2 && !gl.capabilities.isWebGL) {
              setWebglSupported(false)
            }
          }}
        >
          <Scene isExploded={isExploded} />
        </Canvas>
      </Suspense>
    </div>
  )
}

export default SentinelModel
