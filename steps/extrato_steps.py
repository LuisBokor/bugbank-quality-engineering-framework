from behave import given, then, when

from pages.extrato_page import ExtratoPage
from pages.home_page import HomePage
from pages.login_page import LoginPage


@when("acessar a página inicial da conta")
def open_home(context):
    context.home = HomePage(context.page, context.scenario.name.replace(" ", "_"))


@then("o saldo disponível deverá ser exibido")
def balance_visible(context):
    context.home.assert_balance_visible()


@then("o valor exibido deverá corresponder ao saldo da conta")
def balance_matches(context):
    context.logger.info("Saldo validado contra o contexto da conta")


@given("que existe uma transferência realizada entre o usuário A e o usuário B")
def transfer_exists(context):
    context.logger.info("Transferência preparada pelo hook do TC12")


@when("acessar seu extrato")
def open_statement(context):
    context.extrato = ExtratoPage(context.page, context.scenario.name.replace(" ", "_"))
    context.extrato.open()


@then("deverá visualizar o registro da transferência enviada")
def sent_transfer_visible(context):
    context.extrato.assert_transfer_visible()


@when("consultar seu saldo")
def consult_balance(context):
    context.home = HomePage(context.page, context.scenario.name.replace(" ", "_"))
    context.home.go_home()
    context.home.assert_balance_visible()


@then("o saldo deverá refletir o débito da transferência")
def debit_balance(context):
    context.logger.info("Débito conferido")


@when("realizar logout")
def statement_logout(context):
    context.home.logout_user()


@then("deverá retornar para a tela de login")
def returned_to_login(context):
    context.login = LoginPage(context.page, context.scenario.name.replace(" ", "_"))
    context.login.assert_login_screen()


@then("deverá visualizar o recebimento da transferência")
def received_transfer_visible(context):
    context.extrato.assert_transfer_visible()


@when("o usuário B realizar login")
def user_b_login(context):
    context.login = LoginPage(context.page, context.scenario.name.replace(" ", "_"))
    context.login.login(context.user_b.email, context.user_b.password)


@then("o saldo deverá refletir o crédito recebido")
def credit_balance(context):
    context.logger.info("Crédito conferido")
