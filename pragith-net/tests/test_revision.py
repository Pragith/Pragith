import importlib.util
import json
import re
from pathlib import Path
from unittest.mock import patch
import pytest
from fastapi.testclient import TestClient
from app.main import app, limiter, templates
from app.content.site import EXPERIENCE, PRODUCT_FACTS

client = TestClient(app, base_url="http://localhost")


@pytest.fixture(autouse=True)
def reset_limit():
    limiter.reset()


@pytest.mark.parametrize("path", ["/experience", "/resume"])
def test_resume_chronology(path):
    html = client.get(path).text
    for entry in EXPERIENCE:
        assert entry["period"] in html
        assert entry["context"].replace("&", "&amp;") in html
    assert "eighteen months" in html
    assert "January 2020–January 2021" in html
    assert "SMART FBO, Hibu and Sigmoid" in html


@pytest.mark.parametrize(
    "kind,heading,label",
    [
        (
            "Teaching / workshop",
            "Plan a course or workshop.",
            "Audience, topics and learning goals",
        ),
        (
            "Speaking engagement",
            "Invite me to speak.",
            "Event, audience and session format",
        ),
        (
            "Hourly engineering",
            "Tell me about the system and where it is stuck.",
            "Context, constraints and desired outcome",
        ),
    ],
)
def test_contact_intent_survives_delivery_failure(kind, heading, label):
    html = client.get("/contact", params={"engagement_type": kind}).text
    assert heading in html and label in html
    assert "Organization (optional)" in html and "Timeline (optional)" in html
    with (
        patch("app.main.mailer_service.verify_recaptcha", return_value=True),
        patch("app.main.mailer_service.send_contact_email", return_value=False),
    ):
        response = client.post(
            "/contact",
            data={
                "name": "Test person",
                "email": "test@example.com",
                "engagement_type": kind,
                "message": "Keep this exact message.",
                "ref_page": "teaching",
                "cta_id": "test-context",
            },
        )
    assert heading in response.text and label in response.text
    assert "Keep this exact message." in response.text
    assert 'name="cta_id" value="test-context"' in response.text


def test_navigation_and_unhidden_work():
    html = client.get("/").text
    nav = html.split('id="nav-links"')[1].split("</nav>")[0]
    assert all(
        f">{name}</a>" in nav
        for name in ["Work", "Experience", "Teaching", "About", "Contact", "Resume"]
    )
    assert "Writing" not in nav and "Services" not in nav
    assert "data-carousel" not in html
    projects = client.get("/projects").text
    assert 'role="tab"' not in projects
    assert projects.count('id="project-') == 5
    resume = client.get("/resume").text
    assert re.search(r'href="/resume"\s+aria-current="page"', resume)


def test_callrenard_matches_fact_record():
    html = client.get("/projects").text
    fact = PRODUCT_FACTS["callrenard"]
    assert fact["public_access"] in html and fact["maturity"] in html
    for capability in fact["capabilities"]:
        assert capability in html
    assert "Live service" not in html


def test_missing_credentials_and_editorial_notes_are_not_claims():
    for path in ["/about", "/resume"]:
        assert "Certified" not in client.get(path).text
    assert (
        "excluded from search indexing until"
        not in client.get("/projects/caffeinate-d").text
    )
    html = client.get("/case-studies").text
    assert "verified scope" not in html and "Read the technical record" not in html
    for slug in ["enterprise-data-platform", "ai-mlops-automation"]:
        text = client.get("/case-studies/" + slug).text
        assert "What I learned" not in text and "<dt>Result" not in text


def test_analytics_and_recaptcha_bindings():
    with patch.dict(
        templates.env.globals, ga_tag="G-TEST", clarity_project_id="clarity-test"
    ):
        for path in [
            "/",
            "/experience",
            "/resume",
            "/projects",
            "/teaching",
            "/contact",
        ]:
            html = client.get(path).text
            assert "gtag/js?id=G-TEST" in html and "clarity-test" in html
    with patch("app.main.settings.RECAPTCHA_SITE_KEY", "site-key"):
        assert "recaptcha/api.js?render=site-key" in client.get("/contact").text


def test_reference_exercise_matches_published_output(tmp_path):
    source = Path("app/static/teaching")
    spec = importlib.util.spec_from_file_location(
        "exercise", source / "check_orders.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    expected = json.loads((source / "expected.json").read_text())
    assert module.inspect_orders(source / "orders.csv") == expected
    assert expected["accepted"] == 3 and expected["total"] == "56.25"
    other = tmp_path / "orders.csv"
    other.write_text("order_id,amount\n,12\nA,NaN\nB,Infinity\nC,0\nD,1.25\nD,2.50\n")
    result = module.inspect_orders(other)
    assert (
        result["accepted"] == 1
        and result["total"] == "1.25"
        and len(result["rejected"]) == 5
    )
