# Agency Workflow Automation

An AI-powered internal tool for small/mid-sized agencies to automate outreach emails, classify client replies, schedule meetings, generate proposals/documents — with a Human-in-the-Loop approval layer throughout.

## Architecture

Built with a Flask application factory and SQLAlchemy ORM models, backed by a **Supabase Postgres** database (with the `pgvector` extension). The UI is server-rendered Jinja templates with a hand-written CSS design system (no frontend framework/build step). Semantic search/RAG over past client interactions uses `pgvector` similarity search on embeddings from Google Gemini, and generative content (emails, reports, proposal drafts) is produced with Gemini as well. Deployed as a single serverless Python function on Vercel (`api/index.py`), with all routes — including static assets — funneled through the Flask app itself.

Auth is a single flask-login based system (`/auth/login`, `/auth/signup`) protecting the whole app (dashboard, clients, emails, meetings, documents, replies, discovery).

## Setup Instructions

1. **Clone the repository**
2. **Setup virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Environment configuration**:
   - Copy `.env.example` to `.env`.
   - Fill in `DATABASE_URL` (see "Database (Supabase)" below), `GEMINI_API_KEY`, and optionally `GMAIL_USER`/`GMAIL_APP_PASSWORD`/`SLACK_WEBHOOK_URL`.
   - `.env` is only read locally (see `app/config.py`) — it is git-ignored and is **not** deployed to Vercel; production config comes entirely from Vercel's Environment Variables.

## Database (Supabase)

1. Create a Supabase project.
2. Run `supabase_schema.sql` once in the Supabase SQL Editor to create all tables, the `pgvector` extension, and indexes.
3. Get your connection string from **Supabase Dashboard → Settings → Database → Connection Pooling** and use it as `DATABASE_URL`.
   - Use the **pooler** host (`aws-0-<region>.pooler.supabase.com`), not the direct `db.<ref>.supabase.co` host — the direct host is IPv6-only and will fail to connect from Vercel (and most serverless platforms).
   - URL-encode any special characters in the password (e.g. `@` → `%40`), otherwise the connection string will parse incorrectly.
4. `flask-migrate`/Alembic is wired up (`migrations/`) for incremental schema changes going forward, but the initial schema is expected to already exist via `supabase_schema.sql`.

## Running the Application Locally

```bash
python run.py
```

This starts the dev server on `http://localhost:5000` and attempts `flask db upgrade` on startup (safe to ignore if it errors, since the schema is already managed by `supabase_schema.sql`).

## Deploying to Vercel

The repo already includes `vercel.json` and `api/index.py`. All you need to do:

1. Import the GitHub repo into a Vercel project, with **Production Branch** set to `main`.
2. In **Project Settings → Environment Variables**, set: `DATABASE_URL` (pooler string, see above), `SECRET_KEY`, `SUPABASE_URL`, `SUPABASE_KEY`, `GEMINI_API_KEY`, and any optional integration keys you use (`GMAIL_USER`, `GMAIL_APP_PASSWORD`, `SLACK_WEBHOOK_URL`, `APP_BASE_URL` set to your production URL). These are never read from `.env` in production — the app raises a clear startup error if `DATABASE_URL` is missing.
3. Push to `main` (or trigger **Redeploy** from the Deployments tab). Check the deployment's **Runtime Logs** if something fails — the app fails loudly with descriptive errors rather than degrading silently in production.

## Testing Features

- **Graceful degradation of optional integrations**: if `GMAIL_USER`/`GMAIL_APP_PASSWORD` or `SLACK_WEBHOOK_URL` are blank, those features log to the console instead of crashing (see `app/services/slack_service.py`, `app/services/email_service.py`). Same for spaCy in reply classification — it's optional and used only if installed.
- **RAG Bootstrap**: hit `/api/rag/reindex` (while logged in) to (re)index all existing clients/emails/replies/documents into `pgvector` for retrieval.
