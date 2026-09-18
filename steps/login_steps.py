from behave import given, then, when

from pages.home_page import HomePage
from pages.login_page import LoginPage


def login(context):
    return LoginPage(context.page, context.scenario.name.replace(" ", "_"))


@given("que existe uma conta cadastrada")
def account_exists(context):
    context.login = login(context)
    context.login.open()


@when("o usuário informar um e-mail válido")
def valid_email(context):
    context.login.email.fill(context.account.email)


@when("informar uma senha válida")
def valid_login_password(context):
    if hasattr(context, "cadastro"):
        context.cadastro.password.fill(context.account.password)
    else:
        context.login.password.fill(context.account.password)


@when("informar uma senha inválida")
def invalid_password(context):
    context.login.password.fill("SenhaInvalida@999")


@when('clicar em "Acessar"')
def submit_login(context):
    context.login.submit.click()


@then("o usuário deverá ser autenticado com sucesso")
def authenticated(context):
    context.home = HomePage(context.page, context.scenario.name.replace(" ", "_"))
    context.home.assert_authenticated()


@then("o sistema deverá exibir uma mensagem de autenticação inválida")
def invalid_authentication(context):
    context.login.assert_authentication_error()


@then("o usuário não deverá ser autenticado")
def not_authenticated(context):
    context.login.assert_login_screen()


@given("que o usuário está autenticado")
def authenticated_user(context):
    context.login = login(context)
    context.login.open()
    context.login.login(context.account.email, context.account.password)
    context.home = HomePage(context.page, context.scenario.name.replace(" ", "_"))
    context.home.assert_authenticated()


@when("clicar na opção de logout")
def logout(context):
    context.home.logout_user()


@then("a sessão deverá ser encerrada")
def session_closed(context):
    context.login.assert_login_screen()


@then("o usuário deverá ser redirecionado para a tela de login")
def redirected_login(context):
    context.login.assert_login_screen()
