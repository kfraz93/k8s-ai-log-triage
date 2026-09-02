import pytest
from pydantic import ValidationError

from app.models.schemas import LogPayload


def test_valid_log_payload():
    payload_data = {
        "service_name": "payment-service",
        "log_level": "ERROR",
        "error_message": "Database connection pool exhausted",
        "stack_trace": "psycopg2.OperationalError: FATAL",
    }
    payload = LogPayload(**payload_data)
    assert payload.service_name == "payment-service"
    assert payload.error_message == "Database connection pool exhausted"


def test_missing_required_field_raises_validation_error():
    invalid_data = {
        "service_name": "payment-service",
        "log_level": "ERROR",
        # 'error_message' missing intentionally
        "message": "Wrong key name",
    }
    with pytest.raises(ValidationError):
        LogPayload(**invalid_data)
