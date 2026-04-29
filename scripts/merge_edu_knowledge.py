import json
from pathlib import Path


ROOT = Path(r"D:\edutech\web-qal")
BASE_PATH = ROOT / "assets" / "edu-assist" / "knowledge-base.json"
DECISIONS_PATH = ROOT / "assets" / "edu-assist" / "decisions-knowledge.json"
OUT_PATH = ROOT / "assets" / "edu-assist" / "edu-assist-knowledge.json"


def main() -> None:
    base_items = json.loads(BASE_PATH.read_text(encoding="utf-8"))
    decision_items = json.loads(DECISIONS_PATH.read_text(encoding="utf-8"))

    merged = []
    seen = set()
    for item in base_items + decision_items:
        item_id = item.get("id")
        if not item_id or item_id in seen:
            continue
        seen.add(item_id)
        merged.append(item)

    OUT_PATH.write_text(
        json.dumps(merged, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"Merged {len(base_items)} base entries + {len(decision_items)} decision entries")
    print(f"Output entries: {len(merged)}")
    print(OUT_PATH)


if __name__ == "__main__":
    main()
