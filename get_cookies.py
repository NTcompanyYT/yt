import os
import time
from playwright.sync_api import sync_playwright

def main():
    username = os.environ["YT_USERNAME"]
    password = os.environ["YT_PASSWORD"]

    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        # رفتن به صفحه ورود گوگل
        page.goto("https://accounts.google.com/signin/v2/identifier?service=youtube")
        page.fill('input[type="email"]', username)
        page.click('#identifierNext')

        page.wait_for_selector('input[type="password"]', timeout=10000)
        page.fill('input[type="password"]', password)
        page.click('#passwordNext')

        # منتظر بمانیم تا ورود کامل شود (مثلاً با ظاهر شدن یک عنصر خاص)
        try:
            page.wait_for_selector('ytd-app', timeout=15000)  # نشانه ورود موفق
        except:
            # ممکن است چالش تایید دو مرحله‌ای ظاهر شود - اگر تنظیمات App Password درست باشد نباید بیاید
            pass

        # استخراج همه کوکی‌ها در فرمت Netscape
        cookies = context.cookies()
        with open("cookies.txt", "w") as f:
            f.write("# Netscape HTTP Cookie File\n")
            for c in cookies:
                domain = c.get("domain", "")
                flag = "TRUE" if domain.startswith(".") else "FALSE"
                path = c.get("path", "/")
                secure = "TRUE" if c.get("secure") else "FALSE"
                expiry = str(int(c.get("expires", 0))) if c.get("expires") else "0"
                name = c.get("name", "")
                value = c.get("value", "")
                f.write(f"{domain}\t{flag}\t{path}\t{secure}\t{expiry}\t{name}\t{value}\n")

        browser.close()

if __name__ == "__main__":
    main()
