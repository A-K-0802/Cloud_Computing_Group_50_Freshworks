"""
benchmark.py  –  Group 50 | Theme 4: Serverless Cold Start Benchmarking
Person B deliverable.

Usage:
  Quick test  (1 round, 5 requests – no AWS keys needed):
      python benchmark/benchmark.py <URL> 1 5 --no-force

  Full benchmark (5 rounds × 100 requests – needs AWS keys):
      python benchmark/benchmark.py <URL>
"""

import csv, os, sys, time, requests

# ── optional: only imported when forcing cold starts (needs AWS keys) ──
def _get_boto_client():
    try:
        import boto3
        return boto3.client("lambda", region_name="ap-south-1")
    except ImportError:
        return None

URL   = sys.argv[1] if len(sys.argv) > 1 else \
        "https://w3obh27tnh.execute-api.ap-south-1.amazonaws.com/submit"
FUNC  = "SubmitFunction"
ROUNDS = int(sys.argv[2]) if len(sys.argv) > 2 else 5
REQS   = int(sys.argv[3]) if len(sys.argv) > 3 else 100
NO_FORCE = "--no-force" in sys.argv   # skip cold-start forcing (no AWS keys needed)

# ── Force a cold start by bumping a Lambda env variable ───────────────
def force_cold_start(lam):
    cfg = lam.get_function_configuration(FunctionName=FUNC)
    env = cfg["Environment"]["Variables"]
    env["BUMP"] = str(time.time())
    lam.update_function_configuration(FunctionName=FUNC,
                                      Environment={"Variables": env})
    lam.get_waiter("function_updated_v2").wait(FunctionName=FUNC)
    time.sleep(2)
    print(f"  [cold-start forced]")

# ── Main benchmark loop ────────────────────────────────────────────────
os.makedirs("results", exist_ok=True)
rows = []

lam = None
if not NO_FORCE:
    lam = _get_boto_client()
    if lam is None:
        print("WARNING: boto3 not installed – running in --no-force mode.")
        NO_FORCE = True

print("\n" + "="*55)
print("  Serverless Cold Start Benchmark  -  Group 50")
print(f"  URL   : {URL}")
print(f"  Rounds: {ROUNDS}   Requests/round: {REQS}")
mode_str = "warm-only (no-force)" if NO_FORCE else "full (cold-start forced)"
print(f"  Mode  : {mode_str}")
print("="*55 + "\n")

for r in range(1, ROUNDS + 1):
    print(f"-- Round {r}/{ROUNDS} --")
    if not NO_FORCE:
        force_cold_start(lam)

    for n in range(1, REQS + 1):
        t = time.perf_counter()
        try:
            resp = requests.post(URL,
                                 json={"round": r, "n": n, "value": 1.5},
                                 timeout=30)
            ms   = (time.perf_counter() - t) * 1000
            cold = resp.json().get("cold_start", None)
            code = resp.status_code
        except Exception as e:
            ms, cold, code = -1, None, 0
            print(f"  ERROR: {e}")

        rows.append([r, n, round(ms, 2), code, cold])
        tag = " <<< COLD START" if cold else ""
        print(f"  req {n:>3}: {ms:>8.1f} ms  |  status={code}  cold={cold}{tag}")

print("\nDone! Writing results/latency.csv ...")
with open("results/latency.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["round", "request_no", "latency_ms", "status", "cold_start"])
    w.writerows(rows)

print("SAVED: results/latency.csv")
print("  --> Now run:  python benchmark/analyze.py")
