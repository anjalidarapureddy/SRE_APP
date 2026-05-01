from flask import Flask, request
import time
import random

from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# 🔢 Metrics
REQUEST_COUNT = Counter(
    'app_requests_total',
    'Total HTTP Requests',
    ['method', 'endpoint', 'http_status']
)

REQUEST_LATENCY = Histogram(
    'app_request_latency_seconds',
    'Request latency',
    ['endpoint']
)

@app.route("/")
def home():
    start = time.time()
    response = "Hello, SRE World!"
    latency = time.time() - start

    REQUEST_COUNT.labels(request.method, "/", 200).inc()
    REQUEST_LATENCY.labels("/").observe(latency)

    return response

@app.route("/slow")
def slow():
    start = time.time()
    time.sleep(random.randint(1, 5))
    latency = time.time() - start

    REQUEST_COUNT.labels(request.method, "/slow", 200).inc()
    REQUEST_LATENCY.labels("/slow").observe(latency)

    return "Slow response..."

@app.route("/error")
def error():
    REQUEST_COUNT.labels(request.method, "/error", 500).inc()
    return "Error!", 500

# 📊 Metrics endpoint
@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
