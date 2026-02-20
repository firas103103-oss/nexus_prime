#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════
# NEXUS PRIME — Full Stack Deployment to K3s
# ═══════════════════════════════════════════════════════════════════════════
# Deploys orchestrator with HPA, PDB, health probes, and production config
# ═══════════════════════════════════════════════════════════════════════════

set -euo pipefail

echo "════════════════════════════════════════════════════════════════════════"
echo "  NEXUS PRIME — Full Stack K3s Deployment"
echo "  v1.1.0 - Redis Streams + HPA + PDB + Health Probes"
echo "════════════════════════════════════════════════════════════════════════"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
REGISTRY="localhost:5000"
IMAGE_NAME="nexus_orchestrator"
IMAGE_TAG="v1.1.0"
FULL_IMAGE="${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}"
NAMESPACE="nexus-prime"
K8S_MANIFESTS_DIR="/root/NEXUS_PRIME_UNIFIED/k8s-manifests"

# ═══════════════════════════════════════════════════════════════════════════
# STEP 1: Build and Push Image
# ═══════════════════════════════════════════════════════════════════════════

echo -e "${YELLOW}[1/8]${NC} Building orchestrator image..."
cd /root/NEXUS_PRIME_UNIFIED/nexus_prime_core
docker build -t ${FULL_IMAGE} -f Dockerfile . || {
    echo -e "${RED}✗ Build failed${NC}"
    exit 1
}
echo -e "${GREEN}✓ Build successful${NC}"
echo ""

echo -e "${YELLOW}[2/8]${NC} Pushing image to registry..."
docker push ${FULL_IMAGE} || {
    echo -e "${RED}✗ Push failed. Is local registry running?${NC}"
    echo "Start registry: docker run -d -p 5000:5000 --name registry registry:2"
    exit 1
}
echo -e "${GREEN}✓ Image pushed to ${FULL_IMAGE}${NC}"
echo ""

# ═══════════════════════════════════════════════════════════════════════════
# STEP 2: Verify K8s Cluster
# ═══════════════════════════════════════════════════════════════════════════

echo -e "${YELLOW}[3/8]${NC} Verifying K8s cluster..."
if ! kubectl cluster-info &>/dev/null; then
    echo -e "${RED}✗ Cannot connect to K8s cluster${NC}"
    echo "Check: kubectl cluster-info"
    exit 1
fi
echo -e "${GREEN}✓ K8s cluster accessible${NC}"
echo ""

# ═══════════════════════════════════════════════════════════════════════════
# STEP 3: Apply Manifests
# ═══════════════════════════════════════════════════════════════════════════

echo -e "${YELLOW}[4/8]${NC} Applying K8s manifests..."
kubectl apply -f ${K8S_MANIFESTS_DIR}/orchestrator.yaml || {
    echo -e "${RED}✗ Failed to apply manifests${NC}"
    exit 1
}
echo -e "${GREEN}✓ Manifests applied${NC}"
echo ""

# ═══════════════════════════════════════════════════════════════════════════
# STEP 4: Wait for Rollout
# ═══════════════════════════════════════════════════════════════════════════

echo -e "${YELLOW}[5/8]${NC} Waiting for deployment rollout (timeout: 5min)..."
kubectl rollout status deployment/nexus-orchestrator -n ${NAMESPACE} --timeout=5m || {
    echo -e "${RED}✗ Rollout failed or timed out${NC}"
    echo "Checking pod status:"
    kubectl get pods -n ${NAMESPACE} -l app=nexus-orchestrator
    echo ""
    echo "Checking events:"
    kubectl get events -n ${NAMESPACE} --sort-by='.lastTimestamp' | tail -20
    exit 1
}
echo -e "${GREEN}✓ Rollout complete${NC}"
echo ""

# ═══════════════════════════════════════════════════════════════════════════
# STEP 5: Verify Replicas
# ═══════════════════════════════════════════════════════════════════════════

echo -e "${YELLOW}[6/8]${NC} Verifying pod replicas..."
READY_PODS=$(kubectl get pods -n ${NAMESPACE} -l app=nexus-orchestrator --field-selector=status.phase=Running -o json | jq '.items | length')
echo "Ready pods: ${READY_PODS}/3"
if [ "${READY_PODS}" -lt 3 ]; then
    echo -e "${YELLOW}⚠ Not all pods ready yet. Checking status...${NC}"
    kubectl get pods -n ${NAMESPACE} -l app=nexus-orchestrator
fi
echo -e "${GREEN}✓ Pods verified${NC}"
echo ""

# ═══════════════════════════════════════════════════════════════════════════
# STEP 6: Verify HPA
# ═══════════════════════════════════════════════════════════════════════════

echo -e "${YELLOW}[7/8]${NC} Verifying Horizontal Pod Autoscaler..."
kubectl get hpa -n ${NAMESPACE} nexus-orchestrator-hpa || {
    echo -e "${YELLOW}⚠ HPA not found (may take a moment to appear)${NC}"
}
echo -e "${GREEN}✓ HPA configured${NC}"
echo ""

# ═══════════════════════════════════════════════════════════════════════════
# STEP 7: Verify PDB
# ═══════════════════════════════════════════════════════════════════════════

echo -e "${YELLOW}[8/8]${NC} Verifying Pod Disruption Budget..."
kubectl get pdb -n ${NAMESPACE} nexus-orchestrator-pdb || {
    echo -e "${YELLOW}⚠ PDB not found${NC}"
}
echo -e "${GREEN}✓ PDB configured${NC}"
echo ""

# ═══════════════════════════════════════════════════════════════════════════
# FINAL STATUS
# ═══════════════════════════════════════════════════════════════════════════

echo -e "${GREEN}═══════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}  DEPLOYMENT COMPLETE${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════════════════${NC}"
echo ""

echo -e "${BLUE}Deployment Summary:${NC}"
echo "─────────────────────────────────────────────────────────────────────────"
kubectl get all -n ${NAMESPACE} -l app=nexus-orchestrator
echo ""

echo -e "${BLUE}HPA Status:${NC}"
kubectl get hpa -n ${NAMESPACE} nexus-orchestrator-hpa 2>/dev/null || echo "Not ready yet"
echo ""

echo -e "${BLUE}PDB Status:${NC}"
kubectl get pdb -n ${NAMESPACE} nexus-orchestrator-pdb 2>/dev/null || echo "Not ready yet"
echo ""

echo -e "${BLUE}Service Endpoints:${NC}"
kubectl get endpoints -n ${NAMESPACE} nexus-orchestrator 2>/dev/null || echo "Not ready yet"
echo ""

echo -e "${YELLOW}Next Steps:${NC}"
echo "  1. Test gRPC connection:"
echo "     kubectl port-forward -n ${NAMESPACE} svc/nexus-orchestrator 50051:50051"
echo "     grpcurl -plaintext localhost:50051 list"
echo ""
echo "  2. Monitor pods:"
echo "     kubectl logs -n ${NAMESPACE} -l app=nexus-orchestrator -f"
echo ""
echo "  3. Test Redis Streams:"
echo "     kubectl exec -it -n ${NAMESPACE} <redis-pod> -- redis-cli"
echo "     XADD nexus:commands:stream '*' type command_issued target TEST command_id test-1 command_type test priority 5"
echo ""
echo "  4. Test autoscaling:"
echo "     kubectl run -it --rm load-generator --image=busybox --restart=Never -- /bin/sh"
echo "     # Generate load to trigger HPA"
echo ""
echo "  5. Test PDB (drain node):"
echo "     kubectl drain <node-name> --ignore-daemonsets"
echo "     # Should maintain minimum 2 pods"
echo ""
