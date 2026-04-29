# EDU Assist on n8n

هذا المجلد يحتوي على ملفات بداية عملية للبوت:

- `edu-assist-workflow.json`
  Workflow مطور لتيليجرام فيه:
  - `FAQ routing` للأسئلة المتكررة
  - `HTTP knowledge fetch` من ملف JSON عام
  - `AI fallback` للأسئلة التي تحتاج فهمًا أكبر
  - `logging` إلى Google Sheets

- `edu-assist-knowledge-template.csv`
  قالب معرفي لو أحببت إدارة المحتوى في Google Sheets أو أي قاعدة معرفة بسيطة.

- `edu-assist-log-template.csv`
  قالب Sheet لتسجيل الأسئلة والردود المختصرة.

## التشغيل السريع

1. ارفع الملف `assets/edu-assist/knowledge-base.json` إلى موقعك.
   المسار المتوقع في الـ workflow هو:
   `https://edutech-egy.com/assets/edu-assist/knowledge-base.json`

2. في n8n:
   - استورد `edu-assist-workflow.json`
   - اربط بيانات اعتماد Telegram
   - اربط بيانات اعتماد OpenRouter
   - اربط بيانات اعتماد Google Sheets

3. عدّل هذه القيم داخل الـ workflow:
   - `PASTE_LOG_SHEET_URL_HERE`
   - `REPLACE_WITH_YOUR_GOOGLE_SHEETS_CREDENTIAL_ID`

4. أنشئ Google Sheet للوج باسم Sheet:
   - `logs`
   واستخدم رؤوس الأعمدة الموجودة في:
   `edu-assist-log-template.csv`

## لماذا هذا التصميم أسرع؟

- الأسئلة الشائعة لا تمر على LLM أصلًا
- البرومبت أقصر من النسخة القديمة
- المعرفة الكبيرة خارج البرومبت
- يتم إرسال المقاطع المناسبة فقط عند الحاجة

## تحسينات لاحقة مقترحة

- نقل `knowledge-base.json` إلى Google Sheets أو Supabase
- إضافة `cache` للأسئلة المتكررة
- دعم أوامر Telegram مثل `/about` و `/contact` و `/techday`
- توسيع قاعدة المعرفة بملخصات القرارات 3 إلى 9
