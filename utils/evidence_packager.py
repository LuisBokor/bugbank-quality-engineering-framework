"""Consolidação profissional de artefatos por cenário.

Responsabilidade única: ao final de cada cenário, organizar a pasta
``videos/<CENARIO>/`` com vídeo renomeado, screenshots, execution.log,
massa de teste (test_data.json) e HTML capturado, além de atualizar o
record que alimenta os relatórios executivos.

Não altera testes, steps, pages ou a execução — apenas empacota
evidências já produzidas pelo ScenarioRecorder e pelo Playwright.
"""

import json
import shutil
from dataclasses import asdict, is_dataclass
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VIDEOS = ROOT / "videos"

# Atributos do context que carregam massa de teste (AccountContext).
_MASS_ATTRIBUTES = ("account", "destination", "user_a", "user_b")


def safe_name(value: str) -> str:
    import re

    return re.sub(r"[^A-Za-z0-9_.-]+", "_", value).strip("_")


def package_scenario_artifacts(context, scenario, record, page_html=""):
    """Consolida artefatos do cenário e enriquece o record de relatório."""
    try:
        scenario_dir = VIDEOS / safe_name(scenario.name)
        scenario_dir.mkdir(parents=True, exist_ok=True)
        _consolidate_videos(scenario_dir, record)
        _copy_screenshots(scenario_dir, record)
        _write_execution_log(scenario_dir, scenario, record)
        _write_test_data(scenario_dir, context)
        _write_page_source(scenario_dir, record, page_html)
    except Exception as error:  # nunca quebrar a suíte por causa do empacotamento
        record["packaging_error"] = str(error)
    return record


def _relative(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def _consolidate_videos(scenario_dir: Path, record: dict):
    videos = sorted(
        (p for p in scenario_dir.glob("*.webm") if p.stem not in {"video"} and not p.stem.startswith("video_")),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    if not videos:
        return
    primary = scenario_dir / "video.webm"
    shutil.move(str(videos[0]), str(primary))
    for index, extra in enumerate(videos[1:], start=2):
        shutil.move(str(extra), str(scenario_dir / f"video_{index:02d}.webm"))
    record["video"] = _relative(primary)


def _copy_screenshots(scenario_dir: Path, record: dict):
    evidence_dir = ROOT / str(record.get("evidence_dir", ""))
    if not evidence_dir.is_dir():
        return
    target = scenario_dir / "screenshots"
    target.mkdir(exist_ok=True)
    screenshots = []
    for image in sorted(evidence_dir.glob("*.png")):
        destination = target / image.name
        shutil.copy2(str(image), str(destination))
        screenshots.append(_relative(destination))
    record["screenshots"] = screenshots


def _write_execution_log(scenario_dir: Path, scenario, record: dict):
    lines = [
        f"cenario={scenario.name}",
        f"status={record.get('status')}",
        f"duracao_segundos={record.get('duration_seconds')}",
        f"executado_em={record.get('executed_at')}",
        f"url_final={record.get('url')}",
        f"console_errors={record.get('console_errors')}",
        f"network_requests={record.get('network_requests')}",
    ]
    evidence_console = ROOT / str(record.get("evidence_dir", "")) / "console.log"
    if evidence_console.exists():
        lines.append("")
        lines.append("=== console do navegador ===")
        lines.append(evidence_console.read_text(encoding="utf-8"))
    log_path = scenario_dir / "execution.log"
    log_path.write_text("\n".join(lines), encoding="utf-8")
    record["execution_log"] = _relative(log_path)


def _write_test_data(scenario_dir: Path, context):
    mass = {}
    for attribute in _MASS_ATTRIBUTES:
        value = getattr(context, attribute, None)
        if value is None:
            continue
        data = asdict(value) if is_dataclass(value) else dict(value)
        if data.get("password"):
            data["password"] = "***"  # não expor credencial em evidência
        mass[attribute] = data
    if not mass:
        return
    mass["_meta"] = {"gerado_em": datetime.now().isoformat(timespec="seconds"), "origem": "Faker pt_BR"}
    data_path = scenario_dir / "test_data.json"
    data_path.write_text(json.dumps(mass, ensure_ascii=False, indent=2), encoding="utf-8")


def _write_page_source(scenario_dir: Path, record: dict, page_html: str):
    html_dir = scenario_dir / "html"
    html_dir.mkdir(exist_ok=True)
    source = html_dir / "page_source.html"
    if page_html:
        source.write_text(page_html, encoding="utf-8")
    else:
        evidence_html = ROOT / str(record.get("evidence_dir", "")) / "page.html"
        if evidence_html.exists():
            shutil.copy2(str(evidence_html), str(source))
        else:
            return
    record["page_source"] = _relative(source)
