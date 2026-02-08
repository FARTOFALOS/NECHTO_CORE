import json
import pathlib
import subprocess

prompt = "Я ЕСМЬ. Объясни MU-логику и ethical gravity."

subprocess.run(
    ["python", "-m", "nechto_runtime", "measure"],
    input=prompt.encode("utf-8"),
    check=True,
)

metrics_path = pathlib.Path("docs/latest_metrics.json")
print("Wrote:", metrics_path)
print(json.loads(metrics_path.read_text(encoding="utf-8")))
