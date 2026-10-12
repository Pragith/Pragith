"""Verified public content for pragith.net.

Unverified metrics belong in editorial notes, never in rendered page data.
"""

import json
from pathlib import Path

CANONICAL_TITLE = "AI Forward Deployed Engineer"
EXPERIENCE_LABEL = "14+ years"

CERTIFICATIONS = [
    "Claude Certified Architect – Foundations",
    "Google Cloud Professional Data Engineer",
    "Google Cloud Professional Cloud Architect",
    "Databricks Certified Data Engineer Associate",
    "Databricks Certified Generative AI Associate",
    "AWS Certified Cloud Practitioner",
]

CLOUD_PLATFORMS = ["AWS", "Google Cloud", "Microsoft Azure", "Databricks"]

CAPABILITIES = [
    {
        "title": "AI systems",
        "summary": "I connect models to approved data and tools, then add evaluation, permissions, telemetry and human review around the workflow.",
        "href": "/services/ai-systems",
    },
    {
        "title": "Data platforms",
        "summary": "I build and troubleshoot batch, streaming and analytical systems using Python, SQL, Spark, Kafka, Airflow and cloud data services.",
        "href": "/services#data-platforms",
    },
    {
        "title": "Cloud delivery and operations",
        "summary": "I work across AWS, Google Cloud, Azure and Databricks on infrastructure, CI/CD, model delivery, observability and incidents.",
        "href": "/services#cloud-platforms",
    },
    {
        "title": "Teaching",
        "summary": "I teach Python, statistics, machine learning, data engineering and cloud architecture through courses, workshops and team programs.",
        "href": "/teaching",
    },
]

CASE_STUDIES = [
    {
        "slug": "enterprise-data-platform",
        "title": "Enterprise data platform operations",
        "preview": "I examined failures and automated releases on enterprise data platforms handling multi-terabyte workloads and hundreds of pipelines.",
        "context": "The data platform supplied reports and analytical models through hundreds of automated pipelines.",
        "constraint": "The platform had to remain reliable while releases, schema changes and upstream dependencies continued to evolve.",
        "role": "I supported platform operations and data engineering, including releases and production incidents.",
        "architecture": "Cloud data storage and compute, orchestrated batch pipelines, SQL and Python transformation layers, CI/CD and centralized observability.",
        "implementation": "I automated deployments, examined pipeline failures and improved monitoring for data processing. I also supported the teams using the data.",
        "result": "The platform supported multi-terabyte daily processing across hundreds of pipelines with clearer operational ownership and repeatable releases.",
        "technologies": [
            "Python",
            "SQL",
            "Google Cloud",
            "AWS",
            "Airflow",
            "Databricks",
            "CI/CD",
        ],
        "lessons": "Platform reliability depends as much on ownership, release discipline and observability as it does on individual technologies.",
    },
    {
        "slug": "event-driven-data-systems",
        "title": "Near-real-time and event-driven data systems",
        "preview": "I designed data flows between operational applications and cloud services.",
        "context": "Operational applications needed to send data from source systems to cloud services and the teams using it.",
        "constraint": "The integration had to tolerate partial failures, variable event volume and sensitive operational data.",
        "role": "I led the work on data ingestion and processing, including deployment and failure handling.",
        "architecture": "Event-driven ingestion, streaming and asynchronous processing, durable storage, API integration and monitored delivery pipelines.",
        "implementation": "I defined retries, automated deployments and added checks for data delivery.",
        "result": "The resulting system supported timely operational data delivery with explicit failure handling and traceable processing stages.",
        "technologies": [
            "Python",
            "Kafka",
            "Pub/Sub",
            "Cloud Run",
            "Dataflow",
            "APIs",
            "Docker",
        ],
        "lessons": "Near-real-time architecture is valuable only when replay, failure isolation and operational support are designed with the happy path.",
    },
    {
        "slug": "ai-mlops-automation",
        "title": "Enterprise AI assistant delivery",
        "preview": "I owned architecture and production delivery for an enterprise AI assistant for eighteen months.",
        "context": "An enterprise team needed to connect an AI assistant to its existing tools and data.",
        "constraint": "Model behaviour, access, cost and failure modes needed to fit established delivery and support practices.",
        "role": "I owned the assistant’s architecture and production delivery through my consulting work at Vriksh. I also built AI platform components and supported them in production.",
        "architecture": "Model and tool orchestration, governed data access, API services, structured outputs, evaluation hooks, CI/CD and operational telemetry.",
        "implementation": "I connected models to approved tools and data, added deployment controls and supported production debugging.",
        "result": "The team gained a supportable path for deploying AI-assisted workflows without treating model output as automatically correct.",
        "technologies": [
            "Python",
            "FastAPI",
            "LLMs",
            "MLflow",
            "Docker",
            "Kubernetes",
            "CI/CD",
        ],
        "lessons": "Useful enterprise AI combines model capability with evaluation, permissions, human approval and conventional software operations.",
    },
    {
        "slug": "regulated-integrations",
        "title": "Data pipelines for restricted datasets",
        "preview": "I built data pipelines for forensic and regulatory work.",
        "context": "The pipelines processed restricted datasets for analysis, with access controls and records for review.",
        "constraint": "Engineering decisions needed to account for traceability, repeatability, restricted data and governance review.",
        "role": "I designed data processing and integrations with the teams responsible for the data and its access controls.",
        "architecture": "Controlled ingestion, validation, transformation and reporting layers with access boundaries, logs and reproducible processing.",
        "implementation": "I built pipelines, documented data handling and supported validation and review.",
        "result": "The workflows made sensitive analytical processing more repeatable, reviewable and supportable.",
        "technologies": [
            "Python",
            "SQL",
            "Cloud storage",
            "ETL",
            "Data validation",
            "Access controls",
        ],
        "lessons": "In governance-sensitive environments, documentation and traceability are part of the system rather than a final compliance exercise.",
    },
    {
        "slug": "executive-analytics",
        "title": "Reporting and metric definitions",
        "preview": "I connected source data to shared metric definitions and dashboards.",
        "context": "Leadership and operational teams needed reports that used the same metric definitions across their source systems.",
        "constraint": "Definitions, refresh behaviour and access had to remain understandable beyond the original dashboard implementation.",
        "role": "I integrated source data and built reporting models and dashboards. I also helped teams use the reports.",
        "architecture": "Source connectors, transformation models, governed metrics, semantic layers and role-aware dashboards with scheduled or near-real-time refresh.",
        "implementation": "I agreed metric definitions with the team, built reporting models and documented who maintained them.",
        "result": "Stakeholders received a clearer path from operational data to consistent, maintainable executive reporting.",
        "technologies": [
            "SQL",
            "Python",
            "Looker",
            "Apache Superset",
            "Cloud warehouses",
            "Semantic modelling",
        ],
        "lessons": "An executive dashboard is credible when metric definitions, lineage and ownership are as clear as its visual presentation.",
    },
    {
        "slug": "engineering-enablement",
        "title": "Teaching data and cloud engineering",
        "preview": "I taught data science and cloud engineering through courses and workshops.",
        "context": "Learners needed instruction in data science and cloud engineering, with exercises they could work through.",
        "constraint": "Programs had to serve mixed experience levels while retaining technical depth and useful assessment.",
        "role": "I taught graduate courses and workforce programs, led workshops and mentored learners.",
        "architecture": "Project-led curricula spanning Python, statistics, machine learning, APIs, cloud data systems, dashboards and engineering practices.",
        "implementation": "I designed lessons, delivered live instruction, reviewed projects and adapted examples to learner and team needs.",
        "result": "Participants received structured, applied learning across data, AI and cloud engineering topics.",
        "technologies": [
            "Python",
            "SQL",
            "R",
            "Machine learning",
            "Cloud platforms",
            "APIs",
            "BI",
        ],
        "lessons": "Technical education works best when learners can connect architecture decisions to code, operations and real constraints.",
    },
]

PROJECTS = [
    {
        "slug": "velvet",
        "title": "Velvet IPTV Player",
        "status": "Production",
        "summary": "A cross-platform IPTV player for Stalker and Ministra portals, with set-top-box support.",
        "version": "Velvet 5.3.12",
        "href": "https://velvet.plus",
        "link_label": "Visit Velvet",
    },
    {
        "slug": "golf-swing-analyzer",
        "title": "Fairway: Golf Swing Analyzer",
        "status": "Experimental",
        "summary": "Practise your golf swing with live 2D body tracking, saved swing summaries and skeleton replay. Use a face-on camera; left- and right-handed golfers are supported. Body tracking runs in your browser.",
        "version": "Live app · Swing detection and timing estimates are experimental. The app saves summaries and skeleton clips on a self-hosted server.",
        "href": "https://golf.lab.pragith.net",
        "link_label": "Open Golf Swing Analyzer",
    },
    {"slug": "callrenard"},
    {
        "slug": "caffeinate-d",
        "title": "Caffeinate-d",
        "status": "Beta",
        "summary": "A macOS menu-bar app that keeps your display awake.",
        "version": "Source version 0.2.0",
        "href": "/projects/caffeinate-d",
        "link_label": "Project details",
    },
]

EXPERIENCE = [
    {
        "period": "November 2021 to present",
        "title": "AI and data engineering engagements",
        "context": "Vriksh Consulting Services Inc. · Consulting",
        "body": "I design and build AI and data systems and support them in production. My work includes eighteen months owning architecture and production delivery for an enterprise AI assistant. The data platforms I supported handled multi-terabyte datasets and hundreds of automated pipelines.",
    },
    {
        "period": "January to November 2021",
        "title": "Quality & Technical Services Manager / Lead R&D Data Scientist",
        "context": "Sofvie · Employment",
        "body": "I led technical quality and applied data research, including cloud data workflows and delivery automation.",
    },
    {
        "period": "June 2018 to January 2021",
        "title": "Staff Consultant → Senior Consultant",
        "context": "Dentsu / Merkle Cardinal Path · Employment",
        "body": "Staff Consultant, June 2018 to January 2020; promoted to Senior Consultant, January 2020 to January 2021. My work covered enterprise analytics and cloud data consulting.",
    },
    {
        "period": "March 2017 to June 2018",
        "title": "Consultant, Data Science",
        "context": "EY · Employment",
        "body": "I worked on data science and analytical processing for forensic and regulatory work, with client and dataset details kept confidential.",
    },
    {
        "period": "November 2015 to March 2017",
        "title": "Data Scientist",
        "context": "Wipro · Employment",
        "body": "I built analytical systems over operational and log data, working on modelling, implementation and performance investigation.",
    },
    {
        "period": "June 2012 to November 2015",
        "title": "Early data and software roles",
        "context": "SMART FBO, Hibu and Sigmoid",
        "body": "My early work spanned reporting, backend development and real-time analytics using Python, SQL, R and distributed processing.",
    },
]

SERVICES = [
    (
        "ai-systems",
        "AI systems and agent workflows",
        "Model and tool orchestration, retrieval, structured output, evaluation, observability, approval gates and secure integration with existing systems.",
    ),
    (
        "data-platforms",
        "Data platforms",
        "Architecture and implementation for batch, streaming, lakehouse, warehouse and analytics workloads, including release and operational ownership.",
    ),
    (
        "cloud-platforms",
        "MLOps, DevOps and cloud architecture",
        "Infrastructure as code, model delivery, containers, observability and production debugging across AWS, Google Cloud, Azure and Databricks.",
    ),
    (
        "forward-deployed",
        "Forward-deployed implementation",
        "Hands-on architecture, coding and debugging alongside product, security, data and platform teams.",
    ),
    (
        "analytics",
        "Analytics and executive BI",
        "Source integration, governed models, semantic layers, dashboards, access control and maintainable reporting operations.",
    ),
    (
        "training",
        "Technical education",
        "Workshops, curriculum development and team instruction across data, AI, cloud and software delivery.",
    ),
]

INDEXABLE_PATHS = [
    "/",
    "/about",
    "/experience",
    "/case-studies",
    "/services",
    "/services/ai-systems",
    "/services/executive-bi",
    "/teaching",
    "/projects",
    "/apps/rajadharma",
    "/resume",
    "/writing",
    "/contact",
    "/business",
    "/privacy",
    "/legal",
]

# Synchronized publication record; the company site consumes the same JSON.
PRODUCT_FACTS = json.loads(Path(__file__).with_name("product-facts.json").read_text())
for project in PROJECTS:
    if project["slug"] == "callrenard":
        facts = PRODUCT_FACTS["callrenard"]
        project.update(
            title=facts["display_name"],
            status=facts["maturity"],
            summary=facts["purpose"],
            version=facts["public_access"],
            href="https://vriksh.ca/ventures/callrenard",
            link_label="Scope & demonstration",
            capabilities=facts["capabilities"],
            limitations=facts["limitations"],
        )
    elif project["slug"] == "velvet":
        project.update(status="Active development", version="Product website & setup")
PROJECTS.sort(
    key=lambda p: {"golf-swing-analyzer": 0, "velvet": 1, "callrenard": 2}.get(
        p["slug"], 3
    )
)
