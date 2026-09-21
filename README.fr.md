# Portfolio Builder API

[English](README.md) | **Français**

API REST d'un créateur de portfolios : développeurs et créatifs s'inscrivent, composent un ou plusieurs
portfolios (projets, compétences, expériences, formations, sections libres, thème) et les publient
à une adresse publique.

Construite avec **Django 5.2** et **Django REST Framework**, authentification JWT, tâches de fond
Celery et documentation OpenAPI générée automatiquement.

## Fonctionnalités

- **Comptes** : inscription, connexion JWT avec rotation et mise en liste noire des jetons de
  rafraîchissement, déconnexion, endpoint de profil `/api/me/`. Le profil et les préférences de
  notification sont créés automatiquement à l'inscription (signaux Django).
- **Portfolios** : adressés par slug, visibilité `public` / `private`, domaine personnalisé
  optionnel, portfolio par défaut par utilisateur, action `publish`. Les portfolios publics sont
  lisibles sans compte ; toute modification est réservée au propriétaire.
- **Contenu** : projets (stack technique, liens GitHub et démo, mise en avant, ordre d'affichage),
  catégories de compétences et compétences avec niveau, expériences, formations et sections libres.
- **Thèmes et médias** : thèmes au choix, fichiers envoyés avec type, taille et type MIME.
- **Notifications** : messages du formulaire de contact, préférences d'e-mail par utilisateur,
  journal des e-mails avec statut d'envoi. Les e-mails partent via des tâches Celery avec
  nouvelles tentatives automatiques.
- **Prêt pour la production** : pagination, filtres, recherche et tri sur les listes, limitation
  de débit (plus stricte sur l'inscription et la connexion), fichiers de logs rotatifs, métriques
  Prometheus, suivi d'erreurs Sentry, HSTS et cookies sécurisés en production.

## Stack technique

| Couche | Outils |
|---|---|
| API | Django 5.2, Django REST Framework, django-filter |
| Authentification | Simple JWT (accès 60 min, rafraîchissement 7 jours, rotation + liste noire) |
| Tâches asynchrones | Celery, Redis (broker), Celery Beat pour le nettoyage périodique |
| Base de données | SQLite en développement, PostgreSQL en production |
| Documentation | drf-spectacular (OpenAPI 3, Swagger UI, ReDoc) |
| Observabilité | django-prometheus, Sentry, logs fichiers |
| Qualité | pytest, pytest-django, factory_boy, coverage, flake8, black, isort |

## Structure du projet

```
apps/
  accounts/        utilisateurs, profils, inscription, /me
  portfolios/      portfolios, projets, compétences, expériences, formations
  sections/        sections libres des portfolios
  themes/          thèmes
  media/           fichiers envoyés
  notifications/   messages de contact, préférences et journal des e-mails, tâches Celery
config/
  settings/        base.py, dev.py, prod.py
  celery.py        application Celery et planning Beat
shared/            permissions, pagination, limitation de débit
tests/             unit/, integration/, functional/
```

## Aperçu de l'API

La documentation interactive est servie sur **`/api/docs/`** (Swagger UI) et **`/api/redoc/`**.
Le schéma brut est disponible sur `/api/schema/`.

| Endpoint | Description |
|---|---|
| `POST /api/auth/register/` | Créer un compte |
| `POST /api/auth/token/` | Obtenir les jetons d'accès et de rafraîchissement |
| `POST /api/auth/token/refresh/` | Renouveler le jeton d'accès |
| `POST /api/auth/logout/` | Mettre un jeton de rafraîchissement en liste noire |
| `GET /api/me/` | Utilisateur connecté et son profil |
| `/api/portfolios/` | CRUD ; `list` et `retrieve` sont publics, `POST /api/portfolios/{slug}/publish/` |
| `/api/projects/`, `/api/skills/`, `/api/skill-categories/`, `/api/experiences/`, `/api/educations/` | Contenu du portfolio |
| `/api/sections/`, `/api/themes/`, `/api/media-files/` | Mise en page, thèmes et médias |
| `/api/contact-messages/`, `/api/notification-preferences/`, `/api/email-logs/` | Notifications |

Les requêtes authentifiées utilisent l'en-tête `Authorization: Bearer <access_token>`.

## Démarrage

Python 3.11 ou plus récent.

```bash
git clone https://github.com/ibrahko/portfolio-api-builder.git
cd portfolio-api-builder
python -m venv .venv
source .venv/bin/activate          # Windows : .venv\Scripts\activate
pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Ouvrez ensuite http://127.0.0.1:8000/api/docs/.

La configuration de développement (`config.settings.dev`) utilise SQLite, affiche les e-mails dans
la console et exécute les tâches Celery de façon synchrone : **Redis n'est pas nécessaire en local**.

## Lancer les tests

```bash
pytest
pytest --cov=apps --cov-report=term-missing
```

La suite compte 38 tests : unitaires (modèles, serializers, permissions), d'intégration
(authentification, portfolios) et fonctionnels (parcours utilisateur complets).

## Configuration de production

La configuration de production se trouve dans `config/settings/prod.py` et lit tous les secrets
dans l'environnement. `.env.example` liste chaque variable à définir sur le serveur
(`DJANGO_SETTINGS_MODULE=config.settings.prod`, clé secrète, PostgreSQL, Redis, SMTP, Sentry).

```bash
gunicorn config.wsgi:application
celery -A config worker -l info
celery -A config beat -l info
```

## Feuille de route

- Environnement Docker Compose (API, PostgreSQL, Redis, Celery, Nginx)
- Intégration continue GitHub Actions (tests et lint)
- Client front-end pour l'éditeur de portfolio

## Auteur

**Ibrahima Koné** — développeur backend et consultant IT basé en Afrique de l'Ouest.
[GitHub](https://github.com/ibrahko)
