# healthyurl

A simple command-line tool to perform health checks on a given URL using Python's standard library. Exits with code `1` on HTTP errors.

## Installation

For a minimal installation in Docker:

```Dockerfile
ADD --chmod=755 https://raw.githubusercontent.com/mgaitan/healthyurl/main/healthyurl.py /usr/bin/healthyurl
```

Altenatively you can use [uv](https://github.com/astral-sh/uv):

```
uv tool install healthyurl
````

Or pip 

```
pip install --user healthyurl
```


## Usage

```bash
healthyurl <url>
```

Checks the URL and exits with `1` on any HTTP errors. Or in quiet mode:

```bash
healthyurl -q <url>
```


## Why use `healthyurl`?

When using slim images like Python-based microservices, installing `curl` adds around 5Mb (**4.3%** of `python:3.12-slim-bookworm` size). `healthyurl` uses only Python's standard library and does not require installing additional packages, making it more efficient for containers that need to stay small and lightweight.

For example, to use `healthyurl` as part of a health check in a Docker Compose file, you can define it like this:

```yaml
services:
  myservice:
    image: myservice:latest
    healthcheck:
      test: ["CMD", "healthyurl", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
```

This configuration runs `healthyurl` every 30 seconds, and it checks the health of the service at `http://localhost:8080/health`. If the health check fails (returns an HTTP error), the service will be marked as unhealthy.

In the same way, To use `healthyurl` in an ECS task definition, you can configure the health check like this:

```json
{
  "containerDefinitions": [
    {
      "name": "myservice",
      "image": "myservice:latest",
      "healthCheck": {
        "command": [
          "CMD-SHELL",
          "healthyurl -q http://localhost:8080/health"
        ],
        "interval": 30,
        "timeout": 10,
        "retries": 3,
        "startPeriod": 10
      }
    }
  ]
}
```

Both examples show how `healthyurl` can replace `curl`, `wget` etc for basic health checks, helping reduce image size and build times, especially for lightweight Python-based containerized applications.