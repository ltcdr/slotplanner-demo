# Slotplanner – Architecture and System Overview

Slotplanner is a scheduling and resource‑management platform designed to handle bookings, activities, clients, and administrative workflows. This repository provides a public, high‑level overview of the system’s architecture, data model, API structure, and Azure deployment approach. Production code is not included.

---

## Purpose of This Repository

This repository is intended for technical reviewers, recruiters, and hiring managers. It highlights the architectural design, engineering decisions, and structure of the Slotplanner system while keeping the production code private.

The demo and diagrams represent architectural concepts only.
Production logic, business rules, and full administrative workflows are intentionally omitted.

---

## System Components & Related Repositories
Slotplanner is structured as a multi‑repository system to reflect real‑world release and delivery workflows.
This repository (slotplanner-demo) provides the public architectural overview and demo, while additional components are maintained separately:

[slotplanner-demo-functions](https://github.com/ltcdr/slotplanner-demo-functions)  
Azure Functions powering automation tasks, demo activity generation, booking workflows, and integration logic.
Deployed independently via GitHub Actions using OIDC and Managed Identity.

[slotplanner-meta](https://github.com/ltcdr/slotplanner-demo-meta)  
The orchestration repository coordinating cross‑service releases, unified versioning, environment configuration, and deployment sequencing.
This meta layer represents the production‑grade release management approach used for the full Slotplanner system.

These repositories together illustrate a distributed architecture with independent deployment units and coordinated release processes — a core aspect of Slotplanner’s engineering and delivery design.

---

## Demo (Activities & Booking Flow)
The repository includes a small interactive demo located in `/demo/`.
It showcases a simplified version of Slotplanner’s activity and booking workflow:

- Weekly auto‑generated demo activities
- Interactive calendar (HTML + CSS + JavaScript)
- Activity modal with booking action
- Basic booking API (POST /demo/book)
- Bookings overview page (GET /demo/bookings)
- Minimal SQLite‑backed FastAPI demo backend
- Basic authentication protecting the demo pages

This demo is intentionally lightweight and isolated from the production architecture.
It exists solely to illustrate the user‑facing concepts of activities, time slots, and bookings.

---

## Architecture Overview

Slotplanner follows a modular, service‑oriented architecture:

- Backend: FastAPI
- ORM/Data Layer: SQLAlchemy
- Schemas and Validation: Pydantic
- Frontend: HTML, CSS, and JavaScript (React + TypeScript planned)
- Hosting: Azure App Service
- Authentication: Session-based authentication (planned migration to Azure Entra ID)
- Storage: SQLite file-based database (planned migration to PostgreSQL)
- CI/CD: GitHub Actions

The system is organized into clear domains such as users, clients, relatives, activities, bookings, and administrative management.


### Serverless Components

Slotplanner-Demo also includes a lightweight serverless layer hosted in a
separate repository (`slotplanner-demo-functions`). These Azure Functions
handle demo automation tasks, booking operations, and integration workflows.
They are deployed independently via GitHub Actions using OIDC and Managed
Identity, illustrating multi‑service release coordination.


### Data Model

The platform uses a relational schema with entities including:

- Clients
- Client relatives
- Activities
- Bookings
- Domains
- Administrative users
- Audit fields (created_by, changed_by, timestamps)

Diagrams in the `/docs/` directory illustrate relationships and workflows.


### Diagrams

#### Architecture Diagram
![Architecture Diagram](docs/architecture/architecture.png)

#### Entity Relationship Diagram
![ER Diagram](docs/data-model/er-diagram.png)

#### Booking Flow Diagram
![Booking Flow](docs/flows/booking-flow.png)


### API Design

The backend exposes a structured REST API with:

- Consistent request and response schemas
- Separation of routing, service logic, and validation
- Pydantic‑based input and output models
- Error handling and standardized responses
- Endpoints for booking operations and administrative management

Example endpoints and flows are documented in `/docs/api/`.


---

## Deployment

### Current Deployment
Slotplanner currently runs locally using:

- Uvicorn for backend execution
- Caddy for reverse proxy and static file serving
- SQLite as the local database
- Session-based authentication
- Local file-based storage for assets and data


### Planned Azure Deployment
A future cloud deployment is planned using Azure services:

- Azure App Service for backend and frontend hosting
- Azure Database for PostgreSQL as the primary database
- Azure Storage for static assets and backups
- Azure Monitor for logging and metrics
- Azure Entra ID for authentication and identity management
- Deployment slots for staging and production environments
- GitHub Actions for automated CI/CD pipelines

Documentation for the planned deployment will be added in `/docs/deployment/`.


---


## Release & Delivery Process

Slotplanner uses a structured release workflow designed for reliability and
traceability across multiple components:

- Multi‑repo coordination (backend, demo frontend, Azure Functions)
- CI/CD pipelines using GitHub Actions with OIDC authentication
- Deployment slots for staging and production environments
- Automated versioned deployments to Azure App Service
- Independent release pipeline for `slotplanner-demo-functions`
- Rollback strategy using App Service slot swaps
- Consistent schema evolution and migration workflow

A dedicated meta repository orchestrates cross‑service releases, environment
configuration, and deployment order. This reflects a production‑grade release
management approach suitable for distributed systems.

---

## Screenshots and Diagrams

The `/screenshots/` and `/docs/` directories contain:

- User interface previews
- Architecture diagrams
- Sequence diagrams
- Booking workflow illustrations
- Administrative interface overview

These materials demonstrate the system without exposing internal implementation details.

---

## Repository Structure

```
slotplanner-showcase/
├── README.md
├── .gitignore
├── docs/
│   ├── architecture/
│   ├── data-model/
│   ├── flows/
│   ├── api/
│   └── deployment/
└── demo/
    ├── backend/        # FastAPI demo backend (activities + bookings)
    ├── frontend/       # HTML/CSS/JS demo calendar and booking UI
    └── static/         # Images and assets used by the demo

```

---

## Meta Repository (Overview)

Slotplanner’s components are coordinated through a separate meta repository
that manages unified versioning, deployment sequencing, shared configuration,
and release documentation. This repository is not part of the public showcase
but represents the production‑grade release orchestration used for the full
system.

---
