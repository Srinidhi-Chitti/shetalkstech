import requests
import re
import nltk
import docx2txt
import pdfplumber
from pdfminer.high_level import extract_text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('punkt')

# Predefined skill set for extraction
SKILLS_DB = [
    "Python", "Java", "C++", "Machine Learning", "Deep Learning", "Data Science", "SQL",
    "Django", "Flask", "React", "Node.js", "Docker", "Kubernetes", "AWS", "Azure", "TensorFlow",
    "PyTorch", "NLP", "Cybersecurity", "Networking", "Git", "Agile", "Scrum"
]

# Extract text from resume

def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = "".join(page.extract_text() or "" for page in pdf.pages)
    return text

def extract_text_from_docx(docx_path):
    return docx2txt.process(docx_path)

def tokenize_text(text):
    return nltk.word_tokenize(text.lower())

def extract_name(text):
    match = re.search(r"([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)", text)
    return match.group(0) if match else "Unknown"

def extract_email(text):
    match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    return match.group() if match else "Not found"

def extract_phone_number(text):
    match = re.search(r"\+?\d[\d -]{8,15}\d", text)
    return match.group() if match else "Not found"

def extract_skills(text):
    text_tokens = set(tokenize_text(text))
    return [skill for skill in SKILLS_DB if skill.lower() in text_tokens]

def extract_education(text):
    EDUCATION_KEYWORDS = ["BSc", "MSc", "B.Tech", "M.Tech", "PhD", "Bachelor", "Master", "Diploma"]
    sentences = nltk.sent_tokenize(text)
    return [sent for sent in sentences if any(word in sent for word in EDUCATION_KEYWORDS)]

def match_resume_with_job(resume_text, job_description):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([resume_text, job_description])
    return round(cosine_similarity(tfidf_matrix)[0, 1] * 100, 2)

def get_roadmap(role):
    role_slug = role.lower().replace(" ", "-")
    url = f"https://roadmap.sh/api/roadmaps/{role_slug}.json"
    response = requests.get(url)
    if response.status_code == 200:
        return url  # Returning roadmap link
    else:
        return "Roadmap not available for this role"

def get_suggested_courses(missing_skills):
    return {skill: f"https://www.coursera.org/search?query={skill}" for skill in missing_skills}

def analyze_resume(resume_path, job_role):
    if resume_path.endswith(".pdf"):
        text = extract_text_from_pdf(resume_path)
    elif resume_path.endswith(".docx"):
        text = extract_text_from_docx(resume_path)
    else:
        return {"error": "Unsupported file format"}
    
    name = extract_name(text)
    email = extract_email(text)
    phone = extract_phone_number(text)
    skills = extract_skills(text)
    education = extract_education(text)
    match_score = match_resume_with_job(text, job_role)
    roadmap_link = get_roadmap(job_role)
    missing_skills = list(set(SKILLS_DB) - set(skills))
    suggested_courses = get_suggested_courses(missing_skills)
    
    return {
        "name": name,
        "email": email,
        "phone": phone,
        "skills": skills,
        "education": education,
        "match_score": match_score,
        "roadmap": roadmap_link,
        "missing_skills": missing_skills,
        "suggested_courses": suggested_courses
    }

if __name__ == "__main__":
    job_role = input("What role are you applying for? ")
    resume_file = "C:/Users/Srinidhi Chitti/Downloads/Srinidhi_resume_tex (2).pdf"
    result = analyze_resume(resume_file, job_role)
    print("\nExtraction:")
    print(result)