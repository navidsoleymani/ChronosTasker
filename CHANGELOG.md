# 📦 Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)  
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added
- `core/utils/scheduler/scheduler_engine.py`: Default in-memory scheduler using `Celery` with `apply_async` and `add_periodic_task`
- `core/utils/scheduler/scheduler_engine_beat.py`: Persistent scheduler integrated with `django-celery-beat` storing jobs in DB
- Management command `test_schedule_job` for creating and testing scheduled jobs
- Singleton instance (`scheduler_engine`) for centralized scheduling control
- Cron job registration via `PeriodicTask` and `CrontabSchedule` models
- Dynamic task naming and cleanup logic for conflicting periodic tasks

### Changed
- Modularized scheduling engine into `core/utils/scheduler/` with clear separation of volatile vs persistent strategies
- Improved exception handling and logging for job creation and scheduling
- Updated README to reflect django-celery-beat support, scheduler engine types, and usage documentation

### Fixed
- Bug with missing `description` field in `ScheduledJob` model migrations
- AttributeError for missing `schedule_one_off` during engine import (caused by old compiled `.pyc` files)
- Test setup errors due to uninitialized job scheduler

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
