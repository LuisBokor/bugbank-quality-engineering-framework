"""Utilitário one-off: captura screenshots dos relatórios HTML.

Uso:
    python scripts/capture_report_screenshots.py

Saída:
    docs/images/dashboard.png
    docs/images/executive-report.png
    docs/images/detailed-report.png
"""

from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
IMAGES_DIR = ROOT / "docs" / "images"

TARGETS = [
    {
        "source": ROOT / "reports" / "dashboard" / "index.html",
        "output": "dashboard.png",
        "full_page": False,
        "wait_for": ".js-plotly-plot",
    },
    {
        "source": ROOT / "reports" / "html" / "executive_report.html",
        "output": "executive-report.png",
        "full_page": True,
        "wait_for": None,
    },
    {
        "source": ROOT / "reports" / "html" / "detailed_report.html",
        "output": "detailed-report.png",
        "full_page": True,
        "wait_for": None,
    },
]


def main() -> None:
    print("[INFO] Iniciando captura de screenshots...")

    IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch()

        page = browser.new_page(
            viewport={"width": 1600, "height": 900}
        )

        for target in TARGETS:
            source = target["source"]

            if not source.exists():
                print(f"[SKIP] Não encontrado: {source}")
                continue

            print(f"[INFO] Abrindo: {source.name}")

            page.goto(
                source.as_uri(),
                wait_until="networkidle"
            )

            if target["wait_for"]:
                try:
                    page.wait_for_selector(
                        target["wait_for"],
                        timeout=15000
                    )
                except Exception:
                    print(
                        f"[WARN] Timeout aguardando seletor: {target['wait_for']}"
                    )

            page.wait_for_timeout(1500)

            output_path = IMAGES_DIR / target["output"]

            page.screenshot(
                path=str(output_path),
                full_page=target["full_page"]
            )

            print(f"[OK] Gerado: {output_path}")

        browser.close()

    print("[INFO] Processo concluído.")


if __name__ == "__main__":
    main()