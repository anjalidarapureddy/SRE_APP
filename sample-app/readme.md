SRE Monitoring Stack – Practical Implementation (With Commands)
🚀 Project Overview

This project builds a complete monitoring + alerting + visualization pipeline using:

Flask app (simulated workload)
Node Exporter (system metrics)
Prometheus (metrics collection)
Alertmanager (alert routing)
Grafana (visual dashboards)
🧠 Architecture
Flask App ───────┐
                 ├──> Prometheus ───> Grafana
Node Exporter ───┘         │
                          ↓
                   Alertmanager
                   
🧱 Step 1 — Application Setup
📁 Create App
mkdir sample-app
cd sample-app
🧪 Create app.py
vi app.py

Paste your Flask + metrics code.

🎯 Why
Simulate real traffic
Generate latency & errors
Provide data for monitoring
🐳 Step 2 — Dockerize App
📄 Create Dockerfile
vi Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY app.py .

RUN pip install flask prometheus_client

EXPOSE 5000

CMD ["python", "app.py"]
🔨 Build Image
docker build -t sre-app .
▶️ Run Container
docker run -d -p 5000:5000 --name sre-app-container sre-app
🧪 Test App
curl http://localhost:5000
curl http://localhost:5000/slow
curl http://localhost:5000/error
curl http://localhost:5000/metrics
📊 Step 3 — System Metrics (Node Exporter)
▶️ Run Node Exporter
docker run -d -p 9100:9100 --name node-exporter prom/node-exporter
🧪 Verify
curl http://localhost:9100/metrics
🎯 Why

Monitor:

CPU
Memory
Disk
Network
📡 Step 4 — Prometheus Setup
📄 Create Config
vi prometheus.yml
global:
  scrape_interval: 5s

rule_files:
  - "alerts.yml"

scrape_configs:
  - job_name: "node_exporter"
    static_configs:
      - targets: ["<YOUR-IP>:9100"]

  - job_name: "flask_app"
    static_configs:
      - targets: ["<YOUR-IP>:5000"]
▶️ Run Prometheus
docker run -d \
  -p 9090:9090 \
  --name prometheus \
  -v $(pwd)/prometheus.yml:/etc/prometheus/prometheus.yml \
  -v $(pwd)/alerts.yml:/etc/prometheus/alerts.yml \
  prom/prometheus
🌐 Access
http://<YOUR-IP>:9090
📈 Step 5 — PromQL Testing
🧪 Run Queries
node_cpu_seconds_total
rate(app_requests_total[1m])
histogram_quantile(0.95, rate(app_request_latency_seconds_bucket[1m]))
🚨 Step 6 — Alerts Setup
📄 Create Alerts File
vi alerts.yml

Paste alert rules.

🔄 Reload Prometheus
docker restart prometheus

OR

curl -X POST http://localhost:9090/-/reload
🌐 Verify Alerts
http://<YOUR-IP>:9090/alerts
🔔 Step 7 — Alertmanager
📄 Create Config
vi alertmanager.yml
▶️ Run Alertmanager
docker run -d \
  -p 9093:9093 \
  --name alertmanager \
  -v $(pwd)/alertmanager.yml:/etc/alertmanager/alertmanager.yml \
  prom/alertmanager
🔄 Restart Prometheus
docker restart prometheus
🌐 Access
http://<YOUR-IP>:9093
📊 Step 8 — Grafana Setup
▶️ Run Grafana
docker run -d -p 3000:3000 --name grafana grafana/grafana
🌐 Access
http://<YOUR-IP>:3000
🔐 Login
username: admin
password: admin
⚙️ Add Data Source
Type: Prometheus
URL:
http://<YOUR-IP>:9090
📊 Step 9 — Dashboard Queries
CPU
100 - (avg(rate(node_cpu_seconds_total{mode="idle"}[1m])) * 100)
Memory
node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes
Request Rate
rate(app_requests_total[1m])
Error Rate
rate(app_requests_total{http_status="500"}[1m])
Latency
histogram_quantile(0.95, rate(app_request_latency_seconds_bucket[1m]))
⚠️ Issues Faced & Fixes
❌ host.docker.internal not working
Fix
ip a

Use actual IP instead.

❌ Flask container crash
Error
ModuleNotFoundError: prometheus_client
Fix
RUN pip install flask prometheus_client
❌ Connection refused
Debug
docker ps
docker logs sre-app-container
curl http://localhost:5000/metrics
❌ No rules found
Fix
-v $(pwd)/alerts.yml:/etc/prometheus/alerts.yml
❌ Grafana no data
Fix

Use:

http://<EC2-IP>:9090

NOT localhost.

🧠 Key Debug Commands
docker ps
docker logs <container>
docker exec -it <container> bash
curl http://localhost:5000/metrics
curl http://localhost:9100/metrics
🎯 Final Outcome

You built:

✅ Application monitoring
✅ System monitoring
✅ Metrics collection
✅ Alerting system
✅ Visualization dashboards
🚀 Next Steps
Slack alerts
Kubernetes monitoring
Logging (ELK / Loki)
Tracing (Jaeger)
