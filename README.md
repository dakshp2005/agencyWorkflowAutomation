# Agency Workflow Automation

An AI-powered internal tool for small/mid-sized agencies to automate outreach emails, classify client replies, schedule meetings, generate proposals/documents — with a Human-in-the-Loop approval layer throughout.

## Architecture

Built with a robust full-stack foundation utilizing Flask application factory patterns with proper SQLAlchemy ORM database models. The UI uses pure CSS custom design mimicking shadcn/ui. The system intelligence leverages local FAISS vector stores combined with Google Gemini 1.5 for semantic document retrieval and generative content (emails, reports, proposal drafts).

## Setup Instructions

1. **Clone the repository**
2. **Setup virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Download NLP Spacy Model**:
   ```bash
   python -m spacy download en_core_web_sm
   ```
5. **Environment Configuration**:
   - Copy `.env.example` to `.env`
   - Fill in your `GEMINI_API_KEY`, `GMAIL_USER`, `GMAIL_APP_PASSWORD`, `SLACK_WEBHOOK_URL`.
   - Setup Google Calendar OAuth and place the `credentials.json` in the root.

## Setup Requirements Documentation
- **Gmail App Passwords**: Navigate to your Google Account -> Security -> App Passwords and create a 16 character code to place in `.env`.
- **Calendar API**: Setup OAuth Client ID in Google Cloud Platform and download `credentials.json`. 

## Running the Application

1. **Initialize Database and Migrations**:
   ```bash
   flask db init
   flask db migrate -m "Init"
   flask db upgrade
   ```
2. **Run Server & Background Process**:
   ```bash
   python run.py
   ```

## Testing features
- **Mock Fallback**: If `.env` is absent, the services will degrade gracefully and run basic stubs/prints, logging errors to console but not crashing the whole app.
- **RAG Bootstrap**: Navigate to `/api/rag/reindex` to ingest initial clients database.
