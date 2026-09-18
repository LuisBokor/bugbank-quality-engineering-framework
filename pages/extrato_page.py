from playwright.sync_api import expect

from pages.base_page import BasePage


class ExtratoPage(BasePage):
    def __init__(self, page, scenario_name):
        super().__init__(page, scenario_name)
        self.statement_link = page.get_by_text("EXTRATO", exact=True).locator("..")
        self.transactions = page.locator("body")

    def open(self):
        self.statement_link.click()

    def assert_transfer_visible(self):
        expect(self.transactions).to_contain_text("Transfer")
