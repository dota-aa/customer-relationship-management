# 🚀 Enterprise Customer Relationship Management (CRM) API

A high-performance, modular RESTful API for Customer Relationship Management (CRM) built with **Python**, **Django**, and **Django REST Framework (DRF)**.

The architecture strictly follows the **Service-Selector Pattern** to isolate domain logic from HTTP handling, incorporates **Pydantic** for rigorous data validation and DTO transformations across domain boundaries, and provides robust reusable utility layers.

---

## 📑 Table of Contents
- [Architecture & Design Principles](#-architecture--design-principles)
- [Key Features & Business Modules](#-key-features--business-modules)
- [Pydantic Validation & DTO Layer](#-pydantic-validation--dto-layer)
- [Reusable Functions & Utilities](#-reusable-functions--utilities)
- [Tech Stack](#-tech-stack)
- [Project Directory Layout](#-project-directory-layout)
- [Installation & Setup](#-installation--setup)
- [API Endpoints Reference](#-api-endpoints-reference)
- [Roadmap & Upcoming Architecture](#-roadmap--upcoming-architecture)

---

## 🏛 Architecture & Design Principles

The application is engineered with a layered, decoupled design:
- **Presentation Layer (`api_views.py`, `serializers.py`)**: Responsible exclusively for HTTP parsing, request routing, DRF permissions, and response serialization.
- **Service Layer (`services.py`)**: Encapsulates state-changing business operations, atomic database transactions (`transaction.atomic`), and external integration triggers.
- **Selector Layer (`selectors.py`)**: Isolates query logic, aggregations, and ORM performance optimizations (`select_related`, `prefetch_related`, `only`).
- **Validation Layer (Pydantic)**: Acts as the gatekeeper for data contracts, sanitizing inputs and validating complex invariants before persistence.
- **Event Observers (`signals.py`)**: Decouples side-effects, such as logging user activities upon record updates.

---

## 📦 Key Features & Business Modules

- **Accounts & Authentication (`apps/accounts`)**:
  - Custom User Model (`email` as username identifier).
  - Profile management with avatar storage.
  - Token-based authentication using **JWT** (`SimpleJWT`) with token refresh mechanisms.
  - Multi-step registration with email verification tokens.

- **Lead Management (`apps/leads`)**:
  - Full lifecycle tracking of inbound leads.
  - Source tracking (`WEBSITE`, `REFERRAL`, `SOCIAL`, `EMAIL`, `OTHER`).
  - Funnel status transitions (`NEW`, `IN_PROGRESS`, `QUALIFIED`, `CONVERTED`, `LOST`, `JUNK`).

- **Deals & Pipeline (`apps/deals`)**:
  - Revenue opportunity and pipeline stages (`LEAD`, `QUALIFIED`, `PROPOSAL`, `NEGOTIATION`, `CLOSED_WON`, `CLOSED_LOST`).
  - Stage probability calculation and expected close date tracking.
  - Relation mapping between contacts, companies, and sales reps.

- **Contact Directory (`apps/contacts`)**:
  - Customer directory with communication logs and company relationships.

- **Dashboard & Activity Logs (`apps/dashboard`)**:
  - Real-time audit trail capturing user IP address, User-Agent, activity types, and modified target instances.
  - Aggregated analytics for managers and sales executives.

- **Notes & Collaboration (`apps/notes`)**:
  - Contextual notes attached to leads and deals with categorization and priority levels (`LOW`, `MEDIUM`, `HIGH`).

- **Notifications (`apps/notifications`)**:
  - Notification delivery system with customizable user notification preferences (`NotificationSettings`).

- **Transactional Mailing (`apps/mailing`)**:
  - HTML-templated emails for user onboarding, account activation, and security alerts.

---

## 🛡 Pydantic Validation & DTO Layer

**Pydantic** is deeply integrated into the service and validation layer to ensure strict type safety, data integrity, and payload normalization before data reaches the ORM layer.

### Applied Pydantic Validations:
- **Account & Security Validation**: Strict password complexity (minimum length, special characters, uppercase and digit enforcement) and RFC-compliant email verification.
- **Phone Number Normalization**: International E.164 phone number pattern matching and normalization.
- **Financial & Deal Constraints**: Strict bounds for deal amounts (`amount > 0`), probability percentages (`0 <= probability <= 100`), and date timeline consistency (`expected_close_date >= today`).
- **Input Sanitization**: Trimming whitespaces, stripping unsafe tags, and checking length bounds on text/note inputs.

---

## 🧩 Reusable Functions & Utilities

The project houses reusable components in `utils/` and `core/` to eliminate boilerplate and ensure consistency:

- **S3 / Cloud Storage Manager (`utils/bucket.py`)**:
  - `BucketManager`: Reusable client wrapping `boto3` for handling file uploads, generating CDN-accessible paths, and managing private media objects.
- **Request Metadata Parser (`utils/request_utils.py`)**:
  - `get_client_ip(request)`: Safely extracts real client IP addresses across reverse proxies (`X-Forwarded-For`).
  - `get_user_agent(request)`: Extracts and parses client User-Agent strings for audit logging.
- **Abstract Audit Model (`core/models.py`)**:
  - `BaseModel`: Base abstract model providing indexed `created_at` and `updated_at` timestamps for all entities.
- **Standardized Pagination (`core/pagination.py`)**:
  - Uniform page-size and metadata pagination format across all list endpoints.

---

## 🛠 Tech Stack

- **Language**: Python 3.11+
- **Web Framework**: Django 5.x / 6.x
- **REST API Framework**: Django REST Framework (DRF)
- **Data Validation & DTOs**: Pydantic v2
- **Authentication**: JWT (`djangorestframework-simplejwt`)
- **Database**: PostgreSQL (Production) / SQLite (Local Development)
- **Storage / Cloud**: `django-storages` + `boto3` (AWS S3 compatible)

---

## 📂 Project Directory Layout
```text
├── apps/
│   ├── accounts/         # Authentication, user profiles, selectors & services
│   ├── contacts/         # Contacts directory and customer interactions
│   ├── dashboard/        # Activity logs, analytics, dashboard metrics
│   ├── deals/            # Deals pipeline, opportunity lifecycle
│   ├── leads/            # Lead ingestion and stage tracking
│   ├── mailing/          # Email dispatch engine and HTML templates
│   ├── notes/            # Contextual prioritized notes
│   └── notifications/    # Notification triggers and user preferences
├── config/               # Django root configuration, routing, ASGI/WSGI
├── core/                 # Shared base models, mixins, pagination
├── utils/                # Reusable utilities (S3 bucket, IP helpers, validators)
├── manage.py
└── requirements.txt
```


## 🚀 Installation & Setup

### 1. Clone & Setup Virtual Environment

git clone <repository-url>
cd customer-relationship-management-master

## Create virtual environment
```bash
python -m venv venv
```

# Activate virtual environment

### Windows (PowerShell):

```bash
.\venv\Scripts\Activate.ps1
```

### Linux / macOS:
source venv/bin/activate

## 2. Install Dependencies
```bash
pip install -r requirements.txt
```

## 🔮 Roadmap & Upcoming Architecture

The following enterprise capabilities are architected for upcoming integration:

- [ ] **Redis Caching Layer (`django-redis`)**:
  - High-performance in-memory caching for frequently accessed read queries (dashboard summaries, lead lists).
  - Centralized cache storage for token blacklisting and session management.
- [ ] **Asynchronous Task Processing (`Celery` + `RabbitMQ`)**:
  - Offloading heavy I/O operations (transactional emails, verification link generation) to background workers.
  - RabbitMQ as a reliable, high-throughput message broker.
  - Periodic Celery Beat tasks for stale lead reminders and automated deal report exports.
- [ ] **Automated API Documentation**:
  - OpenAPI 3 / Swagger specification via `drf-spectacular`.
