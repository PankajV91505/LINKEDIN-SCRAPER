# 🕵️‍♂️ LinkedIn Job Scraper using Playwright (Python)

This project scrapes job postings from [LinkedIn Jobs](https://www.linkedin.com/jobs/) for specific keywords using **Playwright** and **Python**. It mimics human behavior like scrolling and pagination, and saves job listings (title, company, location, etc.) into an Excel file.

---

## 🚀 Features

- ✅ Auto-login using saved LinkedIn cookies
- 🧠 Human-like scrolling and delays
- 📄 Extracts job title, company name, location, time posted, and full description
- 🔄 Automatically clicks through "Next" pages until 70+ jobs are scraped
- 💾 Exports data to `linkedin_python_jobs.xlsx`
- 🛑 Safe delays and click patterns to reduce detection risk

---

## 📦 Technologies Used

- Python 3.10+
- Playwright
- Pandas + OpenPyXL
- Asyncio

---

## 📁 Project Structure

```
linkedin-job-scraper/
│
├── linkedin_scraper.py          # Main scraper logic
├── cookies.json                 # Saved cookies from manual login
├── linkedin_python_jobs.xlsx    # Output file (auto-generated)
├── requirements.txt             # Python dependencies
└── README.md                    # Project guide
```

---

## ⚙️ Installation & Setup

1. **Clone the repo**:

```bash
git clone https://github.com/your-username/linkedin-job-scraper.git

cd linkedin-job-scraper
```

2. **Install dependencies**:

```bash
pip install -r requirements.txt
```

3. **Example requirements.txt**:

```plaintext
et_xmlfile==2.0.0
greenlet==3.2.3
numpy==2.3.2
openpyxl==3.1.5
pandas==2.3.1
playwright==1.54.0
pyee==13.0.0
python-dateutil==2.9.0.post0
pytz==2025.2
six==1.17.0
typing_extensions==4.14.1
tzdata==2025.2
```
4. **Install Playwright Browsers**:
Install Playwright Browsers:

```bash
playwright install
```
5. **Run the Scraper**:

   - First, manually log in to LinkedIn and save your cookies:
     - Open `cookies.json` in a text editor and paste your cookies after logging in.
     - Make sure the cookies are valid and not expired.
```bash

python save_cookies.py
```

   - Now run the scraper:
```bash
python linkedin_scraper.py
```

```

✅ The scraper will:

    Use saved cookies to log in

    Search for "Python Developer" jobs

    Scroll and extract job details

    Click "Next" until 70 jobs collected

    Save them to linkedin_python_jobs.xlsx

✏️ Customization Options

    Change Job Title: modify the LinkedIn search URL in linkedin_scraper.py

    Country or Remote Filters: add filters in the search URL

    Change Job Limit: update while len(scraped_jobs) < 70

⚠️ Disclaimer

This scraper is for educational purposes only. Scraping LinkedIn may violate their Terms of Service. Use it responsibly and at your own risk.
📬 Contact

Made by @Pankaj Verma
```
