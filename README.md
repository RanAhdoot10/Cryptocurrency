# Setup Grafana with Prometheus for Python projects using Docker

This project includes the implementation of how to set up service monitoring for Python projects with Prometheus and Grafana using Docker containers.

## Getting Started

Run Docker Services

```
docker-compose up -d
```

Navigate to `localhost:3000` to see Grafana login page.
For displaying the data in pct, navigate to "Panel options", select "Standard options", under the "Unit" section, choose "Percent (0-100)"

Prometheus Server URL

```
http://prometheus:9090
```

Cryptocurrency endpoint

```
https://coinstats.app/coins/
```
