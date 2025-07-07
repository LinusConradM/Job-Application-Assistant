# Job-Application-Assistant
Tired of manual job description assessment, let an agent assist you.

This application fetches job listings from a configured URL using Selenium, stores them in a database, and exposes them via a FastAPI endpoint.

## Features
- Configure the job portal URL and scraping interval via environment variables.
- Scrape job listings (title, company, description, location, skills, salary) regularly using Selenium.
- Store listings in SQLite (or other DB via `DATABASE_URL`).
- List all stored jobs via API (`GET /jobs`).

## Installation

1. Clone the repository and navigate into it:
   ```bash
   git clone <repo-url>
   cd Job-Application-Assistant
   ```
2. Create a virtual environment and install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

## Configuration

Copy `.env.example` to `.env` and set your values:
```dotenv
.env
JOB_URL=https://example.com/jobs
SCRAPE_INTERVAL_MINUTES=60
DATABASE_URL=sqlite:///./jobs.db
```

## Running

- To start the API and scheduler:
  ```bash
  uvicorn app.main:app --reload
  ```

- The scraper runs once at startup and then at the configured interval.

-- List jobs via:
  ```bash
  curl http://127.0.0.1:8000/jobs
  ```

## Gradio UI

You can also launch an interactive Gradio interface to fetch and view jobs in your browser:

```bash
python gradio_app.py
```

Open the local URL shown in the console and click **Fetch Jobs Now** to scrape from the configured portal and display stored listings.

### ATS Assessment

Within the Gradio interface, after fetching jobs, you can upload your CV (PDF or TXT), select a specific job from the dropdown, and click **Assess CV**. The system will display:

- Match percentage of your CV against the job's required skills
- List of missing skills
- Red flags (e.g., employment gap > 12 months)

## Deploying on Hugging Face Spaces

1. Push this repository to a new Hugging Face Space (select **Gradio** as the SDK).
2. In your space settings, add any required environment variables (e.g. `JOB_URL`, `SCRAPE_INTERVAL_MINUTES`, `DATABASE_URL`) or upload a `.env` file.
3. The space will automatically install dependencies from `requirements.txt` and launch `gradio_app.py`.
