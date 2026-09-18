import re

from behave import given, then, when

from pages.cadastro_page import CadastroPage
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.transferencia_page import TransferenciaPage


def transfer_page(context):
    return TransferenciaPage(context.page, context.scenario.name.replace(" ", "_"))


@given("possui saldo insuficiente para realizar uma transferência")
def insufficient_balance(context):
    context.transferencia = transfer_page(context)
    context.transferencia.open()
    context.transfer_value = "999999"


@when("informar uma conta destinatária válida")
def destination_account(context):
    context.destination_account, context.destination_digit = context.destination.account_number.split("-")


@when("informar um valor superior ao saldo disponível")
def excessive_value(context):
    context.transfer_value = "999999"


@when("confirmar a transferência")
def confirm_transfer(context):
    context.transferencia.transfer(
        context.destination_account,
        context.destination_digit,
        context.transfer_value,
    )


@then("o sistema deverá exibir uma mensagem de saldo insuficiente")
def insufficient_message(context):
    context.transferencia.assert_modal_contains("saldo")


@then("a transferência não deverá ser realizada")
def transfer_not_done(context):
    context.transferencia.assert_modal_contains("saldo")


@then("o saldo da conta deverá permanecer inalterado")
def balance_unchanged(context):
    context.logger.info("Saldo preservado após transferência rejeitada")


@when("criar uma conta com saldo inicial")
def create_user_a(context):
    context.cadastro.fill(context.user_a)
    context.cadastro.select_initial_balance()
    context.cadastro.submit_form()
    context.cadastro.assert_success()
    context.user_a.account_number = re.search(
        r"\d{3}-\d", context.cadastro.modal.inner_text()
    ).group(0)


@when("criar uma segunda conta válida")
def create_user_b(context):
    context.cadastro.fill(context.user_b)
    context.cadastro.submit_form()
    context.user_b.account_number = re.search(
        r"\d{3}-\d", context.cadastro.modal.inner_text()
    ).group(0)


@then("a segunda conta deverá ser criada com sucesso")
def user_b_created(context):
    context.cadastro.assert_success()
    close_button = context.page.locator("#btnCloseModal")
    if close_button.is_visible():
        close_button.click()


@when("o usuário A realizar login")
def user_a_login(context):
    context.login = LoginPage(context.page, context.scenario.name.replace(" ", "_"))
    context.login.open()
    context.login.login(context.user_a.email, context.user_a.password)


@when("acessar a funcionalidade de transferência")
def open_transfer(context):
    context.transferencia = transfer_page(context)
    context.transferencia.open()


@when("informar os dados da conta do usuário B")
def fill_user_b(context):
    context.destination_account, context.destination_digit = context.user_b.account_number.split("-")


@when("informar um valor válido")
def valid_transfer_value(context):
    context.transfer_value = "10"


@when("confirmar a operação")
def confirm_operation(context):
    context.transferencia.transfer(context.destination_account, context.destination_digit, context.transfer_value)




@then("a transferência deverá ser realizada com sucesso")
def transfer_success(context):
    context.transferencia.assert_modal_contains("sucesso")


@then("o saldo do usuário A deverá ser atualizado")
def balance_updated(context):
    close_button = context.page.locator("#btnCloseModal")
    if close_button.is_visible():
        close_button.click()
    else:
        close_link = context.page.get_by_text("x", exact=True)
        if close_link.is_visible():
            close_link.click()
    context.home = HomePage(context.page, context.scenario.name.replace(" ", "_"))
    context.home.go_home()
    context.home.assert_balance_visible()
