import json
import re
import unicodedata
from datetime import datetime, UTC
from pathlib import Path

import pandas as pd


ROOT = Path(r"D:\edutech\web-qal")
TECHDAY_DIR = ROOT / "n8n" / "فعالية TechDay"
OUT_PATH = ROOT / "assets" / "edu-assist" / "techday-students-db.json"

STANDARD_COLUMNS = [
    "name",
    "student_id",
    "group_name",
    "group_code",
    "school",
    "administration",
    "email",
    "grade",
    "attended",
    "attendance_time",
    "points",
    "blacklist",
    "certificate_blocked",
    "created_at",
    "username",
]

EVENTS = {
    "غرب شبرا.xlsx": {
        "event_id": "techday-west-shubra",
        "event_name": "Tech Day غرب شبرا الخيمة",
        "location": "غرب شبرا الخيمة",
        "host_school": "مدرسة عمر بن الخطاب الثانوية بنات",
        "official_post_type": "حصاد فعالية + بيان تفصيلي",
        "stats": {
            "registered": 350,
            "attended": 231,
            "attendance_rate": "66%",
            "team_count": 5,
            "top_teams": [
                {"name": "Vision Team", "points": 800, "rank": 1},
                {"name": "Bright Stars", "points": 590, "rank": 2},
                {"name": "Warriors Team", "points": 550, "rank": 3},
                {"name": "Pioneers Team", "points": 520, "rank": 4},
                {"name": "Heroes Team", "points": 360, "rank": 5},
            ],
            "best_workshops": [
                {"title": "Communication Skills", "rating": 4.6},
                {"title": "THINK OUTSIDE THE BOX", "rating": 4.5},
                {"title": "KeyLeader", "rating": 4.5},
            ],
            "top_individuals": [
                "يمنى وائل حسن",
                "استيفين أيمن رضا",
                "آية محمود عاطف",
                "لميس سامح محمد",
                "كريمان أحمد فوده",
            ],
            "administration_participation": {
                "غرب شبرا الخيمة": 117,
                "شرق شبرا الخيمة": 114,
            },
            "note": "الأغلبية كانت من الصف الأول الثانوي وفق البوست الرسمي.",
        },
        "workshops": [
            {"title": "THINK OUTSIDE THE BOX", "instructor": "مريم عبده عبدالله محمد"},
            {"title": "Personality Skills", "instructor": "عمر محمد عيد"},
            {"title": "Communication Skills", "instructor": "سلفيا سامح نبيل"},
            {"title": "From Idea To Design", "instructor": "زياد محمد عبدالعزيز"},
            {"title": "Journey in The World of Games", "instructor": "مالك أحمد محمد الجمل"},
            {"title": "Robotics World", "instructor": "أحمد محمد عبدالعليم"},
            {"title": "Cheap Dopamine, Costly Mind", "instructor": "بلال محمود"},
            {"title": "KeyLeader", "instructor": "سيليا أحمد السيد"},
            {"title": "Python Programming Basics", "instructor": "تسنيم محمود محمد أبوزيد"},
        ],
        "official_links": [],
        "notes": [
            "تم إرسال الشهادات على البريد الإلكتروني وفق البوست الرسمي.",
            "تم تنفيذ الفعالية تحت رعاية وتوجيهات الجهات التعليمية المذكورة في البيان الرسمي.",
        ],
    },
    "العبور.xlsx": {
        "event_id": "techday-obour",
        "event_name": "Tech Day العبور",
        "location": "العبور",
        "host_school": "Modern Avenue School",
        "official_post_type": "بيان فعالية",
        "stats": {},
        "workshops": [
            {"title": "Explore The World Of Arduino", "instructor": "أحمد محمد عبدالعليم"},
            {"title": "Cheap Dopamine, Costly Mind", "instructor": "بلال محمود"},
            {"title": "From Idea To Design", "instructor": "زياد محمد عبدالعزيز"},
            {"title": "Journey in The World of Games", "instructor": "مالك أحمد محمد الجمل"},
            {"title": "Future With AI", "instructor": "تسبيح حسن"},
        ],
        "official_links": [],
        "notes": [
            "البوست الرسمي ركّز على التفاعل الكبير من الطلاب وشكر المدرسة والمحاضرين وفريق التنظيم.",
        ],
    },
    "بنها.xlsx": {
        "event_id": "techday-banha",
        "event_name": "Tech Day بنها",
        "location": "بنها",
        "host_school": "مدرسة مصطفى كامل الرسمية المتميزة للغات",
        "official_post_type": "منشوران رسميان لنسختين في نفس المدرسة",
        "stats": {
            "special_note": "ورد في البوست الرسمي أن اليوم الثاني شهد حضور 155 طالبًا وطالبة.",
        },
        "workshops": [
            {"title": "Python Programming Basics", "instructor": "مالك أحمد محمد الجمل وأحمد عبدالرؤف سمير"},
            {"title": "Beyond the Semicolon (C++)", "instructor": "زياد محمد عبدالعزيز"},
            {"title": "Personality Workshop", "instructor": "عمر محمد عيد"},
            {"title": "Explore The World Of Arduino", "instructor": "أحمد محمد عبدالعليم"},
            {"title": "KeyLeader", "instructor": "سلفيا سامح نبيل"},
            {"title": "Robotics World", "instructor": "أحمد محمد عبدالعليم"},
            {"title": "From Idea To Design", "instructor": "زياد محمد عبدالعزيز"},
            {"title": "Emotional Intelligence", "instructor": "سلفيا سامح نبيل"},
            {"title": "Simple World Of Web", "instructor": "يوسف محمد حازم"},
            {"title": "Tech Journey", "instructor": "الحسن عمرو عبدالعليم شفيق"},
            {"title": "Future With AI", "instructor": "تسبيح حسن"},
            {"title": "Journey in The World of Games", "instructor": "مالك أحمد محمد الجمل"},
        ],
        "official_links": [],
        "notes": [
            "الفعالية نُفذت مرتين في نفس المدرسة وفق البوستات الرسمية.",
            "تم إرسال الشهادات على البريد الإلكتروني المسجل وفق أحد المنشورين.",
        ],
    },
}


def clean_text(value) -> str:
    if pd.isna(value):
        return ""
    text = str(value)
    text = "".join(ch for ch in text if unicodedata.category(ch)[0] != "C")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def normalize_arabic(text: str) -> str:
    text = clean_text(text).lower()
    substitutions = {
        "أ": "ا",
        "إ": "ا",
        "آ": "ا",
        "ى": "ي",
        "ة": "ه",
        "ؤ": "و",
        "ئ": "ي",
    }
    for src, dst in substitutions.items():
        text = text.replace(src, dst)
    text = re.sub(r"[^\w\s@.]", " ", text, flags=re.UNICODE)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def mask_email(email: str) -> str:
    email = clean_text(email)
    if "@" not in email:
        return ""
    name, domain = email.split("@", 1)
    if len(name) <= 2:
        masked_name = name[0] + "*"
    else:
        masked_name = name[:2] + "*" * max(2, len(name) - 2)
    return f"{masked_name}@{domain}"


def to_bool(text: str):
    normalized = clean_text(text)
    if normalized == "نعم":
        return True
    if normalized == "لا":
        return False
    return None


def load_students() -> list[dict]:
    students: list[dict] = []
    for path in sorted(TECHDAY_DIR.glob("*.xlsx")):
        event = EVENTS[path.name]
        excel = pd.ExcelFile(path)
        df = pd.read_excel(path, sheet_name=excel.sheet_names[0], header=1)
        df.columns = STANDARD_COLUMNS

        for _, row in df.iterrows():
            name = clean_text(row["name"])
            student_id = clean_text(row["student_id"]).replace(".0", "")
            if not name or "الإدارة التعليمية:" in name or not student_id:
                continue

            administration = clean_text(row["administration"])
            school = clean_text(row["school"])
            group_name = clean_text(row["group_name"])
            group_code = clean_text(row["group_code"])
            grade = clean_text(row["grade"])
            email = clean_text(row["email"])
            attended = to_bool(row["attended"])
            attendance_time = clean_text(row["attendance_time"])
            points_text = clean_text(row["points"]).replace(".0", "")
            points = int(points_text) if points_text.isdigit() else 0
            blacklist = to_bool(row["blacklist"])
            certificate_blocked = to_bool(row["certificate_blocked"])
            created_at = clean_text(row["created_at"])
            username = clean_text(row["username"])

            students.append(
                {
                    "record_id": f"{event['event_id']}::{student_id}",
                    "event_id": event["event_id"],
                    "event_name": event["event_name"],
                    "student_name": name,
                    "normalized_name": normalize_arabic(name),
                    "student_id": student_id,
                    "username": username,
                    "email_lookup": email.lower(),
                    "email_masked": mask_email(email),
                    "administration": administration,
                    "school": school,
                    "group_name": group_name,
                    "group_code": group_code,
                    "grade": grade,
                    "attended": attended,
                    "attendance_time": attendance_time,
                    "points": points,
                    "blacklist": blacklist,
                    "certificate_blocked": certificate_blocked,
                    "created_at": created_at,
                    "source_file": path.name,
                }
            )
    return students


def build_events(students: list[dict]) -> list[dict]:
    event_map: dict[str, list[dict]] = {}
    for student in students:
        event_map.setdefault(student["event_id"], []).append(student)

    events: list[dict] = []
    for path_name, meta in EVENTS.items():
        rows = event_map.get(meta["event_id"], [])
        attended_count = sum(1 for row in rows if row["attended"] is True)
        events.append(
            {
                "event_id": meta["event_id"],
                "event_name": meta["event_name"],
                "location": meta["location"],
                "host_school": meta["host_school"],
                "official_post_type": meta["official_post_type"],
                "workshops": meta["workshops"],
                "notes": meta["notes"],
                "stats": {
                    **meta["stats"],
                    "student_records_in_file": len(rows),
                    "attended_records_in_file": attended_count,
                },
                "source_file": path_name,
            }
        )
    return events


def main() -> None:
    students = load_students()
    events = build_events(students)
    payload = {
        "generated_at": datetime.now(UTC).isoformat(),
        "student_count": len(students),
        "event_count": len(events),
        "events": events,
        "students": students,
    }
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {OUT_PATH}")
    print(f"students={len(students)} events={len(events)}")


if __name__ == "__main__":
    main()
