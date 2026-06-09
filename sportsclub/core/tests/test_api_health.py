# core/tests/test_api_health.py
"""API integration tests for the ping and health endpoints."""

from unittest.mock import patch

from django.db import DatabaseError
from django.test import TestCase


class PingAPITestCase(TestCase):
    """Test suite for the /ping endpoint."""

    def test_ping(self):
        """Test GET /api/v1/core/ping returns 200 with a status payload."""
        response = self.client.get("/api/v1/core/ping")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})


class HealthAPITestCase(TestCase):
    """Test suite for the /health endpoint."""

    def test_health_ok(self):
        """Test GET /api/v1/core/health returns 200 when the database is up."""
        response = self.client.get("/api/v1/core/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok", "database": "ok"})

    def test_health_database_failure(self):
        """Test GET /api/v1/core/health returns 503 when the database is down."""
        with patch("core.api.connection.cursor", side_effect=DatabaseError):
            response = self.client.get("/api/v1/core/health")

        self.assertEqual(response.status_code, 503)
        self.assertIn("detail", response.json())
