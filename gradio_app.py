#!/usr/bin/env python3
"""
Gradio-based UI for Job Application Assistant
"""
import os
from dotenv import load_dotenv

load_dotenv()

import gradio as gr

from app.tasks import scrape_and_store
from app.database import SessionLocal
from app.models import Job


def fetch_and_list():
    """Trigger a scraping run and return all stored jobs."""
    scrape_and_store()
    db = SessionLocal()
    jobs = db.query(Job).all()
    db.close()
    data = [
        [
            job.title,
            job.company,
            job.description,
            job.location,
            job.skills,
            job.salary or "",
        ]
        for job in jobs
    ]
    return data


def main():
    with gr.Blocks() as demo:
        gr.Markdown("# Job Listings")
        btn = gr.Button("Fetch Jobs Now")
        table = gr.Dataframe(
            headers=["Title", "Company", "Description", "Location", "Skills", "Salary"],
            row_count=(0, None),
            col_count=(0, 6),
        )
        btn.click(fn=fetch_and_list, inputs=None, outputs=table)
    demo.launch(server_name="0.0.0.0", server_port=int(os.getenv("PORT", 7860)))


if __name__ == "__main__":
    main()