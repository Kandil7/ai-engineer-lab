# Deployment — Cloud Infrastructure

Cloud deployment strategy, Kubernetes manifests, monitoring setup, and scaling configuration
for the AI Engineer Lab and ThanaweyaGPT platform.

---

## Deployment Strategy

### Environment Tiers

| Tier       | Infrastructure     | Purpose                  | Auto-deploy |
| ---------- | ------------------ | ------------------------ | ----------- |
| Local      | Docker Compose     | Development             | No          |
| Staging    | Single-node K8s    | Pre-production testing  | Yes (main)  |
| Production | Multi-node K8s     | Live traffic            | Manual gate |

### Deployment Flow

```
Code Push → CI Tests → Docker Build → Push to Registry → Deploy to Staging
    → Smoke Tests → Manual Approval → Deploy to Production → Canary → Full Rollout
```

---

## Kubernetes Manifests

### Directory Structure

```
infra/k8s/
├── base/                    # Shared resources
│   ├── namespace.yml
│   ├── configmap.yml
│   └── secrets.yml
├── auth-service/
│   ├── deployment.yml
│   ├── service.yml
│   └── hpa.yml
├── ai-service/
│   ├── deployment.yml
│   ├── service.yml
│   └── hpa.yml
├── postgres/
│   ├── statefulset.yml
│   ├── service.yml
│   └── pvc.yml
└── ingress/
    └── ingress.yml
```

### Example: Auth Service Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: auth-service
  namespace: fslab
spec:
  replicas: 2
  selector:
    matchLabels:
      app: auth-service
  template:
    metadata:
      labels:
        app: auth-service
    spec:
      containers:
        - name: auth-service
          image: ghcr.io/org/fslab/auth-service:latest
          ports:
            - containerPort: 8080
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: db-credentials
                  key: url
          resources:
            requests:
              memory: "128Mi"
              cpu: "100m"
            limits:
              memory: "256Mi"
              cpu: "500m"
          livenessProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 10
            periodSeconds: 15
          readinessProbe:
            httpGet:
              path: /ready
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 10
```

---

## Monitoring Setup

### Metrics Stack

| Component       | Purpose                    | Port    |
| --------------- | -------------------------- | ------- |
| Prometheus      | Metrics collection         | 9090    |
| Grafana         | Metrics visualization      | 3000    |
| Alertmanager    | Alert routing              | 9093    |
| Loki            | Log aggregation            | 3100    |

### Key Metrics to Monitor

| Metric                      | Alert Threshold       |
| --------------------------- | --------------------- |
| Request latency (p95)       | > 2 seconds           |
| Error rate (5xx)            | > 1%                  |
| CPU utilization             | > 80%                 |
| Memory utilization          | > 85%                 |
| Pod restart count           | > 3 in 10 minutes     |
| Database connections        | > 80% of pool         |
| Redis memory                | > 90% of limit        |

### Alert Rules

```yaml
groups:
  - name: fslab-alerts
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.01
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
          
      - alert: HighLatency
        expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 2
        for: 5m
        labels:
          severity: warning
```

---

## Scaling Configuration

### Horizontal Pod Autoscaler (HPA)

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: auth-service-hpa
  namespace: fslab
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: auth-service
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
```

### Scaling Triggers

| Trigger             | Action                          |
| ------------------- | ------------------------------- |
| CPU > 70%           | Scale up by 1 replica           |
| CPU < 30%           | Scale down by 1 replica         |
| Memory > 80%        | Scale up by 1 replica           |
| Custom metric (RPS) | Scale based on requests/second  |

### Database Scaling

- **Read replicas** for read-heavy workloads
- **Connection pooling** (PgBouncer) for connection management
- **Partitioning** for large tables (messages, embeddings)

---

## Cloud Provider Options

| Provider    | Best For                | Services Used                    |
| ----------- | ----------------------- | -------------------------------- |
| AWS         | Full-featured           | EKS, RDS, ElastiCache, S3       |
| GCP         | AI/ML integration       | GKE, Cloud SQL, Memorystore     |
| Azure       | Enterprise              | AKS, Azure SQL, Azure Cache    |
| DigitalOcean| Cost-effective          | DOKS, Managed PG, Managed Redis |

### Recommended for ThanaweyaGPT

**AWS** or **GCP** — both have strong Kubernetes managed services and AI/ML tooling.
Start with managed Kubernetes (EKS/GKE) to avoid cluster management overhead.

---

## Disaster Recovery

### Backup Strategy

| Component      | Backup Method    | Frequency  | Retention |
| -------------- | ---------------- | ---------- | --------- |
| PostgreSQL     | pg_dump + WAL    | Hourly     | 7 days    |
| Redis          | RDB snapshots    | Every 60s  | 24 hours  |
| Qdrant         | Snapshot API     | Daily      | 30 days   |
| Kubernetes     | etcd backup      | Hourly     | 7 days    |

### Recovery Time Objectives

| Scenario               | RTO    | RPO    |
| ---------------------- | ------ | ------ |
| Pod crash              | < 1 min| 0      |
| Node failure           | < 5 min| 0      |
| Database corruption    | < 30 min| < 1 hr |
| Full region outage     | < 1 hr | < 5 min|

---

## Getting Started

```bash
# Apply base manifests
kubectl apply -f infra/k8s/base/

# Deploy auth-service
kubectl apply -f infra/k8s/auth-service/

# Check deployment status
kubectl get pods -n fslab
kubectl get hpa -n fslab

# View logs
kubectl logs -f deployment/auth-service -n fslab

# Scale manually
kubectl scale deployment auth-service --replicas=3 -n fslab

# Port-forward for local access
kubectl port-forward svc/auth-service 8080:8080 -n fslab
```
