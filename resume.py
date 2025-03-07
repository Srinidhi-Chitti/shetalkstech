import re
import nltk
import docx2txt
import pdfplumber
import string
from pdfminer.high_level import extract_text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Download necessary NLTK resources
nltk.download('punkt')
nltk.download('punkt_tab')

# Predefined skill set for extraction
SKILLS_DB = [
    "Python", "Java", "C++", "Machine Learning", "Deep Learning", "Data Science", "SQL",
    "Django", "Flask", "React", "Node.js", "Docker", "Kubernetes", "AWS", "Azure", "TensorFlow",
    "PyTorch", "NLP", "Cybersecurity", "Networking", "Git", "Agile", "Scrum"
]

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = "".join(page.extract_text() or "" for page in pdf.pages)
    return text

# Function to extract text from DOCX
def extract_text_from_docx(docx_path):
    return docx2txt.process(docx_path)

# Custom function to tokenize text
def tokenize_text(text):
    return nltk.word_tokenize(text.lower())

# Function to extract names (simple approach)
def extract_name(text):
    match = re.search(r"([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)", text)
    return match.group(0) if match else None

# Function to extract email
def extract_email(text):
    match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    return match.group() if match else None

# Function to extract phone number
def extract_phone_number(text):
    match = re.search(r"\+?\d[\d -]{8,15}\d", text)
    return match.group() if match else None

# Function to extract skills
def extract_skills(text):
    text_tokens = set(tokenize_text(text))
    extracted_skills = [skill for skill in SKILLS_DB if skill.lower() in text_tokens]
    return extracted_skills

# Function to extract education details
def extract_education(text):
    EDUCATION_KEYWORDS = ["BSc", "MSc", "B.Tech", "M.Tech", "PhD", "Bachelor", "Master", "Diploma"]
    sentences = nltk.sent_tokenize(text)
    education = [sent for sent in sentences if any(word in sent for word in EDUCATION_KEYWORDS)]
    return education

# Function to match resume with job description using TF-IDF
def match_resume_with_job(resume_text, job_description):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([resume_text, job_description])
    similarity_score = cosine_similarity(tfidf_matrix)[0, 1]
    return round(similarity_score * 100, 2)

# Main function to analyze resume
def analyze_resume(resume_path, job_description=""):
    # Extract text from file
    if resume_path.endswith(".pdf"):
        text = extract_text_from_pdf(resume_path)
    elif resume_path.endswith(".docx"):
        text = extract_text_from_docx(resume_path)
    else:
        return {"error": "Unsupported file format"}

    # Extract information
    name = extract_name(text)
    email = extract_email(text)
    phone = extract_phone_number(text)
    skills = extract_skills(text)
    education = extract_education(text)
    
    # Match with job description (if provided)
    match_score = match_resume_with_job(text, job_description) if job_description else None

    return {
        "name": name,
        "email": email,
        "phone": phone,
        "skills": skills,
        "education": education,
        "match_score": match_score
    }

# Example Usage
if __name__ == "__main__":
    resume_file = r"C:\Users\Srinidhi Chitti\Downloads\Srinidhi_resume_tex (2).pdf"  # Using raw string
    job_desc = "Looking for a Python developer with Django and Machine Learning experience."

    analysis_result = analyze_resume(resume_file, job_desc)
    print(analysis_result)
