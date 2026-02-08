from nechto_runtime import State, measure_text

prompt = "Я ЕСМЬ. Объясни MU-логику и ethical gravity."

state = State()
metrics, contract = measure_text(prompt, state)

print("Gate status:", contract["GATE_STATUS"])
print("Metrics summary:")
for key in ("TI", "CI", "AR", "SQ_proxy", "FLOW"):
    print(f"  {key}: {metrics.get(key)}")
