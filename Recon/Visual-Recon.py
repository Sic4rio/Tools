# Lightweight Aquatone-style visual reconnaissance tool in Python

import asyncio
from pathlib import Path
from playwright.async_api import async_playwright
from datetime import datetime

INPUT_FILE = "domains.txt"
OUTPUT_DIR = Path("aqua_output")
SCREENSHOT_DIR = OUTPUT_DIR / "screenshots"
REPORT_FILE = OUTPUT_DIR / "report.html"
CONCURRENT_TASKS = 5  # Safe concurrency limit for low-resource VMs

OUTPUT_DIR.mkdir(exist_ok=True)
SCREENSHOT_DIR.mkdir(exist_ok=True)

# Load domain list
def load_domains():
    with open(INPUT_FILE) as f:
        return [line.strip() for line in f if line.strip()]

# Screenshot a single domain
async def screenshot_domain(browser, domain, semaphore):
    url = f"http://{domain}"
    async with semaphore:
        try:
            context = await browser.new_context()
            page = await context.new_page()
            await page.goto(url, timeout=10000)
            title = await page.title()
            screenshot_path = SCREENSHOT_DIR / f"{domain.replace(':','_')}.png"
            await page.screenshot(path=screenshot_path, full_page=True)
            await context.close()
            print(f"[+] Captured {domain}")
            return {
                "domain": domain,
                "url": url,
                "screenshot": screenshot_path.name,
                "title": title
            }
        except Exception as e:
            print(f"[-] Failed {domain}: {e}")
            return {
                "domain": domain,
                "url": url,
                "screenshot": None,
                "title": "Failed"
            }

# Generate HTML report
def generate_html_report(results):
    with open(REPORT_FILE, "w") as f:
        f.write("<html><head><title>AquaLite Report</title>")
        f.write("<style>body{font-family:sans-serif;background:#111;color:#eee}img{border:1px solid #555;max-width:90%;}h2{border-bottom:1px solid #444}a{color:#6cf}</style>")
        f.write("</head><body><h1>AquaLite Report</h1>")
        f.write(f"<p>Scan Time: {datetime.now().isoformat()}</p>")

        for result in results:
            f.write(f"<h2>{result['domain']}</h2>")
            f.write(f"<p><a href='{result['url']}' target='_blank'>{result['url']}</a><br>Title: {result['title']}</p>")
            if result['screenshot']:
                f.write(f"<img src='screenshots/{result['screenshot']}'><br>")
            else:
                f.write("<p><i>Screenshot failed</i></p>")
        f.write("</body></html>")

# Main async function
async def main():
    domains = load_domains()
    semaphore = asyncio.Semaphore(CONCURRENT_TASKS)
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        tasks = [screenshot_domain(browser, d, semaphore) for d in domains]
        results = await asyncio.gather(*tasks)
        await browser.close()
        generate_html_report(results)
        print(f"[+] Report generated: {REPORT_FILE}")

if __name__ == "__main__":
    asyncio.run(main())
