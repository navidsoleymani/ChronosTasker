# 📦 Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)  
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added
- Support for task metadata and tracking
- Persian (`fa`) localization files
- Dockerized Flower monitoring tool

### Changed
- Updated Redis connection URL to be environment-based
- Moved scheduler logic to `core/utils/scheduler.py`

### Fixed
- Issue with timezone mismatch in Celery Beat
- Bug when listing periodic tasks without `interval` field

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
