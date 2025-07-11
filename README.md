# 🚀 ChronosTasker

> **A scalable, maintainable, and robust Django-based task scheduling system using Celery and Redis.**  
> Designed for asynchronous and periodic task execution with multi-language support and containerized deployment.

---

## 📚 Table of Contents

- [Introduction](#-introduction)
- [Features](#-features)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Running the Application](#-running-the-application)
- [Celery & Task Scheduling](#-celery--task-scheduling)
- [Scheduler Engines](#-scheduler-engines)
- [Localization](#-localization)
- [Testing](#-testing)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact](#-contact)

---

## 📝 Introduction

**ChronosTasker** is a modern backend service developed in **Django** to handle **asynchronous background tasks** and **periodic job scheduling** efficiently. Leveraging **Celery** with **Redis** as the message broker, it supports scalable task execution, job monitoring, and concurrency management.

The system includes:

- Modular architecture for easy extension
- Multi-language support (English & Persian)
- Dockerized environment for effortless deployment
- Clean, well-commented codebase for maintainability

---

## 🌟 Features

- ✅ Asynchronous task processing with Celery workers
- ✅ Periodic task scheduling via Celery Beat
- ✅ Redis-powered message brokering and caching
- ✅ Fully containerized using Docker and Docker Compose
- ✅ Multi-language support (English, Persian)
- ✅ Optional Celery monitoring via Flower dashboard
- ✅ Clean modular Django project structure
- ✅ Comprehensive code documentation and comments

---

## 🛠️ Technology Stack

| Technology     | Purpose                                | Version       |
|----------------|----------------------------------------|---------------|
| Python         | Backend programming language           | 3.12          |
| Django         | Web framework                          | Latest (4.x)  |
| Celery         | Distributed task queue                 | Latest stable |
| Redis          | Message broker & caching               | 7.x           |
| Docker         | Containerization                       | 20.x+         |
| Docker Compose | Multi-container orchestration          | 1.29+         |
| Flower         | Celery monitoring dashboard (optional) | Latest stable |
| PostgreSQL     | Database (optional for Django & Beat)  | 15.x          |

---

## 🏗️ Project Structure

```plaintext
ChronosTasker/
├── config/                 # Django project configuration & Celery app
│   ├── celery.py           # Celery app instance & settings
│   ├── settings/           # Django settings by environment
│   ├── urls.py             # Project-level URL routing
│   └── ...
├── core/                   # Core utilities and shared logic
│   ├── tasks.py            # Generic Celery tasks
│   └── utils/
│       └── scheduler/
│           ├── scheduler_engine.py        # In-memory scheduler engine
│           └── beat_scheduler_engine.py   # Persistent scheduler engine (using django-celery-beat)
├── scheduler/              # Main scheduling Django app
│   ├── models.py           # Job and schedule ORM models
│   ├── serializers.py      # API serializers
│   ├── services.py         # Business logic & service layer
│   ├── tasks.py            # Scheduler-specific Celery tasks
│   ├── views.py            # API views & endpoints
│   └── urls.py             # App-level URL routing
├── tests/                  # Unit and integration tests
│   └── scheduler/
│       └── test_tasks.py
├── Dockerfile              # Docker image build instructions
├── docker-compose.yml      # Docker compose orchestration
├── requirements.txt        # Python dependencies
├── manage.py               # Django management CLI
└── README.md               # This documentation
```

## ⚙️ Installation

### Prerequisites

- Docker & Docker Compose installed
- (Optional) Python 3.12+ for local non-Docker development
- Redis server (local or remote)

### Steps

```bash
# Clone the repository
git clone https://github.com/navidsoleymani/ChronosTasker.git
cd ChronosTasker

# (Optional) Create and activate virtual environment for local development
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Environment Setup

Create a .env file based on SAMPLE_ENV.txt and update configuration such as:

```ini
# Environment type
DJANGO_ENV=dev

# SECURITY
SECRET_KEY=my-secret-key
DEBUG=False
DEPLOY_STATE=True

# DATABASE
DB_TYPE=postgresql
DATABASE_ENGINE=django.db.backends.postgresql_psycopg2
DATABASE_NAME=my_db_name
DATABASE_USER=my_db_user
DATABASE_PASSWORD=my_db_password
DATABASE_HOST=127.0.0.1
DATABASE_PORT=5432

# CACHE (Redis)
REDIS_LOCATION=redis://127.0.0.1:6379/1
REDIS_TIMEOUT=300

# CELERY
CELERY_BROKER_URL=redis://127.0.0.1:6379/0
CELERY_RESULT_BACKEND=redis://127.0.0.1:6379/1
```

## ▶️ Running the Application

### With Docker Compose (Recommended)

```bash
docker-compose up --build
```

- Django server: http://localhost:8000
- Redis broker: default Redis port 6379
- Celery worker & beat: auto-started
- Flower monitoring UI: http://localhost:5555 (if enabled)

### Running Locally Without Docker

1. Ensure Redis is running locally or remotely.

2. Apply migrations:

```bash
python manage.py migrate
```

3. Run Django development server:

```bash
python manage.py runserver
```

4. Start Celery worker:

```bash
celery -A config worker -l info
```

5. Start Celery beat scheduler:

```bash
celery -A config beat -l info
```

## 🔄 Celery & Task Scheduling

- Celery app is configured in `config/celery.py`
- Redis is used as the broker for message passing
- Periodic tasks managed by Celery Beat
- Task implementations located under:
    - `scheduler/tasks.py` — Scheduler-specific Celery task handlers
    - `core/tasks.py` — General-purpose reusable Celery tasks
- Scheduling interfaces live in `core/utils/scheduler/` folder

---

## 🔁 Scheduler Engines

ChronosTasker supports two types of job schedulers:

| Engine Type     | Description                                                              |
|----------------|---------------------------------------------------------------------------|
| In-Memory       | Default mode using Celery’s `add_periodic_task()` – not persistent       |
| Persistent (Beat)| Uses `django-celery-beat` for DB-backed persistent periodic scheduling   |

### 🧩 Switching to Persistent Scheduler (django-celery-beat)

1. Install the dependency:

```bash
pip install django-celery-beat
```

2. Add it to your `INSTALLED_APPS`:

```python
INSTALLED_APPS += ['django_celery_beat']
```

3. Apply migrations:

```bash
python manage.py migrate
```

4. Use the persistent engine in your code:

```python
from core.utils.scheduler.beat_scheduler_engine import scheduler_engine
```

5. Start the beat scheduler with:

```bash
celery -A config beat -l info
```

---

## 🌐 Localization

- Supports English (en) and Persian (fa) languages
- Translation files are managed with Django's makemessages and compilemessages commands
- Localization files are located under the locale/ directory
- Language is configurable via LANGUAGE_CODE in settings or runtime headers

---

## 🧪 Testing

Run the test suite with:

```bash
pytest
```

You can also test a scheduled job manually via:

```bash
python manage.py test_schedule_job
```

This command creates and schedules a `ScheduledJob` to run as a one-off task.

---

## 🤝 Contributing

Contributions are welcome and encouraged!
Please ensure:

- Follow the existing code style and best practices
- Write clear, concise commit messages
- Add tests for new features or bug fixes
- Open issues or pull requests with detailed descriptions

---

## 📄 License

This project is licensed under the MIT License — see the LICENSE file for details.

---

## 📞 Contact

Developed and maintained by Navid Soleymani  
Email: navidsoleymani@ymail.com  
GitHub: https://github.com/navidsoleymani

<p align="center"> <em>Thank you for choosing ChronosTasker! ⏳⚙️</em> </p>