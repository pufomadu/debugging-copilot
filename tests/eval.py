"""
Run the 10–20 eval cases end-to-end and print:
- Retrieval hit@5
- Tier accuracy
- Median latency
Usage:
    python -m tests.eval
Before running, make sure you've ingested your PDFs:
    python -m src.ingest
And updated fixtures' gold_citation to match your real filenames + pages.
"""
import json, statistics, time, pathlib, sys
from rich import print

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))  # allow "from src import ..."

from src.tiered_helper import answer
from src.retriever import retrieve

FIXTURE = ROOT / "tests" / "fixtures" / "errors.jsonl"

def load_cases(path):
    with open(path, "r") as f:
        for line in f:
            yield json.loads(line)

def hit_at_k(retrieved, gold_anchor, k=5):
    """
    Consider a hit if the retrieved anchors include the same file (ignoring #page-* detail).
    You can make this stricter by comparing both file and page.
    """
    gold_file = gold_anchor.split("#")[0]
    anchors = [r["source"] for r in retrieved[:k]]
    return 1 if gold_file in anchors else 0

def main():
    ks, tiers_ok, latencies = [], [], []
    n = 0
    for row in load_cases(FIXTURE):
        n += 1
        q = f"{row['error']}\nCODE:\n{row.get('code','')}"
        t0 = time.time()
        retrieved = retrieve(q, k=5)
        resp = answer(row["error"], code_snippet=row.get("code",""))
        latencies.append(time.time() - t0)

        ks.append(hit_at_k(retrieved, row["gold_citation"], k=5))
        tiers_ok.append(1 if int(resp.get("tier", 1)) == int(row["gold_tier"]) else 0)

    print("\n[bold]=== EVAL SUMMARY ===[/bold]")
    print(f"Cases: {n}")
    print(f"Retrieval hit@5: {sum(ks)}/{n} = {sum(ks)/max(n,1):.2f}")
    print(f"Tier accuracy:   {sum(tiers_ok)}/{n} = {sum(tiers_ok)/max(n,1):.2f}")
    print(f"Median latency:  {statistics.median(latencies):.2f}s")
    print("[dim]Tip: paste this table in your README.[/dim]")

if __name__ == "__main__":
    main()
