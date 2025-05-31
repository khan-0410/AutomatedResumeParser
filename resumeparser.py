import spacy
import pdfplumber
import re

nlp = spacy.load("en_core_web_sm")

def extract_resume_data(pdf_path):
    text = ''
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()

    doc = nlp(text)

    name = None
    for ent in doc.ents:
        if ent.label_ == 'PERSON':
            name = ent.text
            break

    email = re.findall(r'\S+@\S+', text)
    phone = re.findall(r'\+?\d[\d\s-]{8,}\d', text)
    skills = extract_skills(text)
    education = extract_education(text)

    return {
        "Name": name,
        "Email": email[0] if email else None,
        "Phone": phone[0] if phone else None,
        "Skills": skills,
        "Education": education
    }

def extract_skills(text):
    keywords = ['python', 'java', 'sql', 'machine learning', 'flask', 'excel', 'communication']
    found = [kw for kw in keywords if kw.lower() in text.lower()]
    return list(set(found))

def extract_education(text):
    edu_keywords = ['B.Tech', 'M.Tech', 'B.Sc', 'M.Sc', 'B.E', 'M.E', 'Bachelor', 'Master', 'Engineering']
    found = [kw for kw in edu_keywords if kw.lower() in text.lower()]
    return list(set(found))
