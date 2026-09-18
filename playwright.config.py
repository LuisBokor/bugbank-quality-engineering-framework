import os


HEADLESS = os.getenv("HEADLESS", "0") == "1"
BROWSER_CHANNEL = os.getenv("BROWSER_CHANNEL", "msedge")
BASE_URL = "https://bugbank.netlify.app/"
DEFAULT_TIMEOUT_MS = 10_000
VIEWPORT = {"width": 1440, "height": 900}
