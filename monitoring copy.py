import time
import requests
from playwright.sync_api import sync_playwright

TELEGRAM_API_TOKEN = "7593461624:AAEq4FwPqk8wVOnWlQi4wnotXJWaStxxNlg"
TELEGRAM_CHAT_ID = "1759196449"

def send_telegram_message(message):
    """Send a message to the specified Telegram chat."""
    url = f"https://api.telegram.org/bot{TELEGRAM_API_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("Notification sent to Telegram.")
        else:
            print(f"Failed to send notification. Response: {response.text}")
    except Exception as e:
        print(f"Error while sending Telegram message: {e}")

def check_survey_availability(page):
    """Check if a survey is available on the dashboard."""
    dashboard_selector = "div.PageContentWrapper_root__d34ec.PageContentWrapper_spaced__1n06I.PageContentWrapper_normal__r_GSc"
    try:
        is_present = page.locator(dashboard_selector).is_visible(timeout=5000)
        if is_present:
            print("No survey is available.")
        else:
            print("Survey is available.")
            send_telegram_message("Survey is now available on LifePoints!")
    except Exception:
        print("Selector not found, assuming survey is available.")
        send_telegram_message("Survey is now available on LifePoints!")

def monitor_surveys():
    """Monitor survey availability continuously."""
    with sync_playwright() as p:
        # Launch the browser with persistent context to keep the session active
        browser = p.chromium.launch_persistent_context(
            user_data_dir="browser_data",  # Directory to store session data
            headless=False  # Set to True for headless mode
        )
        page = browser.new_page()

        try:
            # Navigate to the LifePoints login page
            page.goto("https://app.lifepointspanel.com/en-US/dashboard")
            print("Navigated to the LifePoints login page.")

            # Log in only if not already logged in
            if page.locator("input[name='username']").is_visible():
                page.fill("input[name='username']", "vasnthwork1@gmail.com")
                page.fill("input[name='password']", "Vasanth@lifepoints")
                page.click("button[type='submit']")
                print("Login form submitted.")
                page.wait_for_load_state("networkidle")
                print("Login completed and website loaded.")

            # Navigate to the dashboard
            page.goto("https://app.lifepointspanel.com/en-IN/dashboard")
            page.wait_for_load_state("networkidle")
            print("Navigated to the dashboard.")

            # Monitor continuously
            print("Starting 24/7 monitoring...")
            while True:
                check_survey_availability(page)
                print("Checked survey availability. Waiting 10 minutes before next check...")
                time.sleep(120)  # Wait for 10 minutes (600 seconds)

        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            # Close the browser
            browser.close()
            print("Browser closed.")

if __name__ == "__main__":
    monitor_surveys()
