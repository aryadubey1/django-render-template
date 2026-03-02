# {{cookiecutter.project_name}}

{{cookiecutter.description}}

**Author:** {{cookiecutter.author}}

---

## Local Setup

```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

pip install -r requirements.txt

cp .env.example .env         # then edit .env with your values

python manage.py migrate
python manage.py runserver
```

## Deploy to Render

1. Push this repo to GitHub
2. Create a new **Web Service** on Render, connect your repo
3. Set **Build Command** to: `./build.sh`
4. Set **Start Command** to: `gunicorn {{cookiecutter.project_slug}}.wsgi`
5. Add these environment variables in Render dashboard:
   - `SECRET_KEY`
   - `DJANGO_SUPERUSER_USERNAME`
   - `DJANGO_SUPERUSER_EMAIL`
   - `DJANGO_SUPERUSER_PASSWORD`
6. Add a **PostgreSQL** database and Render sets `DATABASE_URL` automatically

That's it — deploy!
