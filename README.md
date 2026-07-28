# Slotplanner – Architecture and System Overview

Slotplanner is a scheduling and resource‑management platform designed to handle bookings, activities, clients, and administrative workflows. This repository provides a public, high‑level overview of the system’s architecture, data model, API structure, and Azure deployment approach. No production code is included.

## Architecture Overview

Slotplanner follows a modular, service‑oriented architecture:

- Backend: FastAPI
- ORM/Data Layer: SQLAlchemy
- Schemas and Validation: Pydantic
- Frontend: React with TypeScript
- Hosting: Azure App Service
- Authentication: Azure Entra ID
- Storage: Azure Storage
- CI/CD: GitHub Actions

The system is organized into clear domains such as clients, activities, bookings, and administrative management.

## Data Model

The platform uses a relational schema with entities including:

- Clients
- Client relatives
- Activities
- Bookings
- Domains
- Administrative users
- Audit fields (created_by, changed_by, timestamps)

Diagrams in the `/docs/` directory illustrate relationships and workflows.

## API Design

The backend exposes a structured REST API with:

- Consistent request and response schemas
- Separation of routing, service logic, and validation
- Pydantic‑based input and output models
- Error handling and standardized responses
- Endpoints for booking operations and administrative management

Example endpoints and flows are documented in `/docs/api/`.

## Azure Deployment

Slotplanner is deployed on Azure using:

- Azure App Service for backend and frontend hosting
- Azure Storage for static assets and data
- Azure Monitor for logging and metrics
- Azure Entra ID for authentication
- Deployment slots for staging and production
- GitHub Actions for automated CI/CD

Deployment documentation is available in `/docs/deployment/`.

## Screenshots and Diagrams

The `/screenshots/` and `/docs/` directories contain:

- User interface previews
- Architecture diagrams
- Sequence diagrams
- Booking workflow illustrations
- Administrative interface overview

These materials demonstrate the system without exposing internal implementation details.

## Purpose of This Repository

This repository is intended for technical reviewers, recruiters, and hiring managers. It highlights the architectural design, engineering decisions, and structure of the Slotplanner system while keeping the production code private.

## Repository Structure

slotplanner-showcase/
├── README.md  
├── .gitignore  
├── docs/  
│   ├── architecture/  
│   ├── api/  
│   └── deployment/  
├── screenshots/  
└── demo/
