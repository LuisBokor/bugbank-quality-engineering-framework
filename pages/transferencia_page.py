from playwright.sync_api import expect

from pages.base_page import BasePage


class TransferenciaPage(BasePage):
    def __init__(self, page, scenario_name):
        super().__init__(page, scenario_name)
        self.transfer_link = page.get_by_text("TRANSFERÊNCIA", exact=True).locator("..")
        self.account_input = page.get_by_role("textbox", name="Informe o número da conta")
        self.digit_input = page.get_by_role("textbox", name="Informe o dígito da conta")
        self.value_input = page.get_by_role("textbox", name="Informe o valor da transferência")
        self.description_input = page.get_by_role("textbox", name="Informe uma descrição")
        self.transfer_button = page.get_by_role("button", name="Transferir agora")
        self.modal = page.locator("#modalText")

    def open(self):
        self.transfer_link.click()

    def transfer(self, account: str, digit: str, value: str, description: str = "Teste de transferência"):
        self.account_input.fill(account)
        self.digit_input.fill(digit)
        self.value_input.fill(value)
        self.description_input.fill(description)
        self.transfer_button.click()

    def assert_modal_contains(self, text: str):
        expect(self.modal).to_contain_text(text)
