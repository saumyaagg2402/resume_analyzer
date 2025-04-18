import spacy
import PyPDF2

class ResumeParser:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_lg")
        
    def parse_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF resume"""
        text = ""
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text()
        return text
    
    def extract_skills(self, text: str) -> set:
        """Extract skills from text using NLP"""
        doc = self.nlp(text.lower())
        skills = set()
        for token in doc:
            if token.pos_ in ["NOUN", "PROPN"]:
                skills.add(token.text)
        return skills