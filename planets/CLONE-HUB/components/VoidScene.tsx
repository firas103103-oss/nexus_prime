
import React, { useRef, useMemo } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import * as THREE from 'three';

const NeuralCore = ({ mode, color }: { mode: string; color: string }) => {
  const outerRef = useRef<THREE.Mesh>(null!);
  const innerRef = useRef<THREE.Mesh>(null!);
  const groupRef = useRef<THREE.Group>(null!);
  const isActive = mode === 'GRAVITY_WELL_ACTIVE';

  useFrame((state, delta) => {
    const t = state.clock.getElapsedTime();
    const speed = isActive ? 0.8 : 0.2;
    
    // Core Rotation
    outerRef.current.rotation.y += delta * speed;
    outerRef.current.rotation.x = Math.sin(t * 0.2) * 0.1;
    innerRef.current.rotation.y -= delta * speed * 1.5;
    
    // Pulse Effect
    const pulse = Math.sin(t * (isActive ? 2 : 0.5)) * (isActive ? 0.1 : 0.02);
    outerRef.current.scale.setScalar(1.8 + pulse);
    innerRef.current.scale.setScalar(0.9 - pulse);

    // Floating Animation (Replica of <Float>)
    if (groupRef.current) {
        groupRef.current.position.y = Math.sin(t * 1.5) * 0.1; 
        groupRef.current.rotation.z = Math.sin(t * 0.5) * 0.05;
    }
  });

  const outerMat = useMemo(() => new THREE.MeshPhysicalMaterial({
    color: color, wireframe: true, transparent: true, opacity: isActive ? 0.4 : 0.1,
    transmission: 0.9, roughness: 0, metalness: 0.8
  }), [color, isActive]);

  const innerMat = useMemo(() => new THREE.MeshBasicMaterial({
    color: color, wireframe: true, transparent: true, opacity: isActive ? 0.9 : 0.4,
    blending: THREE.AdditiveBlending
  }), [color, isActive]);

  return (
    <group ref={groupRef}>
      <mesh ref={outerRef} material={outerMat}>
        <icosahedronGeometry args={[1, 1]} />
      </mesh>
      <mesh ref={innerRef} material={innerMat}>
        <icosahedronGeometry args={[1, 2]} />
      </mesh>
      <pointLight distance={3} intensity={isActive ? 3 : 1} color={color} />
    </group>
  );
};

export const VoidScene = ({ visualMode, accentColor }: any) => {
  return (
    <div className="absolute inset-0 z-0 bg-[#020202] transition-colors duration-1000">
      <Canvas camera={{ position: [0, 0, 7], fov: 50 }}>
        <ambientLight intensity={0.05} />
        <NeuralCore mode={visualMode} color={accentColor} />
        <group position={[0, -3.5, 0]} rotation={[Math.PI / 2.2, 0, 0]}>
             <gridHelper args={[40, 40, accentColor, '#222222']} />
        </group>
        <fog attach="fog" args={['#020202', 4, 18]} />
      </Canvas>
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,transparent_20%,#000_100%)] pointer-events-none" />
    </div>
  );
};
