from pathlib import Path


class ScreenshotManager:
    def __init__(self, page, scenario_name: str):
        self.page = page
        self.directory = Path(__file__).resolve().parents[1] / "evidencias" / scenario_name
        self.directory.mkdir(parents=True, exist_ok=True)

    def capture(self, name: str):
        self.page.screenshot(path=str(self.directory / f"{name}.png"), full_page=True)
