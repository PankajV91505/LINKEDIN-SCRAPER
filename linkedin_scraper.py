# linkedin_scraper.py
import asyncio
import json
import time
import pandas as pd
from playwright.async_api import async_playwright


# Simulate human scrolling
async def human_scroll(page, duration=5):
    start = time.time()
    while time.time() - start < duration:
        await page.mouse.wheel(0, 500)
        await asyncio.sleep(1)
        

# Extract job details from the job detail panel
async def extract_job_details(page):
    job_data = {}
    try:
        job_data["title"] = await page.locator("h1.t-24").text_content() or ""
        job_data["company"] = await page.locator("div.job-details-jobs-unified-top-card__company-name a").text_content() or ""
        job_data["location"] = await page.locator("div.job-details-jobs-unified-top-card__primary-description-container span").nth(0).text_content() or ""
        job_data["time_posted"] = await page.locator("div.job-details-jobs-unified-top-card__primary-description-container span").nth(2).text_content() or ""
        job_data["description"] = await page.locator("div.jobs-description-content__text--stretch").text_content() or ""
    except Exception as e:
        print("⚠️ Error extracting fields:", e)
    return job_data


# Main scraping logic
async def scrape():
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=False, slow_mo=100)
        context = await browser.new_context()


        # Load cookies for auto-login
        with open("cookies.json", "r") as f:
            cookies = json.load(f)["cookies"]
        await context.add_cookies(cookies)

        page = await context.new_page()
        

        # Go to LinkedIn and ensure logged in
        await page.goto("https://www.linkedin.com/feed/", wait_until="domcontentloaded")
        print("✅ Logged in using saved cookies.")

        # Navigate to job search page
        await page.goto("https://www.linkedin.com/jobs/search/?keywords=python%20developer")
        await asyncio.sleep(5)

        scraped_jobs = []

        while len(scraped_jobs) < 70:
            await human_scroll(page, duration=5)

            await page.wait_for_selector(".job-card-container--clickable", timeout=15000)
            job_cards = await page.locator(".job-card-container--clickable").all()
            print(f"🟡 Found {len(job_cards)} job cards on current page")

            for job in job_cards:
                if len(scraped_jobs) >= 70:
                    break

                try:
                    await job.scroll_into_view_if_needed()
                    await job.click()
                    await asyncio.sleep(4)
                    job_data = await extract_job_details(page)
                    scraped_jobs.append(job_data)
                    print(f"✅ Scraped {len(scraped_jobs)} jobs")
                except Exception as e:
                    print("⚠️ Job click/scrape error:", e)
                    continue

            # Check if Next button exists and is enabled
            next_button = page.locator("button.jobs-search-pagination__button--next")
            if await next_button.is_enabled():
                print("➡️ Going to next page...")
                await next_button.click()
                await asyncio.sleep(5)
            else:
                print("❌ No more pages or next button disabled.")
                break

        # Save to Excel
        df = pd.DataFrame(scraped_jobs)
        df.to_excel("linkedin_python_jobs.xlsx", index=False)
        print("✅ Scraped data saved to linkedin_python_jobs.xlsx")

        await browser.close()

# Run the script
asyncio.run(scrape())
