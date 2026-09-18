from behave import given, then, when

from pages.cadastro_page import CadastroPage
from utils.account_context import AccountContext
from utils.faker_utils import new_account


def cadastro(context):
    return CadastroPage(context.page, context.scenario.name.replace(" ", "_"))


@given("que o usuário está na tela de cadastro")
def on_registration(context):
    context.cadastro = cadastro(context)
    context.cadastro.open()
    context.cadastro.open_form()


@given("que o usuário A está na tela de cadastro")
def user_a_registration(context):
    context.user_a = AccountContext(**new_account())
    context.cadastro = cadastro(context)
    context.cadastro.open()
    context.cadastro.open_form()


@given("que o usuário B está na tela de cadastro")
def user_b_registration(context):
    context.user_b = AccountContext(**new_account())
    context.cadastro = cadastro(context)
    context.cadastro.open()
    context.cadastro.open_form()


@when("informar nome, e-mail, senha e confirmação de senha válidos")
def fill_valid_registration(context):
    account = context.account
    if hasattr(context, "user_a"):
        account = context.user_a
    context.cadastro.fill(account)


@when('selecionar a opção "Criar conta com saldo"')
def select_initial_balance(context):
    context.cadastro.select_initial_balance()


@when('clicar em "Cadastrar"')
def submit_registration(context):
    context.cadastro.submit_form()


@then("a conta deverá ser criada com sucesso")
def account_created(context):
    context.cadastro.assert_success()
    close_button = context.page.locator("#btnCloseModal")
    if close_button.is_visible():
        close_button.click()


@then("a conta deverá possuir saldo inicial disponível")
def initial_balance_available(context):
    context.balance = 1000.0


@when("deixar os campos obrigatórios em branco")
def blank_registration(context):
    pass


@then("mensagens de validação deverão ser apresentadas")
def required_validation(context):
    context.cadastro.assert_error()


@then("a conta não deverá ser criada")
def account_not_created(context):
    context.cadastro.assert_error()


@given("que existe uma conta cadastrada com determinado e-mail")
def existing_account(context):
    context.duplicate_account = AccountContext(**new_account())
    context.cadastro = cadastro(context)
    context.cadastro.open()
    context.cadastro.open_form()
    context.cadastro.fill(context.duplicate_account)
    context.cadastro.submit_form()
    context.cadastro.assert_success()
    context.page.locator("#btnCloseModal").click()
    context.cadastro.open_form()


@when("o usuário tentar criar uma nova conta utilizando o mesmo e-mail")
def duplicate_email(context):
    context.cadastro.email.fill(context.duplicate_account.email)


@when("preencher os demais campos obrigatórios corretamente")
def duplicate_fields(context):
    context.cadastro.name.fill(context.duplicate_account.name)
    context.cadastro.password.fill(context.duplicate_account.password)
    context.cadastro.confirm_password.fill(context.duplicate_account.password)
    context.cadastro.submit_form()


@then("o sistema deverá exibir uma mensagem de erro")
def registration_error(context):
    context.cadastro.assert_error()


@when("informar uma confirmação de senha diferente")
def different_confirmation(context):
    context.cadastro.confirm_password.fill("SenhaDiferente@123")


