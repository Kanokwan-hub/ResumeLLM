# Resume Analyzer with LLM

**โจทย์**
บริษัทต้องการพัฒนาเครื่องมือในการวิเคราะห์ Resume ของผู้สมัครว่าตรงกับตำแหน่งงานที่มองหาไว้หรือไม่  
- Resume เป็น **PDF เท่านั้น**  
- JD ใช้ตำแหน่งงานที่สมัครเข้ามาคือ **AI & Data Solution Intern**  
- สิ่งที่ต้องวิเคราะห์ ประกอบด้วย  
  - ประสบการณ์ศึกษา  
  - ทักษะ  
  - ความรู้  
  - เครื่องมือที่ต้องใช้งาน  
- ส่งผลออกมาเป็น **คะแนน** และ **ผลการวิเคราะห์พร้อมเหตุผลของคะแนน**  
- ต้องมีการใช้ **LLM** ในการประมวลผล (สามารถเลือก Gemini, OpenAI หรืออื่น ๆ ได้)  
- เขียนด้วย **Python** หากทำในรูปแบบ **API (FastAPI)** จะได้คะแนนพิเศษ  
- ผลการวิเคราะห์คืนค่าเป็น **JSON** (สามารถกำหนดโครงสร้างเองได้)  

## Main Features
- รองรับการอัปโหลด **Resume (PDF)** และ **Job Description (txt)**  
- ใช้ **LLM (Gemini API)** เพื่อแปลงและวิเคราะห์ข้อมูล  
- คำนวณคะแนนความเหมาะสม (0-100) ของผู้สมัครกับ JD  
- ส่งคืนผลลัพธ์เป็น **JSON** ที่มีรายละเอียดทั้งคะแนน, เหตุผล, จุดแข็ง, ข้อปรับปรุง และ สรุปผล  

## Files Structure
```bash
ResumeLLM/
│── README.md # เอกสารประกอบโปรเจกต์
│── api.py # ไฟล์หลักสำหรับ FastAPI
│── Resume.pdf # ไฟล์ resume สำหรับทดสอบ
│── JD.txt # ไฟล์ JD สำหรับทดสอบ
│── requirements.txt # รายการ dependencies
```
## Installation
### 1. Clone Repository
```bash
git clone https://github.com/your-username/ResumeLLM.git
cd ResumeLLM
```
### 2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows

pip install -r requirements.txt
```
### 3. ตั้งค่า Environment Variable
```bash
export GEMINI_API_KEY="your_api_key_here"   # macOS / Linux
set GEMINI_API_KEY="your_api_key_here"      # Windows
```
### 4. รัน FastAPI Server
```bash
uvicorn main:app --reload
```
Server จะรันที่:  
http://127.0.0.1:8000/ (root)  
http://127.0.0.1:8000/docs (Swagger UI ทดสอบ API)

## การใช้งาน API
**Endpoint:**
POST /analyze_resume
**Parameters:**
- resume_pdf: Resume ของผู้สมัคร (PDF)
- jd_text: JD ของตำแหน่งงาน (txt)

