# linkedin_scrape.py
import asyncio
import json
import time
import pandas as pd
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

# Human-like scrolling
async def human_scroll(page, duration=10):
    start = time.time()
    while time.time() - start < duration:
        await page.mouse.wheel(0, 1000)
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
        await page.goto("https://www.linkedin.com/jobs/search/?keywords=python%20developer&f_WT=2")
        await page.wait_for_selector(".job-card-container--clickable", timeout=20000)
        await human_scroll(page, duration=15)

        # Step 3: Collect job cards
        job_cards = await page.locator(".job-card-container--clickable").all()
        print(f"🔍 Found {len(job_cards)} job cards.")
        top_jobs = job_cards[:60]  # or as many as you want

        scraped_jobs = []

        for i, job in enumerate(top_jobs):
            print(f"📄 Scraping job {i+1}/{len(top_jobs)}")
            try:
                await job.scroll_into_view_if_needed()
                await job.click()
                await page.wait_for_selector("h1.t-24", timeout=10000)

                await asyncio.sleep(2)  # wait to load details

                job_data = {
                    "title": await page.locator("h1.t-24").text_content(),
                    "company": await page.locator("div.job-details-jobs-unified-top-card__company-name a").text_content(),
                    "location": await page.locator("div.job-details-jobs-unified-top-card__primary-description-container span").nth(0).text_content(),
                    "time_posted": await page.locator("div.job-details-jobs-unified-top-card__primary-description-container span").nth(2).text_content(),
                    "description": await page.locator("div.jobs-description-content__text--stretch").text_content()
                }

                scraped_jobs.append(job_data)

            except PlaywrightTimeoutError:
                print(f"⚠️ Timeout while loading job {i+1}. Skipping.")
                continue
            except Exception as e:
                print(f"⚠️ Error scraping job {i+1}: {e}")
                continue

        # Step 4: Save to Excel
        df = pd.DataFrame(scraped_jobs)
        df.to_excel("linkedin_python_jobs.xlsx", index=False)
        print(f"✅ Saved {len(scraped_jobs)} jobs to linkedin_python_jobs.xlsx")

        await browser.close()

# Run the script
asyncio.run(scrape())
