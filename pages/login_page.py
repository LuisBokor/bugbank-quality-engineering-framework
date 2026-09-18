from playwright.sync_api import expect

from pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page, scenario_name):
        super().__init__(page, scenario_name)
        self.email = page.get_by_role("textbox", name="Informe seu e-mail").nth(0)
        self.password = page.get_by_role("textbox", name="Informe sua senha").nth(0)
        self.submit = page.get_by_role("button", name="Acessar")
        self.modal = page.locator("#modalText")

    def login(self, email: str, password: str):
        self.email.fill(email)
        self.password.fill(password)
        self.submit.click()

    def assert_authentication_error(self):
        expect(self.modal).to_be_visible()

    def assert_login_screen(self):
        expect(self.email).to_be_visible()
        expect(self.password).to_be_visible()
        expect(self.submit).to_be_visible()
