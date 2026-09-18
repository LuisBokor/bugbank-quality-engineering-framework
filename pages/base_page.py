from playwright.sync_api import Page

from utils.logger import get_logger
from utils.screenshot_manager import ScreenshotManager

DEFAULT_TIMEOUT_MS = 10_000


class BasePage:
    URL = "https://bugbank.netlify.app/"

    def __init__(self, page: Page, scenario_name: str):
        self.page = page
        self.page.set_default_timeout(DEFAULT_TIMEOUT_MS)
        self.logger = get_logger(scenario_name)
        self.screenshots = ScreenshotManager(page, scenario_name)

    def open(self):
        self.logger.info("Abrindo %s", self.URL)
        self.page.goto(self.URL, wait_until="domcontentloaded")

    def capture(self, name: str):
        self.screenshots.capture(name)
