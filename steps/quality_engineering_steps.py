import re

from behave import given, then, when
from playwright.sync_api import expect

from pages.extrato_page import ExtratoPage
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.transferencia_page import TransferenciaPage

TRANSFER_VALUE = "10"
TRANSFER_DESCRIPTION = "QE-04 Data Persistence"


def _scenario_name(context):
    return context.scenario.name.replace(" ", "_")


def _parse_brl(value: str) -> float:
    return float(value.replace(".", "").replace(",", "."))


def _read_balance(context) -> float:
    context.home = HomePage(context.page, _scenario_name(context))
    context.home.go_home()
    context.home.assert_balance_visible()
    text = context.page.locator("body").inner_text()
    match = re.search(r"Saldo em conta\s*R\$\s*(-?[\d.]+,\d{2})", text)
    assert match, f"[DEFEITO QE] Saldo não localizado na página inicial. Conteúdo: {text[:500]}"
    return _parse_brl(match.group(1))


def _statement_snapshot(context) -> str:
    context.extrato = ExtratoPage(context.page, _scenario_name(context))
    context.extrato.open()
    context.extrato.assert_transfer_visible()
    return context.page.locator("body").inner_text()


def _assert_protected_blocked(context, checkpoint: str):
    context.home = HomePage(context.page, _scenario_name(context))
    context.login = LoginPage(context.page, _scenario_name(context))
    defects = []
    try:
        expect(context.home.welcome).not_to_be_visible()
        expect(context.home.balance).not_to_be_visible()
    except AssertionError:
        defects.append("conteúdo da conta (boas-vindas/saldo) visível sem sessão válida")
    try:
        context.login.assert_login_screen()
    except AssertionError:
        defects.append("formulário de login não exibido após encerramento da sessão")
    if defects:
        context.home.capture(f"defeito_{checkpoint}")
        raise AssertionError(
            f"[DEFEITO QE-02] Área protegida acessível ({checkpoint}): "
            f"{'; '.join(defects)}. URL atual: {context.page.url}"
        )
    context.home.capture(f"checkpoint_{checkpoint}")
    context.logger.info(
        "Checkpoint %s: acesso bloqueado. URL atual: %s", checkpoint, context.page.url
    )


# ---------------------------------------------------------------------------
# TC_13 - Financial Reconciliation Assessment
# ---------------------------------------------------------------------------

QE13_DESC_A_B = "QE-01 A para B"
QE13_DESC_B_C = "QE-01 B para C"


def _qe_login(context, account, label: str):
    context.login = LoginPage(context.page, _scenario_name(context))
    context.login.open()
    context.login.login(account.email, account.password)
    context.home = HomePage(context.page, _scenario_name(context))
    context.home.assert_authenticated()
    balance = _read_balance(context)
    context.home.capture(f"{label}_saldo")
    context.logger.info("%s (%s): saldo %.2f", label, account.account_number, balance)
    return balance


def _qe_statement(context, label: str) -> str:
    snapshot = _statement_snapshot(context)
    context.extrato.capture(f"{label}_extrato")
    context.logger.info("%s: extrato capturado (%d chars)", label, len(snapshot))
    return snapshot


def _qe_logout(context):
    context.home = HomePage(context.page, _scenario_name(context))
    context.home.logout_user()
    context.login = LoginPage(context.page, _scenario_name(context))
    context.login.assert_login_screen()


def _qe_transfer(context, source, target, value: str, description: str, label: str):
    context.transferencia = TransferenciaPage(context.page, _scenario_name(context))
    context.transferencia.open()
    account, digit = target.account_number.split("-")
    context.transferencia.transfer(account, digit, value, description)
    context.transferencia.assert_modal_contains("sucesso")
    context.transferencia.capture(f"{label}_sucesso")
    close_button = context.page.locator("#btnCloseModal")
    if close_button.is_visible():
        close_button.click()
    context.logger.info(
        "%s: transferência de %s de %s para %s",
        label, value, source.account_number, target.account_number,
    )


def _qe_financial_defect(context, label: str, message: str, snapshot: str = ""):
    if getattr(context, "home", None):
        context.home.capture(f"defeito_{label}")
    context.logger.error(
        "[DEFEITO QE-01] %s | %s | Extrato: %s",
        label, message, snapshot[:500],
    )
    raise AssertionError(f"[DEFEITO QE-01] {label}: {message}")


def _qe_assert_single_entry(snapshot: str, description: str, value_label: str, kind: str, label: str, context):
    count = snapshot.count(description)
    if count != 1:
        _qe_financial_defect(
            context, label,
            f"{kind} de {value_label} deveria aparecer 1 vez no extrato, "
            f"apareceu {count} (lançamento ausente ou duplicado)",
            snapshot,
        )
    if value_label not in snapshot:
        _qe_financial_defect(
            context, label,
            f"valor {value_label} do {kind.lower()} ausente no extrato",
            snapshot,
        )


@given("que a conta A está autenticada com saldo inicial")
def qe_account_a_authenticated(context):
    context.qe_initial_a = _qe_login(context, context.qe_account_a, "conta_A_inicial")
    assert context.qe_initial_a >= 300, (
        f"[DEFEITO QE] Conta A sem saldo suficiente para o cenário: {context.qe_initial_a:.2f}"
    )


@given("a conta B possui saldo inicial")
def qe_account_b_initial(context):
    context.qe_initial_b = _qe_login(context, context.qe_account_b, "conta_B_inicial")
    _qe_logout(context)
    _qe_login(context, context.qe_account_a, "conta_A_retorno")


@given("a conta C não possui saldo inicial")
def qe_account_c_initial(context):
    context.qe_initial_c = _qe_login(context, context.qe_account_c, "conta_C_inicial")
    _qe_logout(context)
    _qe_login(context, context.qe_account_a, "conta_A_retorno")


@when("a conta A transferir 300 reais para a conta B")
def qe_transfer_a_to_b(context):
    _qe_transfer(context, context.qe_account_a, context.qe_account_b, "300", QE13_DESC_A_B, "transfer_AB")


@then("a transferência da conta A deverá ser concluída com sucesso")
def qe_transfer_a_done(context):
    context.logger.info("Transferência A->B confirmada pelo modal de sucesso")


@when("a conta B transferir 100 reais para a conta C")
def qe_transfer_b_to_c(context):
    _qe_logout(context)
    _qe_login(context, context.qe_account_b, "conta_B_pre_transferencia")
    _qe_transfer(context, context.qe_account_b, context.qe_account_c, "100", QE13_DESC_B_C, "transfer_BC")


@then("a transferência da conta B deverá ser concluída com sucesso")
def qe_transfer_b_done(context):
    context.logger.info("Transferência B->C confirmada pelo modal de sucesso")
    _qe_logout(context)


@then("o saldo final da conta A deverá ser o inicial menos 300")
def qe_final_balance_a(context):
    context.qe_final_a = _qe_login(context, context.qe_account_a, "conta_A_final")
    expected = context.qe_initial_a - 300.0
    if context.qe_final_a != expected:
        _qe_financial_defect(
            context, "saldo_conta_A",
            f"saldo final incorreto: inicial {context.qe_initial_a:.2f} - 300 = "
            f"{expected:.2f}, exibido {context.qe_final_a:.2f}",
        )


@then("o extrato da conta A deverá conter um único débito de 300")
def qe_statement_a(context):
    context.qe_statement_a = _qe_statement(context, "conta_A")
    _qe_assert_single_entry(
        context.qe_statement_a, QE13_DESC_A_B, "300,00", "Débito", "extrato_conta_A", context,
    )
    _qe_logout(context)


@then("o saldo final da conta B deverá ser o inicial mais 300 menos 100")
def qe_final_balance_b(context):
    context.qe_final_b = _qe_login(context, context.qe_account_b, "conta_B_final")
    expected = context.qe_initial_b + 300.0 - 100.0
    if context.qe_final_b != expected:
        _qe_financial_defect(
            context, "saldo_conta_B",
            f"saldo final incorreto: inicial {context.qe_initial_b:.2f} + 300 - 100 = "
            f"{expected:.2f}, exibido {context.qe_final_b:.2f}",
        )


@then("o extrato da conta B deverá conter exatamente um crédito de 300 e um débito de 100")
def qe_statement_b(context):
    context.qe_statement_b = _qe_statement(context, "conta_B")
    _qe_assert_single_entry(
        context.qe_statement_b, QE13_DESC_A_B, "300,00", "Crédito", "extrato_conta_B_credito", context,
    )
    _qe_assert_single_entry(
        context.qe_statement_b, QE13_DESC_B_C, "100,00", "Débito", "extrato_conta_B_debito", context,
    )
    _qe_logout(context)


@then("o saldo final da conta C deverá ser 100")
def qe_final_balance_c(context):
    context.qe_final_c = _qe_login(context, context.qe_account_c, "conta_C_final")
    expected = context.qe_initial_c + 100.0
    if context.qe_final_c != expected:
        _qe_financial_defect(
            context, "saldo_conta_C",
            f"saldo final incorreto: inicial {context.qe_initial_c:.2f} + 100 = "
            f"{expected:.2f}, exibido {context.qe_final_c:.2f}",
        )


@then("o extrato da conta C deverá conter um único crédito de 100")
def qe_statement_c(context):
    context.qe_statement_c = _qe_statement(context, "conta_C")
    _qe_assert_single_entry(
        context.qe_statement_c, QE13_DESC_B_C, "100,00", "Crédito", "extrato_conta_C", context,
    )


@then("o total financeiro do sistema deverá estar reconciliado")
def qe_global_reconciliation(context):
    initial_total = context.qe_initial_a + context.qe_initial_b + context.qe_initial_c
    final_total = context.qe_final_a + context.qe_final_b + context.qe_final_c
    context.logger.info(
        "Reconciliação QE-01: A %.2f->%.2f | B %.2f->%.2f | C %.2f->%.2f | "
        "Total %.2f -> %.2f",
        context.qe_initial_a, context.qe_final_a,
        context.qe_initial_b, context.qe_final_b,
        context.qe_initial_c, context.qe_final_c,
        initial_total, final_total,
    )
    if initial_total != final_total:
        _qe_financial_defect(
            context, "reconciliacao_global",
            f"reconciliação falhou: total inicial {initial_total:.2f} != "
            f"total final {final_total:.2f} (divergência de "
            f"{final_total - initial_total:.2f})",
            context.qe_statement_a + context.qe_statement_b + context.qe_statement_c,
        )


# ---------------------------------------------------------------------------
# TC_14 - Session Integrity Assessment
# ---------------------------------------------------------------------------

@when("pressionar o botão voltar do navegador")
def browser_back(context):
    context._checkpoint = "navegacao_retorno"
    context.page.go_back(wait_until="domcontentloaded")
    context.logger.info("Navegação de retorno do navegador executada")


@then("o acesso à área protegida deverá ser bloqueado")
def protected_blocked(context):
    _assert_protected_blocked(context, getattr(context, "_checkpoint", None) or "checkpoint_generico")
    context._checkpoint = None


@when("atualizar a página")
def page_refresh(context):
    context._checkpoint = "refresh"
    context.page.reload(wait_until="domcontentloaded")
    context.logger.info("Página atualizada após logout")


@then("o acesso à área protegida deverá permanecer bloqueado")
def protected_still_blocked(context):
    _assert_protected_blocked(context, "refresh")
    context._checkpoint = None


@when("tentar acessar diretamente a URL da área logada")
def direct_url_access(context):
    context._checkpoint = "url_direta"
    context.page.goto(f"{HomePage.URL}home", wait_until="domcontentloaded")
    context.logger.info("Tentativa de acesso direto à URL protegida")


@then("a sessão deverá permanecer encerrada")
def session_remains_closed(context):
    _assert_protected_blocked(context, "sessao_final")
    context._checkpoint = None


# ---------------------------------------------------------------------------
# TC_15 - Concurrent Transaction Assessment
# ---------------------------------------------------------------------------

QE15_VALUE = "50"
QE15_DESCRIPTION = "QE-03 Concorrencia"
QE15_ATTEMPTS = 5


def _qe15_snapshot_balance(context) -> float:
    context.home = HomePage(context.page, _scenario_name(context))
    context.home.go_home()
    text = context.page.locator("body").inner_text()
    match = re.search(r"Saldo em conta\s*R\$\s*(-?[\d.]+,\d{2})", text)
    if not match:
        _qe_financial_defect(
            context, "saldo_ausente",
            "saldo não localizado na página inicial durante avaliação de concorrência",
            text,
        )
    return _parse_brl(match.group(1))


@given("que o usuário remetente está autenticado com saldo inicial suficiente")
def qe15_sender_authenticated(context):
    context.qe15_initial_sender = _qe_login(context, context.qe_sender, "remetente_inicial")
    minimum = _parse_brl(f"{QE15_VALUE},00")
    if context.qe15_initial_sender < minimum:
        _qe_financial_defect(
            context, "remetente_sem_saldo",
            f"saldo inicial do remetente insuficiente para o cenário: "
            f"{context.qe15_initial_sender:.2f} < {minimum:.2f}",
        )


@given("existe uma conta receptora válida")
def qe15_receiver_exists(context):
    if not context.qe_receiver.account_number:
        _qe_financial_defect(
            context, "receptor_invalido",
            "conta receptora não foi criada no hook de preparação",
        )
    context.logger.info("Conta receptora: %s", context.qe_receiver.account_number)


@when("preencher uma transferência válida de 50 reais")
def qe15_fill_transfer(context):
    context.transferencia = TransferenciaPage(context.page, _scenario_name(context))
    context.transferencia.open()
    account, digit = context.qe_receiver.account_number.split("-")
    context.transferencia.account_input.fill(account)
    context.transferencia.digit_input.fill(digit)
    context.transferencia.value_input.fill(QE15_VALUE)
    context.transferencia.description_input.fill(QE15_DESCRIPTION)
    context.transferencia.capture("formulario_preenchido")
    context.logger.info(
        "Formulário preenchido: %s -> %s, valor %s",
        context.qe_sender.account_number, context.qe_receiver.account_number, QE15_VALUE,
    )


@when("acionar a confirmação da transferência 5 vezes em rápida sucessão")
def qe15_rapid_confirmations(context):
    button = context.transferencia.transfer_button
    outcomes = []
    for attempt in range(1, QE15_ATTEMPTS + 1):
        try:
            button.click(timeout=1_500, no_wait_after=True)
            outcome = "clique real"
        except Exception as click_error:
            try:
                button.dispatch_event("click")
                outcome = "clique despachado via DOM (overlay interceptou o ponteiro)"
            except Exception as dispatch_error:
                outcome = f"tentativa bloqueada: {type(dispatch_error).__name__}"
                context.transferencia.capture(f"tentativa_{attempt}_bloqueada")
                context.logger.warning(
                    "Tentativa %d bloqueada: %s | erro original: %s",
                    attempt, dispatch_error, click_error,
                )
        outcomes.append(outcome)
        context.logger.info("Tentativa %d/%d: %s", attempt, QE15_ATTEMPTS, outcome)
    context.qe15_attempts = len(outcomes)
    context.qe15_attempt_outcomes = outcomes


@then("o saldo do remetente deverá ter sido debitado exatamente uma vez")
def qe15_sender_debited_once(context):
    context.transferencia.capture("pos_tentativas_rapidas")
    modal_text = ""
    if context.transferencia.modal.is_visible():
        modal_text = context.transferencia.modal.inner_text()
        context.logger.info("Modal exibido após tentativas: %s", modal_text[:200])
        close_button = context.page.locator("#btnCloseModal")
        if close_button.is_visible():
            close_button.click()
    context.qe15_modal_text = modal_text
    context.qe15_final_sender = _qe15_snapshot_balance(context)
    context.home.capture("remetente_saldo_final")
    expected = context.qe15_initial_sender - _parse_brl(f"{QE15_VALUE},00")
    if context.qe15_final_sender != expected:
        _qe_financial_defect(
            context, "remetente_saldo_final",
            f"saldo final {context.qe15_final_sender:.2f} diverge do esperado "
            f"{expected:.2f} (inicial {context.qe15_initial_sender:.2f}, 1 débito de "
            f"{QE15_VALUE},00). Indício de débito duplicado ou débito ausente "
            f"após {context.qe15_attempts} tentativas",
        )


@then("o extrato do remetente deverá conter um único débito da operação")
def qe15_sender_statement(context):
    context.qe15_statement_sender = _qe_statement(context, "remetente")
    occurrences = context.qe15_statement_sender.count(QE15_DESCRIPTION)
    if occurrences != 1:
        _qe_financial_defect(
            context, "extrato_remetente",
            f"extrato do remetente contém {occurrences} ocorrência(s) da operação "
            f"'{QE15_DESCRIPTION}' após {context.qe15_attempts} tentativas "
            "(débito duplicado ou ausente)",
            context.qe15_statement_sender,
        )
    _qe_logout(context)


@then("o saldo do receptor deverá ter sido creditado exatamente uma vez")
def qe15_receiver_credited_once(context):
    final_receiver = _qe_login(context, context.qe_receiver, "receptor_final")
    context.home.capture("receptor_saldo_final")
    expected = _parse_brl(f"{QE15_VALUE},00")
    if final_receiver != expected:
        _qe_financial_defect(
            context, "receptor_saldo_final",
            f"saldo do receptor {final_receiver:.2f} diverge do esperado {expected:.2f} "
            f"(único crédito de {QE15_VALUE},00). Indício de crédito duplicado ou ausente",
        )
    context.qe15_final_receiver = final_receiver


@then("o extrato do receptor deverá conter um único crédito da operação")
def qe15_receiver_statement(context):
    context.qe15_statement_receiver = _qe_statement(context, "receptor")
    occurrences = context.qe15_statement_receiver.count(QE15_DESCRIPTION)
    if occurrences != 1:
        _qe_financial_defect(
            context, "extrato_receptor",
            f"extrato do receptor contém {occurrences} ocorrência(s) da operação "
            f"'{QE15_DESCRIPTION}' (crédito duplicado ou ausente)",
            context.qe15_statement_receiver,
        )


@then("não deverá existir operação financeira duplicada")
def qe15_no_duplicate_operation(context):
    defects = []
    expected_sender = context.qe15_initial_sender - _parse_brl(f"{QE15_VALUE},00")
    if context.qe15_final_sender != expected_sender:
        defects.append(
            f"remetente: esperado {expected_sender:.2f}, "
            f"exibido {context.qe15_final_sender:.2f}"
        )
    expected_receiver = _parse_brl(f"{QE15_VALUE},00")
    if context.qe15_final_receiver != expected_receiver:
        defects.append(
            f"receptor: esperado {expected_receiver:.2f}, "
            f"exibido {context.qe15_final_receiver:.2f}"
        )
    sender_entries = context.qe15_statement_sender.count(QE15_DESCRIPTION)
    receiver_entries = context.qe15_statement_receiver.count(QE15_DESCRIPTION)
    if sender_entries != 1 or receiver_entries != 1:
        defects.append(
            f"lançamentos '{QE15_DESCRIPTION}': remetente {sender_entries}x, "
            f"receptor {receiver_entries}x (esperado 1x em cada)"
        )
    if defects:
        _qe_financial_defect(
            context, "reconciliacao_concorrencia",
            "inconsistência financeira após tentativas concorrentes: "
            + "; ".join(defects),
            context.qe15_statement_sender + "\n---\n" + context.qe15_statement_receiver,
        )
    context.logger.info(
        "Reconciliação de concorrência QE-03 OK: 1 débito, 1 crédito, saldos exatos"
    )


# ---------------------------------------------------------------------------
# TC_16 - Data Persistence Assessment
# ---------------------------------------------------------------------------

@given("que o usuário A está autenticado com saldo inicial")
def user_a_authenticated(context):
    context.login = LoginPage(context.page, _scenario_name(context))
    context.login.open()
    context.login.login(context.user_a.email, context.user_a.password)
    context.initial_balance = _read_balance(context)
    context.home.capture("saldo_inicial")
    context.logger.info("Saldo inicial do usuário A: %.2f", context.initial_balance)


@given("existe uma conta destinatária válida para transferência")
def destination_exists(context):
    assert context.user_b.account_number, "[DEFEITO QE] Conta destinatária não foi criada no hook"
    context.logger.info("Conta destinatária: %s", context.user_b.account_number)


@when("o usuário A realizar uma transferência de valor válido")
def execute_transfer(context):
    context.transferencia = TransferenciaPage(context.page, _scenario_name(context))
    context.transferencia.open()
    account, digit = context.user_b.account_number.split("-")
    context.transferencia.transfer(account, digit, TRANSFER_VALUE, TRANSFER_DESCRIPTION)


@then("a transferência deverá ser concluída com sucesso")
def transfer_completed(context):
    context.transferencia.assert_modal_contains("sucesso")
    context.transferencia.capture("transferencia_sucesso")
    close_button = context.page.locator("#btnCloseModal")
    if close_button.is_visible():
        close_button.click()


@then("o saldo do usuário A deverá ser atualizado com o débito")
def balance_debited(context):
    assert context.initial_balance > 0, (
        "[DEFEITO QE] Conta criada com saldo inicial zerado; "
        "débito da transferência não pode ser validado"
    )
    context.balance_after_transfer = _read_balance(context)
    context.home.capture("saldo_apos_transferencia")
    expected = context.initial_balance - _parse_brl(f"{TRANSFER_VALUE},00")
    assert context.balance_after_transfer == expected, (
        f"[DEFEITO QE-01] Saldo não reflete o débito exato. Inicial {context.initial_balance:.2f}, "
        f"esperado {expected:.2f}, exibido {context.balance_after_transfer:.2f}"
    )


@when("registrar o extrato da conta")
def register_statement(context):
    context.statement_before_logout = _statement_snapshot(context)
    context.extrato.capture("extrato_antes_logout")
    assert TRANSFER_DESCRIPTION in context.statement_before_logout, (
        "[DEFEITO QE-04] Extrato não registrou a transferência com a descrição "
        f"'{TRANSFER_DESCRIPTION}'. Conteúdo: {context.statement_before_logout[:500]}"
    )
    assert "10,00" in context.statement_before_logout, (
        "[DEFEITO QE-01] Valor da transferência (10,00) ausente no extrato. "
        f"Conteúdo: {context.statement_before_logout[:500]}"
    )
    saldo_match = re.search(
        r"Saldo disponível\s*R\$\s*(-?[\d.]+,\d{2})", context.statement_before_logout
    )
    assert saldo_match, "[DEFEITO QE] Saldo disponível não localizado no extrato"
    statement_balance = _parse_brl(saldo_match.group(1))
    assert statement_balance == context.balance_after_transfer, (
        "[DEFEITO QE-01] Divergência entre saldo da home "
        f"({context.balance_after_transfer:.2f}) e saldo do extrato ({statement_balance:.2f})"
    )
    context.logger.info("Extrato registrado e reconciliado com o saldo da home")


@when("realizar logout da conta")
def logout_account(context):
    context.home = HomePage(context.page, _scenario_name(context))
    context.home.logout_user()
    context.login = LoginPage(context.page, _scenario_name(context))
    context.login.assert_login_screen()


@when("o usuário A realizar login novamente")
def login_again(context):
    context.login.login(context.user_a.email, context.user_a.password)
    context.home = HomePage(context.page, _scenario_name(context))
    context.home.assert_authenticated()


@then("o saldo anterior deverá estar preservado")
def balance_preserved(context):
    balance_after_relogin = _read_balance(context)
    context.home.capture("saldo_apos_relogin")
    assert balance_after_relogin == context.balance_after_transfer, (
        f"[DEFEITO QE-04] Perda de saldo após novo login. Antes {context.balance_after_transfer:.2f}, "
        f"depois {balance_after_relogin:.2f}"
    )


@then("as movimentações do extrato deverão estar preservadas")
def statement_preserved(context):
    statement_after = _statement_snapshot(context)
    context.extrato.capture("extrato_apos_relogin")
    assert TRANSFER_DESCRIPTION in statement_after, (
        "[DEFEITO QE-04] Transferência desapareceu do extrato após novo login. "
        f"Conteúdo: {statement_after[:500]}"
    )
    before_count = context.statement_before_logout.count(TRANSFER_DESCRIPTION)
    after_count = statement_after.count(TRANSFER_DESCRIPTION)
    assert after_count == before_count, (
        "[DEFEITO QE-04] Movimentações divergentes após novo login: "
        f"{before_count} ocorrência(s) antes, {after_count} depois "
        "(perda ou duplicação de lançamentos)"
    )
    saldo_match = re.search(r"Saldo disponível\s*R\$\s*(-?[\d.]+,\d{2})", statement_after)
    assert saldo_match, "[DEFEITO QE] Saldo disponível não localizado no extrato após re-login"
    assert _parse_brl(saldo_match.group(1)) == context.balance_after_transfer, (
        "[DEFEITO QE-01] Saldo do extrato diverge do esperado após novo login"
    )
    context.logger.info("Extrato e saldo preservados após novo login")
