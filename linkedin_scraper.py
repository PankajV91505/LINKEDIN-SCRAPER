# linkedin_scraper.py
import asyncio
import json
import time
import pandas as pd
import random
from playwright.async_api import async_playwright

# Human-like scrolling
async def human_scroll(page, duration=5):
    start = time.time()
    while time.time() - start < duration:
        await page.mouse.wheel(0, 500)
        await asyncio.sleep(1)

# Main scraping logic
async def scrape():
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=False, slow_mo=100)
        context = await browser.new_context()

        # Load cookies (for auto-login)
        with open("cookies.json", "r") as f:
            cookies = json.load(f)["cookies"]
        await context.add_cookies(cookies)

        page = await context.new_page()

        # Step 1: Go to LinkedIn directly (already logged in)
        await page.goto("https://www.linkedin.com/feed/", wait_until="domcontentloaded")
        print("✅ Logged in using saved cookies.")

        # Step 2: Search for "Python Developer" jobs
        await page.goto("https://www.linkedin.com/jobs/search/?keywords=python%20developer")
        await asyncio.sleep(5)
        await human_scroll(page, duration=6)

        # Step 3: Collect top 5 job postings
        await page.wait_for_selector(".job-card-container--clickable", timeout=15000)
        job_cards = await page.locator(".job-card-container--clickable").all()
        top_5_jobs = job_cards[:5]

        scraped_jobs = []

        for job in top_5_jobs:
            await job.click()
            await page.wait_for_load_state("networkidle")
            time_out = random.randint(3000, 5000)  
            await page.wait_for_timeout(time_out)
            await asyncio.sleep(4)

            job_data = {}
            try:
                job_data["title"] = await page.locator("h1.t-24").text_content()
                job_data["company"] = await page.locator("div.job-details-jobs-unified-top-card__company-name a").text_content()
                job_data["location"] = await page.locator("div.job-details-jobs-unified-top-card__primary-description-container span").nth(0).text_content()
                job_data["time_posted"] = await page.locator("div.job-details-jobs-unified-top-card__primary-description-container span").nth(2).text_content()
                job_data["description"] = await page.locator("div.jobs-description-content__text--stretch").text_content()
            except Exception as e:
                print("⚠️ Error extracting fields:", e)

            scraped_jobs.append(job_data)

        # Step 4: Save to Excel
        df = pd.DataFrame(scraped_jobs)
        df.to_excel("linkedin_python_jobs.xlsx", index=False)
        print("✅ Jobs saved to linkedin_python_jobs.xlsx")

        await browser.close()

# Run the script
asyncio.run(scrape())
