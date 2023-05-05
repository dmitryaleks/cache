# cache

Distributed cache with monitoring

# Requirements

  - Docker
  - Docker Compose

# Service definitions

## Redis

The core service of a distributed cache, will interface with:
  - client code utilizing the cache
  - the Redis Exporter service running in the same Docker container

```
  redis:
    image: "bitnami/redis:latest"
    ports:
      - 6379:6379
    environment:
      - REDIS_REPLICATION_MODE=master
      - REDIS_PASSWORD=pwd
```

## Redis Exporter

Exporter for Redis telemetry. Interfaces with core Redis service via a Docker link:

```
  redis-exporter:
    image: oliver006/redis_exporter
    ports:
      - 9121:9121
    environment:
      REDIS_ADDR: "redis:6379"
      REDIS_USER: null
      REDIS_PASSWORD: pwd
    links:
      - redis
```

## Prometheus

Data aggregator. Interfaces with Redis Exporter via a Docker link:

```
  prometheus:
    image: prom/prometheus
    ports:
      - 9090:9090
    volumes:
      - ./prometheus:/etc/prometheus:z
    links:
      - redis-exporter
```

Notes:
  - we mount the local "./prometheus" directory to the container's virtual "/etc/prometheus" so that Prometheus could pick up out local config file
  - when mapping the local filesystem to a container filesystem on Fedora Linux (or any SELinux) we need to add "z" (shared mount) option to avoid getting a file access permission problem

## Grafana

Front-end to show the Redis dashboard. No explicit programmatic linkage with data source required at service definition time.
Prometheus data source and dashboard definition are added via the Grafana GUI.

```
  grafana:
    image: grafana/grafana
    ports:
      - 3000:3000
```

Note: default credentials out-of-the-box are admin/admin

## Dashboard definition

[Grafana Dashboard for Redis Exporter](https://grafana.com/grafana/dashboards/763-redis-dashboard-for-prometheus-redis-exporter-1-x/)

## Test load

A trivial Python test script wrapped in a Bash script for a simulated multi-client test can be started as follows:

```
./start_test_load.sh <number_of_client_processes> <rate_events_per_second> <load_duration_sec>
```

E.g.:

```
./start_test_load.sh 128 32 30
```

## Resulting view on the dashboard

![Dashboard](https://raw.github.com/dmitryaleks/cache/master/dashboard/redis-dashboard-prometheus-grafana.png)

