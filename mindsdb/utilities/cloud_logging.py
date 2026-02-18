"""
Firebase-compatible Google Cloud Logging integration.

Uses google-cloud-logging for structured JSON logs with event, level, component, message.
Integrates with Firebase/GCP projects via FIREBASE_PROJECT_ID and GOOGLE_APPLICATION_CREDENTIALS.
Never logs secrets or PII - use PiiFilter before emitting.
"""
import logging
import os
import re
from typing import Optional

# Sensitive keys in extra payloads - values are redacted
_SENSITIVE_KEYS = frozenset({
    'password', 'passwd', 'pwd', 'secret', 'token', 'api_key', 'apikey',
    'auth', 'credential', 'authorization', 'bearer', 'cookie', 'session',
    'ssn', 'email', 'phone', 'credit_card', 'card_number',
})


def _redact_sensitive(msg: str) -> str:
    """Redact obvious secrets/PII from a message string."""
    out = msg
    for pat in [
        r'(password|passwd|pwd|secret|token|api_key|apikey)\s*[=:]\s*["\']?([^"\'\s]{4,})',
        r'(bearer|basic)\s+([a-zA-Z0-9._-]{8,})',
    ]:
        out = re.sub(pat, r'\1=***REDACTED***', out, flags=re.IGNORECASE)
    return out


def _sanitize_extra(extra: dict) -> dict:
    """Remove or redact sensitive keys from extra payload."""
    if not extra:
        return {}
    return {
        k: '***REDACTED***' if k.lower() in _SENSITIVE_KEYS else v
        for k, v in extra.items()
    }


def _level_to_severity(levelno: int) -> str:
    mapping = {
        logging.DEBUG: 'DEBUG',
        logging.INFO: 'INFO',
        logging.WARNING: 'WARNING',
        logging.ERROR: 'ERROR',
        logging.CRITICAL: 'CRITICAL',
    }
    return mapping.get(levelno, 'DEFAULT')


class PiiFilter(logging.Filter):
    """Filter that redacts PII and secrets from log records before emission."""

    def filter(self, record: logging.LogRecord) -> bool:
        if hasattr(record, 'msg') and isinstance(record.msg, str):
            record.msg = _redact_sensitive(record.msg)
        if hasattr(record, 'args') and record.args:
            record.args = tuple(
                _redact_sensitive(str(a)) if isinstance(a, str) else a
                for a in record.args
            )
        return True


class CloudLoggingHandler(logging.Handler):
    """
    Logging handler that sends structured JSON logs to Google Cloud Logging.
    Payload: event, level, component, message. Never logs secrets or PII.
    """

    def __init__(
        self,
        project_id: Optional[str] = None,
        default_resource: Optional[dict] = None,
    ):
        super().__init__()
        self._project_id = project_id or os.environ.get('FIREBASE_PROJECT_ID', '')
        self._client = None
        self._default_resource = default_resource or {}
        self.addFilter(PiiFilter())

    def _get_client(self):
        if self._client is not None:
            return self._client
        try:
            import google.cloud.logging as gcl
            self._client = gcl.Client(project=self._project_id or None)
            return self._client
        except Exception:
            return None

    def emit(self, record: logging.LogRecord) -> None:
        try:
            client = self._get_client()
            if client is None:
                return
            logger = client.logger(name='mindsdb')
            payload = self._build_payload(record)
            severity = _level_to_severity(record.levelno)
            logger.log_struct(payload, severity=severity)
        except Exception:
            self.handleError(record)

    def _build_payload(self, record: logging.LogRecord) -> dict:
        msg = self.format(record)
        if isinstance(record.msg, str):
            msg = _redact_sensitive(record.msg)
        extra = {}
        if hasattr(record, '__dict__'):
            for k, v in record.__dict__.items():
                if k not in (
                    'name', 'msg', 'args', 'created', 'filename', 'funcName',
                    'levelname', 'levelno', 'lineno', 'module', 'msecs',
                    'pathname', 'process', 'processName', 'relativeCreated',
                    'stack_info', 'exc_info', 'exc_text', 'thread', 'threadName',
                    'message', 'asctime',
                ):
                    extra[k] = v
        extra = _sanitize_extra(extra)

        payload = {
            'event': getattr(record, 'event', 'log'),
            'level': _level_to_severity(record.levelno),
            'component': record.name or 'mindsdb',
            'message': msg,
        }
        if extra:
            payload['metadata'] = extra
        return payload


def get_cloud_handler(project_id: Optional[str] = None) -> Optional[CloudLoggingHandler]:
    """
    Returns a configured CloudLoggingHandler if google-cloud-logging is installed
    and FIREBASE_PROJECT_ID (or project_id) is set. Otherwise returns None.
    """
    try:
        import google.cloud.logging  # noqa: F401
    except ImportError:
        return None
    pid = project_id or os.environ.get('FIREBASE_PROJECT_ID', '')
    if not pid:
        return None
    return CloudLoggingHandler(project_id=pid)
