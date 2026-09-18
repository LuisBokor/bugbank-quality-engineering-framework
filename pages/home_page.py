from playwright.sync_api import expect

from pages.base_page import BasePage


class HomePage(BasePage):
    def __init__(self, page, scenario_name):
        super().__init__(page, scenario_name)
        self.welcome = page.get_by_text("Olá", exact=False)
        self.balance = page.get_by_text("Saldo em conta", exact=False)
        self.logout = page.get_by_text("Sair", exact=True)
        self.home_link = page.locator("a[href='/home']")

    def go_home(self):
        if self.home_link.is_visible():
            self.home_link.click()
        else:
            self.page.goto(f"{self.URL}home", wait_until="domcontentloaded")

    def assert_authenticated(self):
        expect(self.welcome).to_be_visible()

    def assert_balance_visible(self):
        expect(self.balance).to_be_visible()

    def logout_user(self):
        self.logout.click()
