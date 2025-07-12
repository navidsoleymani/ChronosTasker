# 📦 Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)  
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added
- ✅ **API**: `ScheduledJobViewSet` with full CRUD and custom actions `activate`/`deactivate`
- ✅ **Celery Task**: New `send_email_task` simulating email delivery with subject/body to recipients
- ✅ **Swagger**: Auto-generated OpenAPI schema for `/jobs/`, `/jobs/{id}/activate/`, `/jobs/{id}/deactivate/`
- ✅ **Admin Command**: `test_schedule_job` for testing one-off job execution
- ✅ **Localization**: Persian translations added for scheduler app
- ✅ **Documentation**: Full `README.md` overhaul with features, structure, setup, Docker, scheduling engine config
- ✅ **Project Structure**:
  - `scheduler/serializers.py`, `services.py`, `views.py`, `urls.py`
  - `core/utils/scheduler/scheduler_engine.py`: Default in-memory scheduler using `Celery`
  - `core/utils/scheduler/beat_scheduler_engine.py`: Persistent engine using `django-celery-beat`

### Changed
- 🔧 Modularized scheduler logic into `scheduler_engine` and `beat_scheduler_engine` under `core/utils/scheduler/`
- 🔧 Improved logging and error handling in `run_scheduled_job` task
- 🔧 Enhanced `run_scheduled_job` to handle retries with `job.max_retries` and `job.end_time`
- 🔧 Swagger documentation enriched with detailed descriptions and parameter metadata
- 🔧 README now includes:
  - Task engine types
  - cURL example for posting new jobs
  - Sample `send_email_task` and test instructions
  - Switching to persistent engine (django-celery-beat)

### Fixed
- 🐞 AttributeError during `scheduler_engine` import caused by stale `.pyc` files
- 🐞 `ScheduledJob` migration missing `description` field (fixed in `0002_...`)
- 🐞 Missing job scheduling during `.save()` (hooked via `perform_create`, `perform_update` in ViewSet)

---

## [1.0.0] - 2025-07-11

### Added
- Initial Django project with Celery integration
- Redis-based broker configuration
- Base models for job & schedule
- REST API for submitting and listing scheduled jobs
- Dockerfile and docker-compose setup
- English localization

---

## [0.1.0] - 2025-07-10

### Added
- Project scaffold and structure
- Basic README and requirements.txt

---

## 🔄 Versioning

This project uses **Semantic Versioning**:

MAJOR.MINOR.PATCH

- **MAJOR**: Breaking changes
- **MINOR**: Backward-compatible new features
- **PATCH**: Backward-compatible bug fixes

---

## 📌 Legend

- **Added** – new features  
- **Changed** – modifications in existing functionality  
- **Deprecated** – soon-to-be removed features  
- **Removed** – deprecated features now removed  
- **Fixed** – any bug fixes  
- **Security** – vulnerabilities fixed  
