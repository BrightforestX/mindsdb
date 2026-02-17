### Docker images for MindsDB

* https://docs.mindsdb.com/setup/self-hosted/docker/
* https://hub.docker.com/u/mindsdb

## Building

Docker images are using only released versions of MindsDB from
https://pypi.org/project/MindsDB/ so no files in parent dir are used.

To build `release` image using version reported at
https://public.api.mindsdb.com/installer/release/docker___success___None

    docker build -f release --no-cache -t mindsdb/mindsdb .

To build `release` image with specific MindsDB version.

    docker build -f release --build-arg VERSION=2.57.0 -t mindsdb/mindsdb .

### `beta` vs `release`

`release` image pins MindsDB version and builds from fixed PyTorch docker
image. `beta` uses latest PyTorch image and updates MindsDB when container
is started to a version set at
https://public.api.mindsdb.com/installer/beta/docker___success___None

## Releasing

The `build.py <beta|release>` script is used in CI to build and push images
on release.

## Environment-Based Configuration

MindsDB Docker Compose now supports environment-based configuration for different deployment scenarios.

### Quick Start

1. **Copy the environment template:**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` file with your configuration:**
   ```bash
   # Example: Change MindsDB ports
   MINDSDB_HTTP_PORT=8080
   MINDSDB_MYSQL_PORT=3306
   
   # Example: Set your OpenAI API key
   OPENAI_API_KEY=sk-your-key-here
   
   # Example: Configure Sentry for error tracking
   SENTRY_IO_DSN=https://your-sentry-dsn
   SENTRY_IO_ENVIRONMENT=production
   ```

3. **Run the appropriate environment:**

### Running Development Environment

For local development with hot reload and debugging enabled:

```bash
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up
```

Or in detached mode:

```bash
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d
```

Development environment features:
- Local source code mounting for hot reload
- Debug mode enabled
- All observability services (OpenTelemetry, Langfuse) enabled
- Console logging for OTEL traces
- Detailed debug logging

### Running Production Environment

For production deployments with optimized settings:

```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

Production environment features:
- Uses pre-built images (no local build)
- Debug mode disabled
- Resource limits and reservations
- Optimized restart policies
- Observability services are disabled by default (enable with `--profile observability`)

To enable observability in production:

```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml --profile observability up -d
```

### Running Default Environment

For quick testing with default settings:

```bash
docker-compose up
```

Or in detached mode:

```bash
docker-compose up -d
```

### Configuration Variables

All configuration variables are documented in `.env.example`. Key categories include:

- **MindsDB Service**: Ports, storage, database connection
- **Logging & Monitoring**: Sentry, log levels
- **Langfuse**: LLM observability configuration
- **OpenTelemetry**: Distributed tracing configuration
- **PostgreSQL**: Database settings
- **API Keys**: OpenAI and other external services

### Environment-Specific Overrides

The system uses Docker Compose override files:
- `docker-compose.yml` - Base configuration with sensible defaults
- `docker-compose.dev.yml` - Development-specific overrides
- `docker-compose.prod.yml` - Production-specific overrides

### Best Practices

1. **Never commit `.env` files** - Use `.env.example` as a template
2. **Use strong secrets in production** - Generate secure values for:
   - `LANGFUSE_NEXTAUTH_SECRET`: `openssl rand -base64 32`
   - `LANGFUSE_ENCRYPTION_KEY`: `openssl rand -hex 32`
3. **Set appropriate resource limits** in production based on your hardware
4. **Enable monitoring** in production environments for better observability

## Running local docker compose environment (in old manner development)

1. Run `docker-compose -f docker-compose-old-manner up` or `docker-compose -f docker-compose-old-manner up -d` (for `detach` mode) to launch mindsdb in docker-compose in old school manner (monolithic on 100%)
