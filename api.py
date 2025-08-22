from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import pdfplumber
import google.generativeai as genai
import os
import json
import logging
import re

app = FastAPI()

# การตั้งค่า Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# การตั้งค่า Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY missing")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

@app.get("/")
async def read_root():
    return {"message": "Welcome to Resume Analyzer with LLM"}

@app.post("/analyze_resume")
async def analyze_resume(
    resume_pdf: UploadFile = File(...),  # อัปโหลดไฟล์ resume.pdf
    jd_text: UploadFile = File(...)  # อัปโหลดไฟล์ JD.text
):
    try:
        # Extract text from the resume
        with pdfplumber.open(resume_pdf.file) as pdf:
            resume_text = "".join([page.extract_text() or "" for page in pdf.pages])
        if not resume_text.strip():
            return JSONResponse(content={"error": "Unable to extract text from the resume PDF"}, status_code=400)

        # Extract text from the Job Description
        jd_text_content = jd_text.file.read().decode("utf-8").strip()
        if not jd_text_content:
            return JSONResponse(content={"error": "No content found in the Job Description file"}, status_code=400)

        # แปลงเรซูเม่เป็น JSON
        parse_prompt = f"""
        แยกส่วนต่าง ๆ จากข้อความเรซูเม่นี้เป็น JSON:
        1. education (ประสบการณ์ศึกษา)
        2. skills (ทักษะ)
        3. knowledge (ความรู้)
        4. tools (เครื่องมือที่ต้องใช้)

        Parsed Resume:
        {resume_text}

        Output in JSON format:
        {{
          "education": [...],
          "skills": [...],
          "knowledge": [...],
          "tools": [...]
        }}
        ต้องตอบเป็นภาษาไทย
        """
        parse_response = model.generate_content(parse_prompt)
        parsed_resume_text = re.sub(r"^```json\s*|\s*```$", "", parse_response.text.strip())

        # Validate JSON from Resume
        try:
            parsed_resume = json.loads(parsed_resume_text)
            required_keys = {"education", "skills", "knowledge", "tools"}
            
            if not all(key in parsed_resume for key in required_keys):
                return JSONResponse(content={"error": "Resume JSON is missing required fields (education, skills, knowledge, tools)"}, status_code=400)
            
            if not all(isinstance(parsed_resume[key], list) for key in required_keys):
                return JSONResponse(content={"error": "All fields in the JSON must be lists"}, status_code=400)
                
        except json.JSONDecodeError as e:
            return JSONResponse(content={"error": f"Failed to parse JSON from the resume: {str(e)}"}, status_code=400)

        # วิเคราะห์เรซูเม่
        analyze_prompt = f"""
        วิเคราะห์ว่าเรซูเม่นี้เหมาะสมกับ Job Description ต่อไปนี้มากน้อยแค่ไหน

        Job Description:
        {jd_text_content}

        Parsed Resume:
        {json.dumps(parsed_resume, ensure_ascii=False)}

        เน้นการวิเคราะห์หมวดหมู่ต่อไปนี้: education, skills, knowledge, tools
        สำหรับแต่ละหมวดหมู่:
        - ให้คะแนน (0-100) พร้อมเหตุผลประกอบการให้คะแนนอย่างละเอียด โดยระบุจุดที่ตรงกันและจุดที่ขาดเมื่อเทียบกับความต้องการของงาน
        - ให้คำนวณ suitability_score จากค่าเฉลี่ยของคะแนนทั้ง 4 หมวดหมู่ (education, skills, knowledge, tools)
        ให้การประเมินความเหมาะสมโดยรวมของผู้สมัครตามคำอธิบายงาน

        Output in JSON format:
        {{
          "suitability_score": <คะแนน 0-100>,
          "analysis": {{
            "education": {{"score": <คะแนน 0-100>, "reasoning": "<เหตุผลประกอบการให้คะแนน>"}},
            "skills": {{"score": <คะแนน 0-100>, "reasoning": "<เหตุผลประกอบการให้คะแนน>"}},
            "knowledge": {{"score": <คะแนน 0-100>, "reasoning": "<เหตุผลประกอบการให้คะแนน>"}},
            "tools": {{"score": <คะแนน 0-100>, "reasoning": "<เหตุผลประกอบการให้คะแนน>"}}
          }},
          "strengths": ["<จุดเด่น 1>", "<จุดเด่น 2>", "..."],
          "improvements": ["<จุดที่ต้องพัฒนา 1>", "<จุดที่ต้องพัฒนา 2>", "..."],
          "summary": "<การประเมินโดยรวมตามคำอธิบายงาน>"
        }}
        ต้องตอบเป็นภาษาไทย
        """
        analyze_response = model.generate_content(analyze_prompt)
        analysis_text = re.sub(r"^```json\s*|\s*```$", "", analyze_response.text.strip())
        analysis_result = json.loads(analysis_text)

        scores = [
            analysis_result["analysis"]["education"]["score"],
            analysis_result["analysis"]["skills"]["score"],
            analysis_result["analysis"]["knowledge"]["score"],
            analysis_result["analysis"]["tools"]["score"]
        ]
        analysis_result["suitability_score"] = sum(scores) / len(scores)

        return analysis_result

    except Exception as e:
        logger.error(f"เกิดข้อผิดพลาดที่ไม่คาดคิด: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    