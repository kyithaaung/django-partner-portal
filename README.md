# Django Partner Portal

## About the "red minus" lines in your PR diff

If you see **red lines prefixed with `-`** in GitHub/Git diff, that is **not an error by itself**.
It means those lines were removed or replaced by the new change.

- `-` (red): old code/text removed
- `+` (green): new code/text added

So the red minus is expected whenever a file is edited.

---

## Fix for the previous environment issue (Django missing)

The previous run failed because Django wasn't installed in the runtime environment.

This repo now includes `requirements.txt` so dependencies are explicit.

## Important: run commands from project root

You must run commands from the folder that contains `manage.py`.
In your error, you ran from `...\config`, so `core/forms.py` was not found.

### Windows example

```bat
cd D:\django-learning-app
```

Then run:

```bat
python -m py_compile config\__init__.py config\settings.py config\urls.py core\models.py core\forms.py core\views.py core\urls.py core\serializers.py core\tests.py core\routers.py
```

If you are already inside `D:\django-learning-app\config`, either:

- go up one level first: `cd ..`
- or use relative paths with `..\` prefix.

### 1) Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 2) Run migrations (SQLite quick start)

```bash
python manage.py migrate
```

### 3) Start server

```bash
python manage.py runserver 0.0.0.0:8000
```

---

## URLs to test on local laptop

After running `python manage.py runserver 0.0.0.0:8000`, open:

- `http://127.0.0.1:8000/login/` (login page)
- `http://127.0.0.1:8000/` (portal dashboard, login required)
- `http://127.0.0.1:8000/admin/` (admin)

If you still see only `admin/` in the Django 404 debug page, confirm `config/urls.py` includes `path("", include("core.urls"))` and restart the server.

---

## Database mode

By default, settings use SQLite for local development.

To use split MySQL databases (`default` + `partner`), set:

```bash
export USE_SQLITE=false
```

Then configure values from `.env.example` and start services with Docker Compose.

```bash
docker compose up -d mysql_internal mysql_partner
python manage.py migrate --database=default
python manage.py migrate --database=partner
```

---

## Security notes

See `SECURITY.md` for hardening recommendations.
