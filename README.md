# Portfolio Builder API

**English** | [Français](README.fr.md)

REST API behind a portfolio builder: developers and creatives sign up, compose one or more portfolios
(projects, skills, experience, education, custom sections, theme) and publish them at a public URL.

Built with **Django 5.2** and **Django REST Framework**, JWT authentication, Celery background jobs
and an auto-generated OpenAPI documentation.

## Features

- **Accounts** — registration, JWT login with refresh-token rotation and blacklisting, logout,
  `/api/me/` profile endpoint. A profile and notification preferences are created automatically
  on sign-up (Django signals).
- **Portfolios** — addressed by slug, `public` / `private` visibility, optional custom domain,
  default portfolio per user, `publish` action. Public portfolios are readable without an account;
  every write is restricted to the owner.
- **Content** — projects (tech stack, GitHub and live links, highlight, ordering), skill categories
  and skills with levels, experience, education and free-form sections.
- **Themes and media** — selectable themes, uploaded media files with type, size and MIME metadata.
- **Notifications** — contact form messages, per-user e-mail preferences, e-mail log with delivery
  status. E-mails are sent by Celery tasks with automatic retries.
- **Production concerns** — pagination, filtering, search and ordering on list endpoints,
  rate limiting (stricter on register and login), rotating log files, Prometheus metrics,
  Sentry error tracking, HSTS / secure cookies in production.

## Tech stack

| Layer | Tools |
|---|---|
| API | Django 5.2, Django REST Framework, django-filter |
| Auth | Simple JWT (access 60 min, refresh 7 days, rotation + blacklist) |
| Async jobs | Celery, Redis (broker), Celery Beat for periodic cleanup |
| Database | SQLite in development, PostgreSQL in production |
| Docs | drf-spectacular (OpenAPI 3, Swagger UI, ReDoc) |
| Observability | django-prometheus, Sentry, file logging |
| Quality | pytest, pytest-django, factory_boy, coverage, flake8, black, isort |

## Project structure

```
apps/
  accounts/        users, profiles, registration, /me
  portfolios/      portfolios, projects, skills, experience, education
  sections/        custom portfolio sections
  themes/          themes
  media/           uploaded files
  notifications/   contact messages, e-mail preferences and logs, Celery tasks
config/
  settings/        base.py, dev.py, prod.py
  celery.py        Celery app and Beat schedule
shared/            permissions, pagination, throttles
tests/             unit/, integration/, functional/
```

## API overview

Interactive documentation is served at **`/api/docs/`** (Swagger UI) and **`/api/redoc/`**.
The raw schema is available at `/api/schema/`.

| Endpoint | Description |
|---|---|
| `POST /api/auth/register/` | Create an account |
| `POST /api/auth/token/` | Obtain access and refresh tokens |
| `POST /api/auth/token/refresh/` | Refresh the access token |
| `POST /api/auth/logout/` | Blacklist a refresh token |
| `GET /api/me/` | Current user and profile |
| `/api/portfolios/` | CRUD; `list` and `retrieve` are public, `POST /api/portfolios/{slug}/publish/` |
| `/api/projects/`, `/api/skills/`, `/api/skill-categories/`, `/api/experiences/`, `/api/educations/` | Portfolio content |
| `/api/sections/`, `/api/themes/`, `/api/media-files/` | Layout, themes and media |
| `/api/contact-messages/`, `/api/notification-preferences/`, `/api/email-logs/` | Notifications |

Authenticated requests use the header `Authorization: Bearer <access_token>`.

## Getting started

Requires Python 3.11+.

```bash
git clone https://github.com/ibrahko/portfolio-api-builder.git
cd portfolio-api-builder
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Then open http://127.0.0.1:8000/api/docs/.

Development settings (`config.settings.dev`) use SQLite, print e-mails to the console and run
Celery tasks synchronously, so **Redis is not needed locally**.

## Running the tests

```bash
pytest
pytest --cov=apps --cov-report=term-missing
```

The suite contains 38 tests split into unit (models, serializers, permissions), integration
(authentication, portfolios) and functional (end-to-end user flows) tests.

## Production configuration

Production settings live in `config/settings/prod.py` and read every secret from the environment.
`.env.example` lists every variable to define in the server environment
(`DJANGO_SETTINGS_MODULE=config.settings.prod`, secret key, PostgreSQL, Redis, SMTP, Sentry).

```bash
gunicorn config.wsgi:application
celery -A config worker -l info
celery -A config beat -l info
```

## Roadmap

- Docker Compose setup (API, PostgreSQL, Redis, Celery, Nginx)
- GitHub Actions CI running tests and linting
- Front-end client for the portfolio editor

## Author

**Ibrahima Koné** — backend developer and IT consultant based in West Africa.
[GitHub](https://github.com/ibrahko)
