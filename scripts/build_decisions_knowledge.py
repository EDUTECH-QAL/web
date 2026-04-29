import json
import re
from pathlib import Path


ROOT = Path(r"D:\edutech\web-qal")
SOURCE = Path(r"D:\الفريق التقني لمديرية التربية والتعليم بالقليوبة\القرارات الداخلية\القرارات.txt")
OUT_DIR = ROOT / "assets" / "edu-assist"


def normalize_space(text: str) -> str:
    return re.sub(r"\s+\n", "\n", re.sub(r"[ \t]+", " ", text)).strip()


def short_text(text: str, limit: int = 900) -> str:
    text = normalize_space(text)
    if len(text) <= limit:
        return text
    clipped = text[:limit]
    last_break = max(clipped.rfind("."), clipped.rfind("،"), clipped.rfind("\n"))
    if last_break > 200:
        clipped = clipped[: last_break + 1]
    return clipped.strip()


def extract_keywords(*parts: str) -> list[str]:
    seen = []
    for part in parts:
        for token in re.split(r"[\s،:()\-\/]+", part):
            token = token.strip()
            if len(token) < 3:
                continue
            if token.isdigit():
                continue
            if token not in seen:
                seen.append(token)
    return seen[:14]


def parse_sections(body: str) -> list[dict]:
    matches = list(re.finditer(r"(?m)^(\d+)\.\s+(.+)$", body))
    sections: list[dict] = []
    if not matches:
        return sections

    for idx, match in enumerate(matches):
        start = match.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(body)
        number = match.group(1)
        heading = match.group(2).strip()
        content = normalize_space(body[start:end])
        sections.append(
            {
                "section_number": int(number),
                "heading": heading,
                "content": content,
                "summary": short_text(content, 700),
                "keywords": extract_keywords(heading),
            }
        )
    return sections


def parse_decisions(text: str) -> list[dict]:
    header_pattern = re.compile(r"(?m)^القرار الداخلي رقم \((\d+)\) لسنة (\d+)$")
    header_matches = list(header_pattern.finditer(text))
    decisions: list[dict] = []

    for idx, header in enumerate(header_matches):
        start = header.start()
        end = header_matches[idx + 1].start() if idx + 1 < len(header_matches) else len(text)
        block = text[start:end].strip()

        lines = [line.rstrip() for line in block.splitlines()]
        if len(lines) < 4:
            continue

        number = int(header.group(1))
        year = int(header.group(2))
        issue_date = ""
        subject = ""
        body_start = 0

        for i, line in enumerate(lines):
            if line.startswith("تاريخ الإصدار:"):
                issue_date = line.split(":", 1)[1].strip()
            elif line.startswith("الموضوع:"):
                subject = line.split(":", 1)[1].strip()
                body_start = i + 1
                break

        body = normalize_space("\n".join(lines[body_start:]))
        sections = parse_sections(body)
        intro = body.split("1.", 1)[0].strip() if "1." in body else body[:1000]
        summary = f"{subject}. {short_text(intro, 500)}"
        decisions.append(
            {
                "decision_number": number,
                "decision_year": year,
                "decision_id": f"decision-{number:03d}",
                "title": f"القرار الداخلي رقم ({number}) لسنة {year}",
                "issue_date": issue_date,
                "subject": subject,
                "summary": summary,
                "keywords": extract_keywords(subject, summary),
                "sections": sections,
                "full_text": body,
            }
        )
    return decisions


def build_flat_knowledge(decisions: list[dict]) -> list[dict]:
    entries: list[dict] = []
    for decision in decisions:
        entries.append(
            {
                "id": f"{decision['decision_id']}-summary",
                "type": "decision_summary",
                "category": "decisions",
                "decision_number": decision["decision_number"],
                "decision_year": decision["decision_year"],
                "title": decision["title"],
                "date": decision["issue_date"],
                "subject": decision["subject"],
                "keywords": decision["keywords"],
                "content": decision["summary"],
                "source": "internal_decisions",
            }
        )
        for section in decision["sections"]:
            entries.append(
                {
                    "id": f"{decision['decision_id']}-section-{section['section_number']}",
                    "type": "decision_section",
                    "category": "decisions",
                    "decision_number": decision["decision_number"],
                    "decision_year": decision["decision_year"],
                    "title": f"{decision['title']} - {section['heading']}",
                    "date": decision["issue_date"],
                    "subject": decision["subject"],
                    "section_number": section["section_number"],
                    "section_title": section["heading"],
                    "keywords": extract_keywords(
                        decision["subject"], section["heading"], *section["keywords"]
                    ),
                    "content": section["summary"],
                    "full_content": section["content"],
                    "source": "internal_decisions",
                }
            )
    return entries


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    text = SOURCE.read_text(encoding="utf-8")
    text = text.replace("\r\n", "\n")
    decisions = parse_decisions(text)
    flat = build_flat_knowledge(decisions)

    nested_path = OUT_DIR / "decisions-structured.json"
    flat_path = OUT_DIR / "decisions-knowledge.json"

    nested_path.write_text(
        json.dumps(decisions, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    flat_path.write_text(
        json.dumps(flat, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"Built {len(decisions)} decisions")
    print(f"Built {len(flat)} flat knowledge entries")
    print(nested_path)
    print(flat_path)


if __name__ == "__main__":
    main()
