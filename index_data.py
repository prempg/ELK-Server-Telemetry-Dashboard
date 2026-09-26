from datetime import datetime, timedelta
import random
from elasticsearch import Elasticsearch, helpers

# Connect to local Elasticsearch
es = Elasticsearch(["http://localhost:9200"])

endpoints = [
    "/api/v1/login",
    "/api/v1/products",
    "/api/v1/cart",
    "/api/v1/checkout",
    "/api/v1/payment",
]
methods = ["GET", "POST", "PUT"]
status_codes = [200, 200, 200, 201, 400, 404, 500]

print("Generating and pushing dummy log records to Elasticsearch...")

records = []
base_time = datetime.utcnow()

for i in range(1000):
  event_time = base_time - timedelta(minutes=random.randint(0, 180))
  doc = {
      "@timestamp": event_time.isoformat(),
      "endpoint": random.choice(endpoints),
      "method": random.choice(methods),
      "status_code": random.choice(status_codes),
      "response_time_ms": random.randint(20, 850),
      "client_ip": (
          f"192.168.1.{random.randint(10, 80)}"
      ),
      "bytes_transferred": random.randint(500, 15000),
  }
  records.append({"_index": "server_telemetry_logs", "_source": doc})

# Bulk indexing
helpers.bulk(es, records)
print("Successfully pushed 1000 records to index: server_telemetry_logs")