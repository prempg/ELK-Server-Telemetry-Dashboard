# ELK-Server-Telemetry-Dashboard
<img width="1918" height="1078" alt="image" src="https://github.com/user-attachments/assets/75ed6212-aeac-4040-8247-4ca58ada1036" />


# Production Server Telemetry & APM Dashboard (ELK Stack)

An end-to-end telemetry monitoring and application performance management (APM) system built using **Elasticsearch 7.17** and **Kibana**. The solution collects, indexes, and visualizes synthetic microservice HTTP access logs in real time.

---

## Architecture Overview

```text
[ Python Synthetic Log Generator ] 
               │
               ▼ Bulk Indexing (JSON via HTTP 9200)
    [ Elasticsearch Cluster ] (Index: server_telemetry_logs)
               │
               ▼ Visual Query Engine & Index Pattern
     [ Kibana APM Dashboard ] (Port 5601)

Elasticsearch Engine: Single-node cluster configured with locked JVM heap allocations (-Xms512m -Xmx512m) to prevent OS swapping and memory exhaustion.

Log Ingestion Pipeline: Python client leveraging the Elasticsearch helpers.bulk API to ingest 1,000+ structured event schemas with ISO-8601 @timestamp tracking.

Kibana Analytics Layer: Configured custom Data Views indexing HTTP methods, status codes, latency values, and URI routing endpoints.

Log Event Schema
Each document pushed into server_telemetry_logs follows this structure:
{
  "@timestamp": "2026-09-26T14:45:10.123Z",
  "endpoint": "/api/v1/checkout",
  "method": "POST",
  "status_code": 200,
  "response_time_ms": 142,
  "client_ip": "192.168.1.45",
  "bytes_transferred": 4210
}
Visualizations Included
Total Ingested Log Events (Metric View): Real-time counter monitoring total volume ingested during the active query window.

Average Latency Trend (Line Lens): Aggregates and tracks response_time_ms across 30-minute buckets to pinpoint performance degradation and latency spikes.

Traffic Distribution by API Endpoint (Horizontal Bar Lens): Evaluates service usage across high-volume endpoints (/api/v1/login, /api/v1/products, /api/v1/cart).

HTTP Status Code Ratio (Donut Lens): Real-time availability breakdown categorizing 2xx (Success), 4xx (Client errors), and 5xx (Server faults).

Dashboard Preview
Setup & Reproduction
1. Start Services via Docker Compose
docker compose up -d
Verify cluster health:
curl http://localhost:9200

Ingest Telemetry Data
pip install elasticsearch==7.17.9
python index_data.py

3. Access Kibana Console
Navigate to http://localhost:5601, create the Data View for server_telemetry_logs*, and view the dashboard under Analytics > Dashboard.
