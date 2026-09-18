from playwright.sync_api import expect

from pages.base_page import BasePage
from utils.account_context import AccountContext


class CadastroPage(BasePage):
    def __init__(self, page, scenario_name):
        super().__init__(page, scenario_name)
        self.register_button = page.get_by_role("button", name="Registrar")
        self.email = page.get_by_role("textbox", name="Informe seu e-mail").nth(1)
        self.name = page.get_by_role("textbox", name="Informe seu Nome")
        self.password = page.get_by_role("textbox", name="Informe sua senha").nth(1)
        self.confirm_password = page.get_by_role("textbox", name="Informe a confirmação da senha")
        self.initial_balance = page.get_by_text("Criar conta com saldo")
        self.submit = page.get_by_role("button", name="Cadastrar")
        self.modal = page.locator("#modalText")

    def open_form(self):
        self.register_button.click()
        expect(self.name).to_be_visible()

    def fill(self, account: AccountContext, confirmation: str | None = None):
        self.name.fill(account.name)
        self.email.fill(account.email)
        self.password.fill(account.password)
        self.confirm_password.fill(confirmation or account.password)

    def select_initial_balance(self):
        label = self.page.get_by_text("Criar conta com saldo", exact=False)
        toggle = label.locator("xpath=following-sibling::*[1]")
        toggle.click()

    def submit_form(self):
        self.submit.click()

    def assert_success(self):
        expect(self.modal).to_contain_text("criada com sucesso")

    def assert_error(self, text: str | None = None):
        validation_text = self.page.get_by_text("É campo obrigatório", exact=False)
        password_error = self.page.get_by_text("As senhas não são iguais.", exact=False)
        if self.modal.is_visible():
            if text:
                expect(self.modal).to_contain_text(text)
            return
        expect(validation_text.or_(password_error).first).to_be_visible()
