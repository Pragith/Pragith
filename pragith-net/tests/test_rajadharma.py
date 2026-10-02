from unittest.mock import AsyncMock, patch

import httpx
import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app, base_url="http://localhost")


def test_product_page_preserves_canonical_url_and_real_contact():
    response = client.get("/apps/rajadharma?utm_source=rajadharma&utm_campaign=about")
    assert response.status_code == 200
    assert (
        '<link rel="canonical" href="https://pragith.net/apps/rajadharma">'
        in response.text
    )
    assert "Pragith Prakash" in response.text
    assert "mailto:rajadharma@vriksh.ca" in response.text
    assert "Saved on your device" in response.text


@pytest.mark.parametrize(
    "status,payload",
    [
        (200, {"status": "sent"}),
        (429, {"error": "rate_limited"}),
        (503, {"error": "temporarily_unavailable"}),
    ],
)
def test_feedback_forwards_only_to_fixed_backend_and_preserves_result(status, payload):
    upstream = AsyncMock()
    upstream.post.return_value = httpx.Response(
        status, json=payload, headers={"Retry-After": "600"}
    )
    with patch("app.main.httpx.AsyncClient") as factory:
        factory.return_value.__aenter__.return_value = upstream
        response = client.post(
            "/api/rajadharma/feedback",
            json={
                "category": "bug",
                "subject": "Save failure",
                "message": "My reign did not resume.",
            },
            headers={"X-Forwarded-For": "forged", "Authorization": "do-not-forward"},
        )
    assert response.status_code == status
    assert response.json() == payload
    assert response.headers["Retry-After"] == "600"
    assert upstream.post.call_args.args == (
        "http://rajadharma-feedback:8000/api/feedback",
    )
    forwarded = upstream.post.call_args.kwargs
    assert forwarded["headers"]["X-Real-IP"] != "forged"
    assert "Authorization" not in forwarded["headers"]
    assert b"Save failure" in forwarded["content"]


def test_feedback_rejects_non_json_and_oversized_requests_without_upstream():
    with patch("app.main.httpx.AsyncClient") as factory:
        assert (
            client.post("/api/rajadharma/feedback", content="message").status_code
            == 415
        )
        assert (
            client.post(
                "/api/rajadharma/feedback",
                content="x" * 16385,
                headers={"Content-Type": "application/json"},
            ).status_code
            == 413
        )
        factory.assert_not_called()


@pytest.mark.parametrize(
    "failure",
    [
        httpx.ConnectError("private internal address"),
        httpx.ReadTimeout("private timeout"),
    ],
)
def test_feedback_preserves_failure_without_exposing_internal_details(failure):
    upstream = AsyncMock()
    upstream.post.side_effect = failure
    with patch("app.main.httpx.AsyncClient") as factory:
        factory.return_value.__aenter__.return_value = upstream
        response = client.post("/api/rajadharma/feedback", json={})
    assert response.status_code == 503
    assert response.json() == {"error": "temporarily_unavailable"}


@pytest.mark.parametrize("body", ["not-json", "[]", "x" * 4097])
def test_feedback_handles_invalid_upstream_responses(body):
    upstream = AsyncMock()
    upstream.post.return_value = httpx.Response(200, content=body)
    with patch("app.main.httpx.AsyncClient") as factory:
        factory.return_value.__aenter__.return_value = upstream
        response = client.post("/api/rajadharma/feedback", json={})
    assert response.status_code == 503
