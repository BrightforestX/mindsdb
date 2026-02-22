# Logging Setup (Firebase Crashlytics + Cloud Logging)

MindsDB supports **Google Cloud Logging** (Firebase-compatible) for structured logs. Errors emitted at ERROR/CRITICAL level appear in **Cloud Error Reporting**, providing server-side crash/error visibility similar to Firebase Crashlytics.

## Prerequisites

- A Firebase or Google Cloud project
- Optional: A service account with Cloud Logging write permissions (otherwise Application Default Credentials are used)

## Environment Variables

| Variable | Description |
|----------|-------------|
| `FIREBASE_PROJECT_ID` | Your Firebase/GCP project ID. Required for Cloud Logging. |
| `GOOGLE_APPLICATION_CREDENTIALS` | Path to service account JSON key file. Omit to use ADC (e.g. `gcloud auth application-default login`). |
| `CLOUD_LOGGING_ENABLED` | Set to `true` or `1` to enable the Cloud Logging handler. Default: `false`. |
| `CLOUD_LOGGING_LEVEL` | Minimum level: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`. Default: `INFO`. |

## Installation

Install the Cloud Logging extra:

```bash
pip install mindsdb[cloud]
```

Or install directly:

```bash
pip install google-cloud-logging
```

## Quick Start

1. Copy `.env.example` to `.env` and set:

   ```bash
   FIREBASE_PROJECT_ID=your-project-id
   CLOUD_LOGGING_ENABLED=true
   # Optional: for explicit credentials
   GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
   ```

2. Start MindsDB. Logs will be sent to Cloud Logging when the handler is enabled and credentials are valid.

## Log Format

Logs are structured JSON with:

- **event**: Semantic event name (default: `log`)
- **level**: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`
- **component**: Logger name (e.g. `mindsdb.api.http`)
- **message**: Log message (PII/secrets are redacted)
- **metadata**: Optional extra key-value data (sensitive keys are redacted)

## Security

- **PII and secrets are never logged**. The Cloud Logging handler automatically redacts:
  - Password, token, API key, credential values
  - Bearer/ Basic auth headers
  - Sensitive keys in `extra` metadata
- Do not log raw request bodies, user identifiers, or other PII.

## Firebase Config (`firebase.json`)

A minimal `firebase.json` is included for project reference:

```json
{
  "projects": {
    "default": "your-firebase-project-id"
  }
}
```

Update `your-firebase-project-id` with your actual project ID.

## Error Reporting

Errors logged at `ERROR` or `CRITICAL` appear in [Google Cloud Error Reporting](https://console.cloud.google.com/errors), giving crash-like visibility for server-side failures.

## Troubleshooting

- **No logs in Cloud Logging**: Ensure `FIREBASE_PROJECT_ID` is set, `CLOUD_LOGGING_ENABLED` is true, and `google-cloud-logging` is installed.
- **Auth errors**: Set `GOOGLE_APPLICATION_CREDENTIALS` or run `gcloud auth application-default login`.
- **Handler not attaching**: The handler only attaches when the cloud extra is installed and project ID is configured. Check logs at startup for any import/init errors.
