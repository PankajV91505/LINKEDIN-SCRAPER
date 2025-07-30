# save_cookies.py
import asyncio
import json
from playwright.async_api import async_playwright

async def save_cookies():
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("https://www.linkedin.com/login")
        print("🔐 Login manually with Google or credentials (you have 60 sec)...")
        await asyncio.sleep(60)

        cookies = await context.cookies()
        with open("cookies.json", "w") as f:
            json.dump({"cookies": cookies}, f)

        print("✅ Cookies saved.")
        await browser.close()

asyncio.run(save_cookies())
