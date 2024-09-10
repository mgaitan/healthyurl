# Healthchecker

A simple command-line tool to perform health checks on a given URL using Python's standard library. Exits with code `1` on HTTP errors.

## Features

- **Basic health check:** Performs a GET request to the specified URL and exits with `1` on HTTP errors.
- **Quiet mode:** Suppresses error messages, useful for running silent checks.

## Installation

For a minimal installation in Docker:

```Dockerfile
ADD --chmod=755 https://raw.githubusercontent.com/mgaitan/healthchecker/main/healthchecker.py /usr/bin/healthchecker
```

This will allow you to use `healthchecker` in your container without installing any external dependencies or increasing the image size by around 4.3%, as `curl` does when installed.


Altenatively you can use [uv](https://github.com/astral-sh/uv):

```
uv tool install healthchecker
````

Or pip 

```
pip install --user healthchecker
```


## Usage

```bash
healthchecker <url>
```

Checks the URL and exits with `1` on any HTTP errors.

or in quiet mode:

```bash
healthchecker -q <url>
```


## Why use `healthchecker`?

When using slim images like Python-based microservices, installing `curl` adds around **4.3%** to the image size (based on `python:3.12-slim-bookworm`). `healthchecker` uses only Python's standard library and does not require installing additional packages, making it more efficient for containers that need to stay small and lightweight.

For example, to use `healthchecker` as part of a health check in a Docker Compose file, you can define it like this:

```yaml
services:
  myservice:
    image: myservice:latest
    healthcheck:
      test: ["CMD", "healthchecker", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
```

This configuration runs `healthchecker` every 30 seconds, and it checks the health of the service at `http://localhost:8080/health`. If the health check fails (returns an HTTP error), the service will be marked as unhealthy.

In the same way, To use `healthchecker` in an ECS task definition, you can configure the health check like this:

```json
{
  "containerDefinitions": [
    {
      "name": "myservice",
      "image": "myservice:latest",
      "healthCheck": {
        "command": [
          "CMD-SHELL",
          "healthchecker http://localhost:8080/health"
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

Both examples show how `healthchecker` can replace `curl`, `wget` etc for basic health checks, helping reduce image size and build times, especially for lightweight Python-based containerized applications.