import re

SKILLS = {
    "Programming Languages": ["python", "java", "c++", "c", "javascript", "typescript", "kotlin", "swift", "go", "rust", "php", "ruby"],
    "Web Development": ["html", "css", "react", "angular", "vue", "node.js", "express", "django", "flask", "bootstrap", "tailwind"],
    "Databases": ["sql", "mysql", "postgresql", "mongodb", "sqlite", "firebase", "redis", "oracle"],
    "Tools & Platforms": ["git", "github", "docker", "linux", "aws", "azure", "gcp", "figma", "postman", "jira"],
    "Data & ML": ["machine learning", "deep learning", "pandas", "numpy", "tensorflow", "pytorch", "scikit-learn", "data analysis", "nlp"],
}

IMPORTANT_SECTIONS = ["education", "experience", "projects", "skills", "internship", "achievements", "certifications", "summary", "objective"]

STRONG_ACTION_WORDS = ["built", "developed", "designed", "implemented", "created", "led", "improved", "optimized", "deployed", "automated", "managed", "architected", "launched", "delivered"]

WEAK_PHRASES = ["responsible for", "worked on", "helped with", "assisted in", "was involved in", "participated in"]


def extract_text(filepath):
    import fitz
    doc = fitz.open(filepath)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text


def analyze(text):
    text_lower = text.lower()
    results = {}

    # ── 1. Skills Detection ───────────────────────────────────
    found_skills = {}
    missing_skills = {}
    for category, skills in SKILLS.items():
        found = [s for s in skills if s in text_lower]
        missing = [s for s in skills if s not in text_lower]
        found_skills[category] = found
        missing_skills[category] = missing

    results["found_skills"] = found_skills
    results["missing_skills"] = missing_skills

    # ── 2. Sections Check ─────────────────────────────────────
    found_sections = [s for s in IMPORTANT_SECTIONS if s in text_lower]
    missing_sections = [s for s in IMPORTANT_SECTIONS if s not in text_lower]
    results["found_sections"] = found_sections
    results["missing_sections"] = missing_sections

    # ── 3. Action Words ───────────────────────────────────────
    found_actions = [w for w in STRONG_ACTION_WORDS if w in text_lower]
    results["action_words"] = found_actions
    results["action_word_count"] = len(found_actions)

    # ── 4. Weak Phrases ───────────────────────────────────────
    found_weak = [p for p in WEAK_PHRASES if p in text_lower]
    results["weak_phrases"] = found_weak

    # ── 5. Word Count ─────────────────────────────────────────
    word_count = len(text.split())
    results["word_count"] = word_count

    # ── 6. Contact Info Check ─────────────────────────────────
    has_email = bool(re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text))
    has_phone = bool(re.search(r"(\+91|0)?[\s-]?[6-9]\d{9}", text))
    has_linkedin = "linkedin" in text_lower
    has_github = "github" in text_lower
    results["contact"] = {
        "email": has_email,
        "phone": has_phone,
        "linkedin": has_linkedin,
        "github": has_github,
    }

    # ── 7. Score Calculation ──────────────────────────────────
    score = 0

    total_found_skills = sum(len(v) for v in found_skills.values())
    score += min(total_found_skills * 3, 30)

    score += len(found_sections) * 4

    score += min(len(found_actions) * 3, 15)

    score -= len(found_weak) * 3

    if has_email: score += 5
    if has_phone: score += 5
    if has_linkedin: score += 5
    if has_github: score += 5

    if 300 <= word_count <= 800:
        score += 10
    elif word_count < 300:
        score += 3

    score = max(0, min(score, 100))
    results["score"] = score

    # ── 8. Feedback ───────────────────────────────────────────
    feedback = []

    if not has_email:
        feedback.append({"type": "error", "msg": "No email address found. Add your email."})
    if not has_phone:
        feedback.append({"type": "error", "msg": "No phone number found. Add your contact number."})
    if not has_linkedin:
        feedback.append({"type": "warning", "msg": "LinkedIn profile not mentioned. Add your LinkedIn URL."})
    if not has_github:
        feedback.append({"type": "warning", "msg": "GitHub profile not mentioned. Recruiters love seeing your code."})
    if "projects" not in text_lower:
        feedback.append({"type": "error", "msg": "No Projects section found. This is the most important section for freshers."})
    if "experience" not in text_lower and "internship" not in text_lower:
        feedback.append({"type": "warning", "msg": "No Experience/Internship section. Add any internships or part-time work."})
    if len(found_actions) < 3:
        feedback.append({"type": "warning", "msg": "Too few action words. Use words like 'Built', 'Developed', 'Designed' to describe your work."})
    if found_weak:
        feedback.append({"type": "warning", "msg": f"Weak phrases found: {', '.join(found_weak)}. Replace with strong action words."})
    if word_count < 300:
        feedback.append({"type": "warning", "msg": f"Resume seems too short ({word_count} words). Add more detail to your projects and experience."})
    if word_count > 800:
        feedback.append({"type": "info", "msg": f"Resume is quite long ({word_count} words). Try to keep it under 1 page for freshers."})
    if total_found_skills < 5:
        feedback.append({"type": "error", "msg": "Very few technical skills detected. Make sure you have a clear Skills section."})

    if score >= 80:
        feedback.insert(0, {"type": "success", "msg": "Strong resume! Just a few tweaks and you're good to go."})
    elif score >= 60:
        feedback.insert(0, {"type": "info", "msg": "Decent resume. Work on the suggestions below to make it stronger."})
    else:
        feedback.insert(0, {"type": "warning", "msg": "Your resume needs some work. Follow the suggestions below carefully."})

    results["feedback"] = feedback
    return results
