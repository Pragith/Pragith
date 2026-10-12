"""Render non-GET copy states without sending mail or calling reCAPTCHA."""

import json

from starlette.requests import Request

from app.main import render

request = Request(
    {
        "type": "http",
        "method": "GET",
        "path": "/contact",
        "query_string": b"",
        "headers": [],
        "scheme": "http",
        "server": ("localhost", 4784),
    }
)
states = []
for name, template, extra in [
    ("contact-success", "contact_success.html", {}),
    ("server-error-template", "500.html", {}),
    (
        "contact-verification-error",
        "contact.html",
        {"error": "reCAPTCHA verification failed. Please try again."},
    ),
    (
        "contact-delivery-error",
        "contact.html",
        {"error": "The message could not be sent. Please try again."},
    ),
]:
    response = render(
        request,
        template,
        title="Message received | Pragith Prakash"
        if name == "contact-success"
        else "Contact Pragith Prakash",
        description="Your message has been received."
        if name == "contact-success"
        else "Contact Pragith Prakash.",
        canonical_path="/contact",
        form={},
        tracking={},
        recaptcha_site_key="",
        **extra,
    )
    states.append({"route": "source-state:" + name, "html": response.body.decode()})
print(json.dumps(states))
