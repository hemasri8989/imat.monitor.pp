import time
import requests
from bs4 import BeautifulSoup

URL = "https://admission-imat.ilmiotest.it/choice"
TARGET_CENTERS = ["Chennai", "Delhi"]
CHECK_INTERVAL = 300  # 5 minutes
last_status = {}

def check_slots():
    global last_status
    try:
        response = requests.get(URL, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        page_text = soup.get_text().lower()

        for city in TARGET_CENTERS:
            city_lower = city.lower()
            if city_lower in page_text:
                if "red" in page_text:
                    status = "FULL (RED)"
                elif "yellow" in page_text:
                    status = "LIMITED (YELLOW)"
                elif "green" in page_text:
                    status = "AVAILABLE (GREEN)"
                else:
                    status = "UNKNOWN"
            else:
                status = "NOT FOUND"

            if last_status.get(city) != status:
                print(f"[UPDATE] {city}: {status}")
                last_status[city] = status

    except Exception as e:
        print(f"Error checking slots: {e}")

if __name__ == "__main__":
    print("🚀 IMAT Slot Monitor started...")
    while True:
        check_slots()
        time.sleep(CHECK_INTERVAL)
