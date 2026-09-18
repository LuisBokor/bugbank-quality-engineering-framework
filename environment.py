import os
import re
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

from pages.cadastro_page import CadastroPage
from pages.login_page import LoginPage
from pages.transferencia_page import TransferenciaPage
from utils.account_context import AccountContext
from utils.evidence_packager import package_scenario_artifacts
from utils.faker_utils import new_account
from utils.logger import get_logger
from utils.observability import ROOT, create_recorder, generate_reports


BROWSER_CHANNEL = os.getenv("BROWSER_CHANNEL", "msedge")
HEADLESS = os.getenv("HEADLESS", "0") == "1"
VIEWPORT = {"width": 1440, "height": 900}


AUTH_SCENARIOS = {
    "TC_02 - Acessar a Conta",
    "TC_07 - Realizar Login com Senha Inválida",
    "TC_08 - Realizar Logout da Aplicação",
    "TC_09 - Consultar Saldo da Conta",
    "TC_10 - Realizar Transferência sem Saldo Suficiente",
    "TC_12 - Fluxo E2E Completo de Transferência, Extrato, Saldo e Logout",
}


def before_scenario(context, scenario):
    context.logger = get_logger(scenario.name)
    context.playwright = sync_playwright().start()
    context.browser = context.playwright.chromium.launch(
        channel=BROWSER_CHANNEL,
        headless=HEADLESS,
    )
    video_dir = ROOT / "videos" / re.sub(r"[^A-Za-z0-9_.-]+", "_", scenario.name)
    video_dir.mkdir(parents=True, exist_ok=True)
    context.browser_context = context.browser.new_context(
        viewport=VIEWPORT,
        record_video_dir=str(video_dir),
    )
    context.page = context.browser_context.new_page()
    create_recorder(context, scenario)
    context.account = AccountContext(**new_account())
    context.logger.info("Iniciando cenário %s", scenario.name)

    if scenario.name in AUTH_SCENARIOS:
        _create_account(context, context.account)
    if scenario.name == "TC_10 - Realizar Transferência sem Saldo Suficiente":
        context.destination = AccountContext(**new_account())
        _create_account(context, context.destination)
    if scenario.name == "TC_12 - Fluxo E2E Completo de Transferência, Extrato, Saldo e Logout":
        _prepare_e2e_transfer(context)


def after_scenario(context, scenario):
    recorder = getattr(context, "observability", None)
    record = recorder.finish(scenario) if recorder else {"scenario": scenario.name, "status": scenario.status}
    page_html = ""
    try:
        if getattr(context, "page", None):
            page_html = context.page.content()
    except Exception:
        page_html = ""
    try:
        if getattr(context, "browser_context", None):
            context.browser_context.close()
            if getattr(context, "page", None) and context.page.video:
                raw_video_path = str(context.page.video.path()).replace("\\", "/")
                if raw_video_path.startswith("videos/"):
                    record["video"] = raw_video_path
                else:
                    video_path = Path(raw_video_path)
                    if video_path.is_absolute():
                        try:
                            record["video"] = str(video_path.relative_to(ROOT)).replace("\\", "/")
                        except ValueError:
                            record["video"] = raw_video_path
                    else:
                        record["video"] = f"videos/{video_path.name}"
    except Exception as error:
        record["video_error"] = str(error)
    finally:
        if getattr(context, "browser", None):
            context.browser.close()
        if getattr(context, "playwright", None):
            context.playwright.stop()
    package_scenario_artifacts(context, scenario, record, page_html)
    context._report_records.append(record)


def after_step(context, step):
    if step.status == "failed":
        recorder = getattr(context, "observability", None)
        if recorder:
            recorder.capture_failure(step)


def before_all(context):
    context._report_records = []
    context._report_started_at = time.perf_counter()


def before_step(context, step):
    recorder = getattr(context, "observability", None)
    if recorder:
        recorder.before_step(step)


def after_all(context):
    generate_reports(
        context._report_records,
        context._report_started_at,
        BROWSER_CHANNEL,
        os.getenv("TEST_ENVIRONMENT", "bugbank.netlify.app"),
    )


def _create_account(context, account, with_initial_balance=False):
    page = CadastroPage(context.page, context.scenario.name.replace(" ", "_"))
    last_body = ""
    for _ in range(3):
        try:
            page.open()
            page.open_form()
            page.fill(account)
            if with_initial_balance:
                page.select_initial_balance()
            page.submit_form()
            page.assert_success()
            modal_text = page.modal.inner_text()
            account_number = re.search(r"\d{3}-\d", modal_text)
            if account_number:
                account.account_number = account_number.group(0)
                close_button = context.page.locator("#btnCloseModal")
                if close_button.is_visible():
                    close_button.click()
                return
        except Exception:
            last_body = context.page.locator("body").inner_text()
            account.email = new_account()["email"]
    raise AssertionError(f"Não foi possível criar a conta de teste. Página: {last_body}")


def _prepare_e2e_transfer(context):
    context.user_a = AccountContext(**new_account())
    context.user_b = AccountContext(**new_account())
    _create_account(context, context.user_a, with_initial_balance=True)
    _create_account(context, context.user_b)

    login = LoginPage(context.page, context.scenario.name.replace(" ", "_"))
    login.open()
    login.login(context.user_a.email, context.user_a.password)
    transfer = TransferenciaPage(context.page, context.scenario.name.replace(" ", "_"))
    transfer.open()
    account, digit = context.user_b.account_number.split("-")
    transfer.transfer(account, digit, "10", "Preparação TC12")
    transfer.assert_modal_contains("sucesso")
    close_button = context.page.locator("#btnCloseModal")
    if close_button.is_visible():
        close_button.click()
