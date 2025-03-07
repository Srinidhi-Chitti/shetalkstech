import re
import nltk
import docx2txt
import pdfplumber
from pdfminer.high_level import extract_text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Download necessary NLTK resources
nltk.download('punkt')

# Predefined skill set and corresponding job roles
SKILLS_DB = {
    "Python": "Python Developer",
    "Java": "Java Developer",
    "C++": "Software Engineer",
    "Machine Learning": "Machine Learning Engineer",
    "Deep Learning": "AI Engineer",
    "Data Science": "Data Scientist",
    "SQL": "Database Administrator",
    "Django": "Django Developer",
    "Flask": "Backend Developer",
    "React": "Frontend Developer",
    "Node.js": "Full Stack Developer",
    "Docker": "DevOps Engineer",
    "Kubernetes": "Cloud Engineer",
    "AWS": "Cloud Solutions Architect",
    "Azure": "Cloud Engineer",
    "TensorFlow": "AI Engineer",
    "PyTorch": "AI Engineer",
    "NLP": "NLP Engineer",
    "Cybersecurity": "Cybersecurity Analyst",
    "Networking": "Network Engineer",
    "Git": "Software Developer",
    "Agile": "Project Manager",
    "Scrum": "Scrum Master"
}

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = "".join(page.extract_text() or "" for page in pdf.pages)
    return text

# Function to extract text from DOCX
def extract_text_from_docx(docx_path):
    return docx2txt.process(docx_path)

# Function to extract skills
def extract_skills(text):
    text_tokens = set(nltk.word_tokenize(text.lower()))
    extracted_skills = [skill for skill in SKILLS_DB if skill.lower() in text_tokens]
    return extracted_skills

# Function to suggest a job role based on extracted skills
def suggest_job_role(skills):
    job_roles = [SKILLS_DB[skill] for skill in skills if skill in SKILLS_DB]
    return max(set(job_roles), key=job_roles.count) if job_roles else "No matching role found"

# Main function to analyze resume
def analyze_resume(resume_path):
    # Extract text from file
    if resume_path.endswith(".pdf"):
        text = extract_text_from_pdf(resume_path)
    elif resume_path.endswith(".docx"):
        text = extract_text_from_docx(resume_path)
    else:
        return {"error": "Unsupported file format"}

    # Extract skills and suggest job role
    skills = extract_skills(text)
    suggested_role = suggest_job_role(skills)

    return {
        "skills": skills,
        "suggested_role": suggested_role
    }

# Example Usage
if __name__ == "__main__":
    resume_file = r"C:\\Users\\Srinidhi Chitti\\Downloads\\Srinidhi_resume_tex (2).pdf"
    analysis_result = analyze_resume(resume_file)
    print(analysis_result)
