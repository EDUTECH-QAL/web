import json
from pathlib import Path


WORKFLOW_PATH = Path(r"D:\edutech\web-qal\n8n\edu-assist-workflow.json")


DETECT_INTENT_CODE = """return items.map((item) => {
  const text = item.json.normalizedMessage || '';
  const hasAny = (...terms) => terms.some((term) => text.includes(term));
  const hasStudentId = /\\b\\d{5,}\\b/.test(text);
  const hasUsername = /\\bstudent_\\d+\\b/i.test(text);
  const hasEmail = /[a-z0-9._%+-]+@[a-z0-9.-]+\\.[a-z]{2,}/i.test(text);
  const hasStudentContext = hasAny('الطالب', 'طالب', 'رقم الطالب', 'بيانات الطالب', 'بياناته', 'معلومات الطالب', 'شهادة', 'النقاط', 'حضر', 'الحضور', 'المجموعة', 'المدرسة');

  let intent = 'ai';
  if (!text) intent = 'empty';
  else if (hasAny('/student', 'student command', 'student help')) intent = 'command_student';
  else if (hasAny('/techday', 'techday command', 'techday help')) intent = 'command_techday';
  else if (hasAny('/start', 'ابدأ', 'ابدا', 'السلام', 'اهلا', 'مرحبا', 'hello', 'hi')) intent = 'welcome';
  else if (hasAny('من انتم', 'ما هو الفريق', 'مين انتم', 'عرفني بالفريق', 'نبذة', 'نبذه', 'ايه هو الفريق')) intent = 'faq_about';
  else if (hasAny('تواصل', 'اتواصل', 'لينك', 'رابط', 'contact', 'الموقع', 'website')) intent = 'faq_contact';
  else if (hasStudentId || hasUsername || hasEmail || hasStudentContext) intent = 'student_lookup';
  else if (hasAny('tech day', 'تك داي', 'techday', 'الفعالية', 'الفعاليات')) intent = 'faq_techday';

  return {
    json: {
      ...item.json,
      intent
    }
  };
});"""


STUDENT_LOOKUP_CODE = """const original = $items('Detect Intent', 0, 0)[0].json;
const payload = items[0].json || {};
const students = Array.isArray(payload.students) ? payload.students : [];
const events = Array.isArray(payload.events) ? payload.events : [];
const eventsById = Object.fromEntries(events.map((event) => [event.event_id, event]));
const rawQuery = String(original.userMessage || '').trim();

function normalizeArabic(text) {
  return String(text || '')
    .toLowerCase()
    .replace(/[\\u064B-\\u065F\\u0670]/g, '')
    .replace(/[أإآ]/g, 'ا')
    .replace(/ى/g, 'ي')
    .replace(/ة/g, 'ه')
    .replace(/ؤ/g, 'و')
    .replace(/ئ/g, 'ي')
    .replace(/[^\\p{L}\\p{N}@._\\s-]/gu, ' ')
    .replace(/\\s+/g, ' ')
    .trim();
}

function maskEmail(email) {
  const value = String(email || '');
  if (!value.includes('@')) return '';
  const [name, domain] = value.split('@');
  if (name.length <= 2) return `${name[0] || ''}*@${domain}`;
  return `${name.slice(0, 2)}${'*'.repeat(Math.max(2, name.length - 2))}@${domain}`;
}

const query = normalizeArabic(rawQuery);
const bulkSignals = [
  'كل الطلاب',
  'جميع الطلاب',
  'هاتلي كل',
  'اعرض كل',
  'اسمهم',
  'الطلاب اللي',
  'قائمة الطلاب',
  'كل من',
  'كل طالب',
  'كل الاسماء'
];

if (bulkSignals.some((signal) => query.includes(normalizeArabic(signal)))) {
  const replyText = 'لأسباب تنظيمية وخصوصية، يمكنني التعامل مع بيانات طالب واحد فقط في كل مرة. من فضلك أرسل الاسم الكامل للطالب أو رقم الطالب أو اسم المستخدم المرتبط به فقط.';
  return [{ json: { ...original, source: 'student_db', matchedKnowledge: 'student_lookup_bulk_blocked', replyText, replyPreview: replyText.slice(0, 150) } }];
}

const eventHints = [
  { id: 'techday-west-shubra', patterns: ['غرب شبرا', 'شرق شبرا', 'شبرا الخيمة', 'شبرا الخيمه'] },
  { id: 'techday-obour', patterns: ['العبور', 'obour'] },
  { id: 'techday-banha', patterns: ['بنها', 'banha'] },
];
const eventHint = eventHints.find((item) => item.patterns.some((pattern) => query.includes(normalizeArabic(pattern))));
let pool = eventHint ? students.filter((student) => student.event_id === eventHint.id) : students.slice();

const idMatches = [...rawQuery.matchAll(/\\b\\d{5,}\\b/g)].map((match) => match[0]);
const usernameMatches = [...rawQuery.matchAll(/\\bstudent_\\d+\\b/gi)].map((match) => match[0].toLowerCase());
const emailMatches = [...rawQuery.matchAll(/[a-z0-9._%+-]+@[a-z0-9.-]+\\.[a-z]{2,}/gi)].map((match) => match[0].toLowerCase());
const identifierCount = idMatches.length + usernameMatches.length + emailMatches.length;

if (identifierCount > 1) {
  const replyText = 'من فضلك أرسل معرفًا واحدًا فقط في كل مرة: رقم طالب واحد أو اسم مستخدم واحد أو بريد إلكتروني واحد.';
  return [{ json: { ...original, source: 'student_db', matchedKnowledge: 'student_lookup_multiple_identifiers', replyText, replyPreview: replyText.slice(0, 150) } }];
}

let matches = [];
let matchedBy = '';
if (idMatches.length === 1) {
  matchedBy = 'student_id';
  matches = pool.filter((student) => String(student.student_id) === idMatches[0]);
} else if (usernameMatches.length === 1) {
  matchedBy = 'username';
  matches = pool.filter((student) => String(student.username || '').toLowerCase() === usernameMatches[0]);
} else if (emailMatches.length === 1) {
  matchedBy = 'email';
  matches = pool.filter((student) => String(student.email_lookup || '').toLowerCase() === emailMatches[0]);
} else {
  const quoted = [...rawQuery.matchAll(/[\"'“”](.{3,}?)['\"“”]/g)].map((match) => match[1].trim()).filter(Boolean);
  if (quoted.length > 1) {
    const replyText = 'يمكنني البحث عن طالب واحد فقط في الرسالة الواحدة. من فضلك أرسل اسم طالب واحد فقط أو رقمه.';
    return [{ json: { ...original, source: 'student_db', matchedKnowledge: 'student_lookup_multiple_names', replyText, replyPreview: replyText.slice(0, 150) } }];
  }

  let candidate = quoted[0] || rawQuery;
  candidate = candidate
    .replace(/(?:بيانات|معلومات|حاله|حالة|نقاط|شهاده|شهادة|حضور|حضر|نتيجه|نتيجة|اسم|رقم|الطالب|طالب|في|فعاليه|فعالية|تك داي|tech day|student|lookup|عاوز|عايز|هاتلي|اعرض|اعطني|محتاج|لو سمحت|من فضلك|هل|هو|عن|بتاع|خاصة|خاصه|للطالب|المسجل|المشارك|المشترك)/gi, ' ')
    .replace(/غرب شبرا|شرق شبرا|شبرا الخيمة|شبرا الخيمه|العبور|بنها/gi, ' ');

  const normalizedCandidate = normalizeArabic(candidate);
  const tokens = normalizedCandidate.split(' ').filter((token) => token.length > 1);

  if (tokens.length < 2) {
    const replyText = 'من فضلك أرسل الاسم الكامل للطالب أو رقم الطالب أو اسم المستخدم المرتبط به. لا أستطيع تنفيذ بحث عام أو البحث باسم أول فقط.';
    return [{ json: { ...original, source: 'student_db', matchedKnowledge: 'student_lookup_need_precise_identifier', replyText, replyPreview: replyText.slice(0, 150) } }];
  }

  const exact = pool.filter((student) => student.normalized_name === normalizedCandidate);
  if (exact.length) {
    matchedBy = 'full_name_exact';
    matches = exact;
  } else {
    matchedBy = 'full_name_partial';
    matches = pool.filter((student) => {
      const full = String(student.normalized_name || '');
      if (full.includes(normalizedCandidate) || normalizedCandidate.includes(full)) return true;
      return tokens.every((token) => full.includes(token));
    });
  }
}

if (matches.length === 0) {
  const replyText = 'لم أجد طالبًا مطابقًا بالبيانات الحالية. من فضلك أرسل الاسم الكامل بشكل أدق، أو رقم الطالب، أو اسم المستخدم المرتبط به.';
  return [{ json: { ...original, source: 'student_db', matchedKnowledge: 'student_lookup_not_found', replyText, replyPreview: replyText.slice(0, 150) } }];
}

if (matches.length > 1) {
  const previewList = matches.slice(0, 5).map((student) => `- ${student.student_name} | رقم الطالب: ${student.student_id} | الفعالية: ${student.event_name}`).join('\\n');
  const replyText = `وجدت أكثر من طالب أو أكثر من سجل مطابق، لذلك لن أرجع بيانات جماعية. من فضلك حدّد طالبًا واحدًا فقط باستخدام رقم الطالب أو اسم المستخدم المرتبط به.\\n\\nأمثلة مطابقة أولية:\\n${previewList}`;
  return [{ json: { ...original, source: 'student_db', matchedKnowledge: matches.slice(0, 5).map((student) => student.record_id).join(', '), replyText, replyPreview: replyText.slice(0, 150) } }];
}

const student = matches[0];
const event = eventsById[student.event_id] || {};
const attendanceText = student.attended === true ? 'تم تسجيل الحضور' : student.attended === false ? 'لا يوجد حضور مسجل' : 'حالة الحضور غير محددة';
const certificateText = student.certificate_blocked === true ? 'محروم من الشهادة' : student.certificate_blocked === false ? 'غير محروم من الشهادة' : 'حالة الشهادة غير محددة';
const blacklistText = student.blacklist === true ? 'موجود في القائمة السوداء' : student.blacklist === false ? 'غير موجود في القائمة السوداء' : 'حالة القائمة السوداء غير محددة';
const workshops = Array.isArray(event.workshops) ? event.workshops.slice(0, 5).map((workshop) => workshop.title).join('، ') : '';
const maskedEmail = student.email_masked || maskEmail(student.email_lookup || '');

const lines = [
  'بيانات الطالب المطلوبة:',
  `- الاسم: ${student.student_name}`,
  `- رقم الطالب: ${student.student_id}`,
  `- الفعالية: ${student.event_name}`,
  `- الإدارة التعليمية: ${student.administration || 'غير محددة'}`,
  `- المدرسة: ${student.school || 'غير محددة'}`,
  `- المجموعة: ${student.group_name || 'غير محددة'}${student.group_code ? ` (${student.group_code})` : ''}`,
  `- السنة الدراسية: ${student.grade || 'غير محددة'}`,
  `- حالة الحضور: ${attendanceText}`,
  `- النقاط: ${student.points ?? 0}`,
  `- الشهادة: ${certificateText}`,
  `- القائمة السوداء: ${blacklistText}`,
];
if (student.attendance_time) lines.push(`- وقت تسجيل الحضور: ${student.attendance_time}`);
if (maskedEmail) lines.push(`- البريد المسجل: ${maskedEmail}`);
if (student.username) lines.push(`- اسم المستخدم المرتبط: ${student.username}`);
if (event.host_school) lines.push(`- مقر الاستضافة: ${event.host_school}`);
if (workshops) lines.push(`- من ورش الفعالية: ${workshops}`);
lines.push('إذا أردت الاستعلام عن طالب آخر، أرسل اسمه الكامل أو رقمه في رسالة جديدة منفصلة.');

const replyText = lines.join('\\n');
return [{
  json: {
    ...original,
    source: 'student_db',
    matchedKnowledge: student.record_id,
    studentLookupMode: matchedBy,
    replyText,
    replyPreview: replyText.slice(0, 150)
  }
}];"""


def main() -> None:
    workflow = json.loads(WORKFLOW_PATH.read_text(encoding="utf-8"))
    nodes = workflow["nodes"]
    connections = workflow["connections"]

    for node in nodes:
        if node.get("name") == "Detect Intent":
            node["parameters"]["jsCode"] = DETECT_INTENT_CODE
        elif node.get("name") == "Switch Intent":
            node["parameters"]["numberOutputs"] = 9
            node["parameters"]["output"] = "={{ ({ empty: 0, welcome: 1, faq_about: 2, faq_contact: 3, faq_techday: 4, command_student: 5, command_techday: 6, student_lookup: 7, ai: 8 })[$json.intent] ?? 8 }}"

    existing_names = {node["name"] for node in nodes}
    if "Fetch Student Database" not in existing_names:
        nodes.append(
            {
                "parameters": {
                    "url": "https://edutech-egy.com/assets/edu-assist/techday-students-db.json",
                    "options": {"timeout": 15000},
                },
                "type": "n8n-nodes-base.httpRequest",
                "typeVersion": 4.2,
                "position": [-260, 620],
                "id": "46c194fb-d43d-4c6e-bb9d-d19689670d02",
                "name": "Fetch Student Database",
            }
        )

    if "Handle Student Lookup" not in existing_names:
        nodes.append(
            {
                "parameters": {"jsCode": STUDENT_LOOKUP_CODE},
                "type": "n8n-nodes-base.code",
                "typeVersion": 2,
                "position": [20, 620],
                "id": "e670a7b5-b328-43a0-8603-5c42e3981aa6",
                "name": "Handle Student Lookup",
            }
        )
    else:
        for node in nodes:
            if node.get("name") == "Handle Student Lookup":
                node["parameters"]["jsCode"] = STUDENT_LOOKUP_CODE

    if "Reply Student Command" not in existing_names:
        nodes.append(
            {
                "parameters": {
                    "assignments": {
                        "assignments": [
                            {
                                "id": "0f7493fd-cb37-4277-b67e-5f8d6b12cd01",
                                "name": "replyText",
                                "value": "أمر /student مخصص للاستعلام عن طالب واحد فقط في كل رسالة.\\n\\nاستخدم أحد الأشكال التالية:\\n- /student 314309\\n- /student student_314309\\n- /student آدم احمد شوقي\\n\\nمهم:\\n- لا يمكنني إرجاع قوائم جماعية للطلاب\\n- الاسم الأول فقط لا يكفي\\n- الأفضل استخدام رقم الطالب أو اسم المستخدم المرتبط",
                                "type": "string",
                            },
                            {
                                "id": "f578b455-2093-4b8a-b894-34a5c366f002",
                                "name": "source",
                                "value": "faq",
                                "type": "string",
                            },
                            {
                                "id": "7b51e98c-8a41-4fe4-bf0c-6bf4e6110e12",
                                "name": "matchedKnowledge",
                                "value": "command_student",
                                "type": "string",
                            },
                            {
                                "id": "a76444a4-e09c-4858-bf32-7c0a9f4f9504",
                                "name": "replyPreview",
                                "value": "={{ String($json.replyText || '').slice(0, 150) }}",
                                "type": "string",
                            },
                        ]
                    },
                    "options": {},
                },
                "type": "n8n-nodes-base.set",
                "typeVersion": 3.4,
                "position": [-260, 420],
                "id": "1bb8b5d5-a8a1-4c8d-9d4e-aed0bb3ea311",
                "name": "Reply Student Command",
            }
        )

    if "Reply TechDay Command" not in existing_names:
        nodes.append(
            {
                "parameters": {
                    "assignments": {
                        "assignments": [
                            {
                                "id": "49f63b82-b205-45b2-a89f-a2f9f0e68f6b",
                                "name": "replyText",
                                "value": "أمر /techday يساعدك في الأسئلة السريعة عن الفعاليات.\\n\\nالمتاح حاليًا:\\n- Tech Day غرب شبرا الخيمة\\n- Tech Day العبور\\n- Tech Day بنها\\n\\nأمثلة:\\n- /techday غرب شبرا\\n- /techday العبور\\n- /techday بنها\\n\\nويمكنك أيضًا السؤال بصيغة طبيعية مثل: ما هي ورش فعالية بنها؟",
                                "type": "string",
                            },
                            {
                                "id": "640cf5e2-0627-4991-8897-fc3239b6409b",
                                "name": "source",
                                "value": "faq",
                                "type": "string",
                            },
                            {
                                "id": "49abf886-69fd-43f8-b11d-6035fbe4a21c",
                                "name": "matchedKnowledge",
                                "value": "command_techday",
                                "type": "string",
                            },
                            {
                                "id": "3121c0d6-44b6-490d-8f30-6f7da6d49b34",
                                "name": "replyPreview",
                                "value": "={{ String($json.replyText || '').slice(0, 150) }}",
                                "type": "string",
                            },
                        ]
                    },
                    "options": {},
                },
                "type": "n8n-nodes-base.set",
                "typeVersion": 3.4,
                "position": [-260, 540],
                "id": "ba9652af-5bc0-4218-92f5-c5a4fac209e7",
                "name": "Reply TechDay Command",
            }
        )

    switch_outputs = connections["Switch Intent"]["main"]
    while len(switch_outputs) < 9:
        switch_outputs.append([])

    switch_outputs[5] = [{"node": "Reply Student Command", "type": "main", "index": 0}]
    switch_outputs[6] = [{"node": "Reply TechDay Command", "type": "main", "index": 0}]
    switch_outputs[7] = [{"node": "Fetch Student Database", "type": "main", "index": 0}]
    switch_outputs[8] = [{"node": "Fetch Knowledge Base", "type": "main", "index": 0}]

    connections["Fetch Student Database"] = {
        "main": [[{"node": "Handle Student Lookup", "type": "main", "index": 0}]]
    }
    connections["Handle Student Lookup"] = {
        "main": [[
            {"node": "Send a text message", "type": "main", "index": 0},
            {"node": "Append Log Row", "type": "main", "index": 0},
        ]]
    }
    connections["Reply Student Command"] = {
        "main": [[
            {"node": "Send a text message", "type": "main", "index": 0},
            {"node": "Append Log Row", "type": "main", "index": 0},
        ]]
    }
    connections["Reply TechDay Command"] = {
        "main": [[
            {"node": "Send a text message", "type": "main", "index": 0},
            {"node": "Append Log Row", "type": "main", "index": 0},
        ]]
    }

    WORKFLOW_PATH.write_text(
        json.dumps(workflow, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print("Workflow updated with student lookup path")


if __name__ == "__main__":
    main()
