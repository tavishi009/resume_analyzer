# Resume Analyzer

Upload your resume and get instant feedback — what's missing, what's weak, and what's working. Built this as a full-stack project to practice Python + Flask + frontend together.

---

## What it does

- Upload any PDF resume.
- Detects 40+ technical skills across categories like Web Dev, ML, Databases, etc.
- Checks for important sections (Projects, Experience, Skills, etc.).
- Flags weak phrases like "responsible for" or "helped with".
- Checks if email, phone, LinkedIn, and GitHub are present.
- Gives a score out of 100 with feedback on what to fix.

---

## How to run it

**1. Clone the repo and go into the folder**
```bash
git clone https://github.com/your-username/resume-analyzer.git
cd resume-analyzer
```

**2. Install dependencies**
```bash
pip install flask pymupdf
```

**3. Run the app**
```bash
python app.py
```

**4. Open your browser and go to**
```
http://127.0.0.1:5000
```

That's it. Upload a PDF resume and you'll get results in seconds.

---

## Project structure

```
resume-analyzer/
├── app.py              ← Flask server
├── analyzer.py         ← all the analysis logic
├── requirements.txt    ← dependencies
└── templates/
    └── index.html      ← frontend UI
```

---

## Tech stack

| Layer | Tool |
|---|---|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python + Flask |
| PDF Parsing | PyMuPDF |
| Database | None needed |

---

## Note

Only works with text-based PDFs. Scanned image resumes won't work since there's no OCR.

---

