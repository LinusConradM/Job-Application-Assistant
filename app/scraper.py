import time
import logging

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from .config import settings

logger = logging.getLogger(__name__)


class JobScraper:
    def __init__(self, url: str = settings.JOB_URL):
        if not url:
            raise ValueError("JOB_URL must be set in environment or .env")
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options,
        )
        self.url = url

    def fetch_jobs(self):
        jobs = []
        logger.info("Fetching jobs from %s", self.url)
        try:
            self.driver.get(self.url)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            time.sleep(2)
            job_elements = self.driver.find_elements(By.CSS_SELECTOR, ".job-listing")
            for elem in job_elements:
                try:
                    title = elem.find_element(By.CSS_SELECTOR, ".job-title").text
                    company = elem.find_element(By.CSS_SELECTOR, ".company").text
                    description = elem.find_element(By.CSS_SELECTOR, ".description").text
                    location = elem.find_element(By.CSS_SELECTOR, ".location").text
                    skills = elem.find_element(By.CSS_SELECTOR, ".skills").text
                    try:
                        salary = elem.find_element(By.CSS_SELECTOR, ".salary").text
                    except Exception:
                        salary = None
                    jobs.append({
                        "title": title,
                        "company": company,
                        "description": description,
                        "location": location,
                        "skills": skills,
                        "salary": salary,
                    })
                except Exception:
                    continue
        except WebDriverException as e:
            logger.error("Error loading page %s: %s", self.url, e)
            return jobs

        logger.info("Found %d job listings", len(jobs))
        return jobs

    def close(self):
        if self.driver:
            logger.info("Closing Selenium WebDriver")
            self.driver.quit()
