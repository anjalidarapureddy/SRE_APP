📘 SRE Monitoring Stack – Practical Implementation (README)
🚀 Project Overview

This project demonstrates a complete SRE monitoring pipeline built step-by-step using:

Application (Flask)
System metrics (Node Exporter)
Metrics collection (Prometheus)
Alerting (Alertmanager)
Visualization (Grafana)

The goal is to simulate a real production monitoring setup and understand how each component works together.

🧠 Architecture (Big Picture)
Flask App ───────┐
                 ├──> Prometheus ───> Grafana (Dashboards)
Node Exporter ───┘         │
                          ↓
                   Alertmanager → Notifications
                   
🧱 Step 1 — Application Deployment
✅ What we did
Built a simple Flask app
Added endpoints:
/ → normal response
/slow → latency simulation
/error → error simulation
🎯 Why we did this

To simulate real production behavior:

Traffic
Latency
Errors

These are the Golden Signals SREs monitor.

🧪 Sample Code
@app.route("/")
def home():
    return "Hello, SRE World!"

@app.route("/slow")
def slow():
    time.sleep(random.randint(1, 5))
    return "Slow response..."

@app.route("/error")
def error():
    return "Error!", 500
    
🐳 Step 2 — Containerization
✅ What we did
Created Dockerfile
Built and ran the app in a container
🎯 Why
Standardized environment
Easier deployment
Matches real-world infrastructure

📊 Step 3 — System Metrics Collection
✅ What we used
Node Exporter
🎯 Why

To monitor host-level metrics:

CPU
Memory
Disk
Network
🧠 Key Concept

System metrics answer:

“Is the machine healthy?”

📡 Step 4 — Prometheus Setup
✅ What we did
Installed Prometheus
Configured prometheus.yml
Added scrape targets:
Node Exporter
Flask App
🎯 Why Prometheus
Pull-based monitoring
Time-series database
Powerful query language (PromQL)
🧠 Key Concept

Prometheus scrapes metrics, it does not push.

📈 Step 5 — Application Instrumentation
✅ What we added

Inside Flask app:

Counter → request count
Histogram → latency
/metrics endpoint
🎯 Why

To monitor application-level behavior:

Request rate
Errors
Latency
🧠 Key Concept

Application metrics answer:

“Is the application healthy?”

📊 Step 6 — PromQL Queries

We used queries like:

CPU Usage
100 - (avg(rate(node_cpu_seconds_total{mode="idle"}[1m])) * 100)
Error Rate
rate(app_requests_total{http_status="500"}[1m])
Latency (95th percentile)
histogram_quantile(0.95, rate(app_request_latency_seconds_bucket[1m]))
🎯 Why PromQL
Analyze time-series data
Derive meaningful insights
Used in alerts & dashboards

🚨 Step 7 — Alerting
✅ What we did
Created alerts.yml
Configured alert rules
Integrated Alertmanager
🔥 Alerts Created
High CPU usage
High memory usage
High error rate
High latency
Target down
🎯 Why Alerts

To automatically detect problems without manual monitoring.

🧠 Key Concept

Alert lifecycle:

Inactive → Pending → Firing

🔔 Step 8 — Alertmanager
✅ What we did
Deployed Alertmanager
Connected it with Prometheus
🎯 Why
Route alerts
Group alerts
Send notifications (Slack, Email, etc.)
🧠 Current Limitation
No real notification configured yet
Alerts exist but are not sent anywhere

📊 Step 9 — Grafana (Visualization)
✅ What we did
Installed Grafana
Connected Prometheus as data source
Created dashboards
🎯 Why Grafana
Visualize metrics
Analyze trends
Debug issues visually
📈 Dashboards Created
CPU usage
Memory usage
Disk usage
Request rate
Error rate
Latency
🧠 Final Understanding
Layer	Purpose
App	Generates metrics
Node Exporter	System metrics
Prometheus	Collect & store
Alertmanager	Alert routing
Grafana	Visualization

⚠️ Issues Faced & Resolutions
❌ Issue 1: host.docker.internal not working
Problem
no such host
Cause
Not supported in Linux/EC2
Fix
Replaced with actual host IP

❌ Issue 2: Prometheus target DOWN (connection refused)
Cause
Flask app not running
Root Problem
ModuleNotFoundError: prometheus_client
Fix
Added dependency in Dockerfile:
RUN pip install flask prometheus_client

❌ Issue 3: No rules found in Prometheus
Cause
alerts.yml not mounted
Fix
Added volume mount:
-v $(pwd)/alerts.yml:/etc/prometheus/alerts.yml

❌ Issue 4: Alerts not triggering notifications
Cause
Alertmanager had no receivers configured
Fix
Added alertmanager.yml

❌ Issue 5: Grafana "No data"
Cause
Wrong Prometheus URL (localhost)
Fix
Used EC2/private IP instead
🧠 Key Learnings (Very Important)
1. Metrics Types
Counter → increasing values
Histogram → latency distribution
2. Debugging Flow (SRE mindset)
Prometheus → Target → Network → Container → Logs → Root cause
3. System vs App Metrics
Type	Example
System	CPU, Memory
App	Requests, Errors
4. Observability Stack
Metrics → Prometheus
Visualization → Grafana
Alerts → Alertmanager
🚀 What You Built

You now have a production-like monitoring system:

✔ Application monitoring
✔ System monitoring
✔ Metrics storage
✔ Alerting system
✔ Visualization dashboards

🔜 Next Improvements (Optional)
Slack integration
Kubernetes monitoring
Log aggregation (ELK / Loki)
Distributed tracing
