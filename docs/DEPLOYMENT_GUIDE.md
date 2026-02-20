# NEXUS PRIME Deployment Guide

Complete guide for deploying NEXUS PRIME in different environments.

---

## 📋 Table of Contents

- [Docker Compose (Development)](#docker-compose)
- [Docker Compose (Production)](#docker-compose-production)
- [Kubernetes (K3s)](#kubernetes-k3s)
- [Kubernetes (Production)](#kubernetes-production)
- [Cloud Platforms](#cloud-platforms)
- [SSL/TLS Setup](#ssltls-setup)
- [Monitoring](#monitoring)
- [Backups](#backups)

---

## 🐳 Docker Compose

### Development Setup

```bash
git clone https://github.com/mrf103/nexus-prime.git
cd NEXUS_PRIME_UNIFIED

# Start all services
docker compose up -d

# View logs
docker compose logs -f

# Stop
docker compose down
```

### Production Setup

```bash
# 1. Clone repository
git clone https://github.com/mrf103/nexus-prime.git
cd NEXUS_PRIME_UNIFIED

# 2. Configure environment
cp .env.example .env
nano .env  # Edit variables

# 3. Secure passwords
export POSTGRES_PASSWORD=$(openssl rand -hex 32)
export JWT_SECRET=$(openssl rand -hex 32)
export SESSION_SECRET=$(openssl rand -hex 64)

# Update .env with generated values

# 4. Start services
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# 5. Verify
docker compose ps
curl localhost:8090/health
```

---

## ☸️ Kubernetes (K3s)

### Quick Install

```bash
# 1. Install K3s
curl -sfL https://get.k3s.io | sh -
sleep 10

# 2. Verify
kubectl get nodes

# 3. Deploy NEXUS PRIME
cd NEXUS_PRIME_UNIFIED
kubectl create namespace nexus-prime
kubectl apply -k k8s-manifests/

# 4. Check pods
kubectl get pods -n nexus-prime

# 5. Port forward for testing
kubectl port-forward -n nexus-prime svc/nexus-cortex 8090:8090 &
```

### Production K8s

```bash
# 1. Create secrets
kubectl create secret generic nexus-secrets \
  --from-literal=POSTGRES_PASSWORD=$(openssl rand -hex 32) \
  --from-literal=JWT_SECRET=$(openssl rand -hex 32) \
  -n nexus-prime

# 2. Deploy with Helm (if available)
helm install nexus-prime ./charts/nexus-prime \
  --namespace nexus-prime \
  --create-namespace

# 3. Configure Ingress
kubectl apply -f k8s-manifests/ingress.yaml

# 4. Enable auto-scaling
kubectl autoscale deployment nexus-cortex \
  --min=3 --max=10 --cpu-percent=70 \
  -n nexus-prime
```

---

## ☁️ Cloud Platforms

### AWS (ECS)

```bash
# 1. Build and push images
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin \
  <account-id>.dkr.ecr.us-east-1.amazonaws.com

docker tag nexus-cortex:latest \
  <account-id>.dkr.ecr.us-east-1.amazonaws.com/nexus-cortex:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/nexus-cortex:latest

# 2. Create ECS cluster
aws ecs create-cluster --cluster-name nexus-prime

# 3. Deploy task definition
aws ecs register-task-definition \
  --cli-input-json file://aws/ecs-task-definition.json

# 4. Create service
aws ecs create-service \
  --cluster nexus-prime \
  --service-name nexus-cortex \
  --task-definition nexus-cortex:1 \
  --desired-count 3
```

### Google Cloud (GKE)

```bash
# 1. Create GKE cluster
gcloud container clusters create nexus-prime \
  --num-nodes=3 \
  --machine-type=n1-standard-4

# 2. Get credentials
gcloud container clusters get-credentials nexus-prime

# 3. Deploy
kubectl apply -k k8s-manifests/
```

### Azure (AKS)

```bash
# 1. Create resource group
az group create --name nexus-prime-rg --location eastus

# 2. Create AKS cluster
az aks create \
  --resource-group nexus-prime-rg \
  --name nexus-prime-aks \
  --node-count 3 \
  --node-vm-size Standard_D4s_v3

# 3. Get credentials
az aks get-credentials \
  --resource-group nexus-prime-rg \
  --name nexus-prime-aks

# 4. Deploy
kubectl apply -k k8s-manifests/
```

---

## 🔒 SSL/TLS Setup

### Let's Encrypt (Cert-Manager)

```bash
# 1. Install cert-manager
kubectl apply -f \
  https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml

# 2. Create ClusterIssuer
cat <<EOF | kubectl apply -f -
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: admin@mrf103.com
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
    - http01:
        ingress:
          class: traefik
EOF

# 3. Update Ingress to use TLS
# See k8s-manifests/ingress.yaml
```

---

## 📊 Monitoring

### Prometheus + Grafana

```bash
#1. Install monitoring stack
helm repo add prometheus-community \
  https://prometheus-community.github.io/helm-charts

helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace

# 2. Access Grafana
kubectl port-forward -n monitoring \
  svc/prometheus-grafana 3001:80

# 3. Import dashboards
# - ID 16110: FastAPI
# - ID 11835: Redis
# - ID 9628: PostgreSQL
```

---

## 💾 Backups

### Automated Backup Script

```bash
#!/bin/bash
# /root/backup_nexus.sh

BACKUP_DIR=/root/nexus_prime_backups
DATE=$(date +%Y%m%d_%H%M)

# Backup database
docker exec nexus_db pg_dump -U postgres nexus_core > \
  $BACKUP_DIR/db_$DATE.sql

# Backup volumes
tar -czf $BACKUP_DIR/volumes_$DATE.tar.gz \
  ./data/db_data \
  ./data/ollama \
  ./data/redis_data \
  ./data/auth_keys

# Cleanup old backups (keep 7 days)
find $BACKUP_DIR -mtime +7 -delete

echo "Backup complete: $DATE"
```

### Schedule with Cron

```bash
# Add to crontab
crontab -e

# Daily at 3 AM
0 3 * * * /root/backup_nexus.sh
```

---

## 🚨 Health Checks

### Automated Monitoring

```bash
#!/bin/bash
# /root/health_check.sh

SERVICES=("cortex:8090" "auth:8003" "litellm:4000")

for service in "${SERVICES[@]}"; do
  IFS=':' read -r name port <<< "$service"
  status=$(curl -s -o /dev/null -w "%{http_code}" \
    http://localhost:$port/health)
  
  if [ "$status" != "200" ]; then
    echo "ALERT: $name is down (HTTP $status)"
    # Send alert (email, Slack, etc.)
  fi
done
```

---

## 📞 Support

For deployment issues:
- Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- Open GitHub Issue
- Email: support@mrf103.com

---

**Next:** [MONITORING.md](MONITORING.md) for detailed monitoring setup
