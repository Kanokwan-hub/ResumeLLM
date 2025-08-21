# ResumeLLM
# Resume Analyzer with LLM

โปรเจกต์นี้เป็น **FastAPI application** สำหรับวิเคราะห์ความเหมาะสมของ **Resume (PDF)** กับ **Job Description (TXT)** โดยใช้ **Google Gemini API** เพื่อแปลงข้อความใน Resume เป็น JSON และให้คะแนนความตรงกันกับ JD

---

## คุณสมบัติ

- อัปโหลดไฟล์ `resume.pdf` และ `jd.txt`
- แปลง Resume เป็น JSON: `education`, `skills`, `knowledge`, `tools`
- วิเคราะห์ความตรงกันกับ JD และให้คะแนนโดยละเอียด
- คืนค่า JSON พร้อมคะแนน, เหตุผลประกอบ, จุดเด่น และข้อปรับปรุง

---

## การติดตั้ง

```bash
# Clone repository
git clone <your-repo-url>
cd <your-repo-folder>

# สร้าง virtual environment (แนะนำ)
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# ติดตั้ง dependencies
pip install fastapi uvicorn pdfplumber google-generativeai
