"""Gera o dashboard executivo MVP a partir dos JSONs de execução.

Uso:
    python generate_dashboard.py

Entradas:
    reports/json/execution_results.json
    reports/json/execution_history.json (opcional)

Saída:
    reports/dashboard/index.html
"""

import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "reports" / "json" / "execution_results.json"
HISTORY = ROOT / "reports" / "json" / "execution_history.json"
OUTPUT = ROOT / "reports" / "dashboard" / "index.html"

FEATURES = ("cadastro", "login", "transferencia", "extrato")


def feature_key(name: str) -> str:
    value = (name or "").lower()
    if "cadastro" in value:
        return "cadastro"
    if "autentica" in value or "login" in value:
        return "login"
    if "transfer" in value:
        return "transferencia"
    if "extrato" in value or "saldo" in value:
        return "extrato"
    return "cadastro"


def load_json(path: Path, default):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else default


def scenario_sort_key(item: dict):
    """Ordenação numérica por test_id (TC_01, TC_02, ..., TC_10, TC_11, TC_12)."""
    digits = "".join(char for char in str(item.get("test_id", "")) if char.isdigit())
    return int(digits) if digits else 0


def scenario_links(item: dict) -> str:
    links = []
    if item.get("video"):
        links.append(("Vídeo", item["video"]))
    if item.get("execution_log"):
        links.append(("Logs", item["execution_log"]))
    if item.get("page_source"):
        links.append(("HTML", item["page_source"]))
    scenario_dir = str(item.get("video", "")).rsplit("/", 1)[0]
    if scenario_dir:
        links.append(("Massa", f"{scenario_dir}/test_data.json"))
    if item.get("evidence_dir"):
        links.append(("Evidências", item["evidence_dir"]))
    return " · ".join(f"<a href='../../{escape(str(path))}'>{label}</a>" for label, path in links)


def scenario_card(item: dict) -> str:
    status = item.get("status", "")
    video = ""
    if item.get("video"):
        src = escape(str(item["video"]).replace("\\", "/"))
        video = f"<video width='100%' controls preload='metadata'><source src='../../{src}' type='video/webm'></video>"
    shots = "".join(
        f"<a href='../../{escape(shot)}' target='_blank'><img src='../../{escape(shot)}' alt='screenshot' loading='lazy'></a>"
        for shot in item.get("screenshots", [])
    )
    return (
        f"<details class='scenario'><summary>"
        f"<strong>{escape(str(item.get('test_id', '')))}</strong> — {escape(str(item.get('scenario', '')))} "
        f"<span class='{status.lower()}'>{status}</span></summary>"
        f"<div class='body'>{video}<div class='shots'>{shots}</div>"
        f"<p class='links'>{scenario_links(item)}</p>"
        f"<p class='meta'>{escape(str(item.get('executed_at', '')))} · {item.get('duration_seconds', 0)}s · "
        f"console errors: {item.get('console_errors', 0)} · requests: {item.get('network_requests', 0)}</p>"
        f"</div></details>"
    )


def main():
    payload = load_json(RESULTS, {})
    summary = payload.get("summary", {})
    records = payload.get("scenarios", [])
    history = load_json(HISTORY, [])

    total = summary.get("total_scenarios", len(records))
    passed = summary.get("passed", 0)
    failed = summary.get("failed", 0)
    rate = summary.get("success_rate", 0)
    avg = summary.get("average_duration", 0)
    duration = summary.get("total_duration", 0)
    score = summary.get("quality_score", 0)
    classification = summary.get("classification", "—")

    coverage = {key: 0 for key in FEATURES}
    for item in records:
        coverage[feature_key(item.get("feature", ""))] += 1

    kpis = (
        ("Total de Cenários", total),
        ("Aprovados", passed),
        ("Reprovados", failed),
        ("Taxa de Sucesso", f"{rate}%"),
        ("Tempo Médio", f"{avg}s"),
        ("Tempo Total", f"{duration}s"),
    )
    cards = "".join(f"<div class='card'><small>{label}</small><strong>{value}</strong></div>" for label, value in kpis)
    cards += (
        f"<div class='card score-card'><small>Quality Score</small>"
        f"<strong>{score}<span class='unit'>/100</span></strong>"
        f"<span class='classification'>{escape(str(classification))}</span></div>"
    )

    ids = [escape(str(item.get("test_id", ""))) for item in records]
    durations = [item.get("duration_seconds", 0) for item in records]
    hist_x = [escape(str(h.get("executed_at", ""))) for h in history]
    hist_y = [h.get("quality_score", 0) for h in history]
    ordered = sorted(records, key=scenario_sort_key)
    scenarios_html = "".join(scenario_card(item) for item in ordered) or "<p>Nenhum cenário encontrado.</p>"

    html = f"""<!doctype html>
<html lang='pt-br'>
<head>
<meta charset='utf-8'>
<meta name='viewport' content='width=device-width, initial-scale=1'>
<title>BugBank — Dashboard Executivo</title>
<script src='https://cdn.plot.ly/plotly-2.35.2.min.js'></script>
<style>
*{{box-sizing:border-box}}
body{{font-family:'Segoe UI',Arial,sans-serif;background:#0f1720;color:#e6edf3;margin:0;padding:18px 28px 28px;font-size:14px}}
.container{{max-width:1920px;margin:0 auto}}
h1{{color:#58a6ff;margin:0 0 2px;font-size:22px}}
.subtitle{{color:#8b98a5;margin:0 0 14px;font-size:12px}}
.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:10px;margin:0 0 14px}}
.card{{background:#161d27;border:1px solid #2a3542;border-radius:8px;padding:10px 14px;min-width:0}}
.card small{{color:#8b98a5;text-transform:uppercase;letter-spacing:.4px;font-size:10px;display:block}}
.card strong{{display:block;font-size:20px;margin-top:4px;line-height:1.15;white-space:nowrap}}
.card.score-card{{background:linear-gradient(135deg,#132a1c,#161d27);border-color:#2a4a35}}
.card.score-card strong{{color:#3fb950;font-size:20px}}
.card.score-card .unit{{font-size:12px;color:#8b98a5;font-weight:400}}
.card.score-card .classification{{display:block;font-size:11px;color:#8b98a5;font-weight:600;margin-top:2px}}
.graphs{{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:12px;margin:0 0 18px}}
.graph{{background:#161d27;border:1px solid #2a3542;border-radius:8px;padding:6px;height:300px}}
h2{{color:#58a6ff;border-bottom:1px solid #2a3542;padding-bottom:6px;font-size:16px;margin:20px 0 10px}}
.scenario{{background:#161d27;border:1px solid #2a3542;border-radius:10px;margin:8px 0;padding:12px 16px}}
.scenario summary{{cursor:pointer;font-size:14px}}
.scenario .body{{margin-top:12px}}
.scenario video{{border-radius:8px;background:#000;max-width:480px}}
.shots img{{max-width:24%;border-radius:6px;margin:8px 8px 0 0;border:1px solid #2a3542}}
.links a{{color:#58a6ff;margin-right:4px}}
.meta{{color:#8b98a5;font-size:12px}}
.pass{{color:#3fb950;font-weight:700}}
.fail{{color:#f85149;font-weight:700}}
@media (max-width:1400px){{
  .graphs{{grid-template-columns:repeat(auto-fit,minmax(260px,1fr))}}
  .cards{{grid-template-columns:repeat(auto-fit,minmax(120px,1fr))}}
}}
@media (max-height:820px){{
  .graph{{height:250px}}
  body{{padding:14px 22px 22px}}
}}
</style>
</head>
<body>
<div class='container'>
<h1>BugBank · Dashboard Executivo</h1>
<p class='subtitle'>Execução: {escape(str(summary.get('generated_at', '—')))} · Ambiente: {escape(str(summary.get('environment', '—')))} · Browser: {escape(str(summary.get('browser', '—')))}</p>

<section class='cards'>{cards}</section>

<section class='graphs'>
  <div class='graph' id='g_passfail'></div>
  <div class='graph' id='g_coverage'></div>
  <div class='graph' id='g_duration'></div>
  <div class='graph' id='g_history'></div>
</section>

<h2>Cenários</h2>
{scenarios_html}
</div>

<script>
const layout = {{paper_bgcolor:'rgba(0,0,0,0)',plot_bgcolor:'rgba(0,0,0,0)',font:{{color:'#e6edf3',size:11}},margin:{{t:32,b:32,l:36,r:16}},autosize:true}};
const config = {{responsive:true,displayModeBar:false,displaylogo:false}};
Plotly.newPlot('g_passfail',[{{type:'pie',labels:['Aprovados','Reprovados'],values:[{passed},{failed}],marker:{{colors:['#3fb950','#f85149']}},hole:.45}}],{{...layout,title:'Pass × Fail'}},config);
Plotly.newPlot('g_coverage',[{{type:'bar',x:{list(coverage)},y:{list(coverage.values())},marker:{{color:'#58a6ff'}}}}],{{...layout,title:'Cobertura por Funcionalidade'}},config);
Plotly.newPlot('g_duration',[{{type:'bar',x:{ids},y:{durations},marker:{{color:'#d29922'}}}}],{{...layout,title:'Tempo por Cenário (s)'}},config);
Plotly.newPlot('g_history',[{{type:'scatter',mode:'lines+markers',x:{hist_x},y:{hist_y},line:{{color:'#3fb950'}}}}],{{...layout,title:'Histórico de Execuções (Quality Score)'}},config);
window.addEventListener('resize',()=>{{
  ['g_passfail','g_coverage','g_duration','g_history'].forEach(id=>Plotly.Plots.resize(document.getElementById(id)));
}});
</script>
</body>
</html>"""


    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(html, encoding="utf-8")
    print(f"Dashboard gerado: {OUTPUT}")


if __name__ == "__main__":
    main()
