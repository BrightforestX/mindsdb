---
name: Environment-based Docker configuration
overview: Create an env/ folder structure with multiple .env files for different environments (dev, prod, supabase, local), update docker-compose.custom.yml to use env_file, enhance Makefile to support environment selection, and update .gitignore to track template.env while ignoring sensitive .env files.
status: completed
todos:
  - id: create-env-folder
    content: Create env/ directory and env/.gitignore file to ignore all .env files except template.env
    status: completed
  - id: create-template-env
    content: Create env/template.env with comprehensive documentation of all configuration options and examples
    status: completed
    dependencies:
      - create-env-folder
  - id: create-env-files
    content: Create env/dev.env, env/prod.env, env/supabase.env, and env/local.env with appropriate default values for each environment
    status: completed
    dependencies:
      - create-env-folder
  - id: update-docker-compose
    content: Update docker-compose.custom.yml to add env_file directive using ${ENV_FILE:-env/dev.env} and update volume mounts to be conditional
    status: completed
  - id: update-makefile
    content: Enhance Makefile run_docker_custom and rebuild_docker_custom targets to accept ENV parameter, validate file existence, and set ENV_FILE variable
    status: completed
  - id: update-gitignore
    content: Update .gitignore to allow env/template.env to be tracked while keeping other .env files ignored
    status: completed
---

# Environment-Based Docker Configuration Setup

## Overview

Implement a flexible environment-based configuration system for the custom Docker Compose setup, allowing easy switching between different environments (development, production, Supabase, local) using separate `.env` files.

## Files to Create

### 1. `env/` folder structure

Create the following files in a new `env/` directory:

- **`env/template.env`** - Documentation template with all configuration options and examples
- **`env/dev.env`** - Development environment configuration
- **`env/prod.env`** - Production environment configuration  
- **`env/supabase.env`** - Supabase-specific configuration
- **`env/local.env`** - Local development with SQLite (no remote DB)
- **`env/.gitignore`** - Ignore all .env files except template.env

### 2. Environment file contents

Each `.env` file will contain:

- `MINDSDB_DB_CON` - PostgreSQL connection string (required for remote DB)
- `MINDSDB_CONFIG_PATH` - Optional config.json path
- `MINDSDB_STORAGE_DIR` - Storage directory path
- `MINDSDB_LOG_LEVEL` - Logging level (DEBUG, INFO, WARNING, ERROR)
- `MINDSDB_USERNAME` - Optional HTTP authentication username
- `MINDSDB_PASSWORD` - Optional HTTP authentication password
- `MINDSDB_DEFAULT_PROJECT` - Default project name

## Files to Modify

### 1. `docker-compose.custom.yml`

- Add `env_file` directive that uses `${ENV_FILE:-env/dev.env}` as default
- Keep existing `environment` section as fallbacks
- Update volume mount for config file to be conditional

### 2. `Makefile`

- Update `run_docker_custom` target to:
  - Accept `ENV` parameter (e.g., `make run_docker_custom ENV=supabase`)
  - Validate that `env/$(ENV).env` exists
  - Set `ENV_FILE=env/$(ENV).env` when calling docker-compose
- Update `rebuild_docker_custom` to also accept `ENV` parameter
- Add helpful error messages if ENV is not specified or file doesn't exist

### 3. `.gitignore`

- Update to allow `env/template.env` to be tracked
- Keep ignoring `env/*.env` except `!env/template.env`
- Ensure `*.env` pattern doesn't block `env/template.env`

## Implementation Details

### Environment file structure

- `template.env` will be fully documented with comments explaining each variable
- Other `.env` files will have minimal comments, just values
- All files use the same variable names for consistency

### Docker Compose integration

- `env_file` directive loads variables from the specified file
- Environment variables in the `environment` section serve as fallbacks
- Variables from `env_file` take precedence over fallbacks

### Makefile enhancements

- Default to `dev.env` if no ENV specified
- Validate environment file exists before running
- Provide clear error messages and usage instructions

## Usage Pattern

After implementation, users can:

```bash
# Use specific environment
make run_docker_custom ENV=supabase
make run_docker_custom ENV=prod
make run_docker_custom ENV=dev

# Or use docker-compose directly
ENV_FILE=env/supabase.env docker-compose -f docker-compose.custom.yml up -d
```

## Git Strategy

- `env/template.env` will be committed (documentation)
- All other `env/*.env` files will be ignored (contain sensitive data)
- Users copy `template.env` to create their own environment files