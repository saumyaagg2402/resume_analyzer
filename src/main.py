from resume_parser import ResumeParser
from job_matcher import JobMatcher
import os
from dotenv import load_dotenv

class ResumeAnalyzer:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        if not os.getenv('OPENAI_API_KEY'):
            raise ValueError("OpenAI API key not found in environment variables")
            
        self.parser = ResumeParser()
        self.matcher = JobMatcher()
    
    def analyze(self, resume_path: str, job_description: str) -> dict:
        # Parse resume
        resume_text = self.parser.parse_pdf(resume_path)
        
        # Get AI-powered analysis
        results = self.matcher.calculate_match_score(resume_text, job_description)
        
        return results

if __name__ == "__main__":
    analyzer = ResumeAnalyzer()
    
    resume_path = "/Users/saumya/Desktop/Saumya_CV.pdf"
    job_description = """
    Role Description: Business Analysis Intern
    
    Qualifications:
    - Analytical Skills and Business Analysis
    - Communication skills
    - Business Process knowledge
    - Ability to gather Business Requirements
    - Strong problem-solving abilities
    - Attention to detail
    - Knowledge of data analysis tools
    - Business or Management degree
    """
    
    results = analyzer.analyze(resume_path, job_description)
    print(f"\nMatch Score: {results['match_score']}%")
    print(f"\nMatching Skills: {', '.join(results['matching_skills'])}")
    print(f"\nMissing Skills: {', '.join(results['missing_skills'])}")
    print(f"\nDetailed Feedback:\n{results['feedback']}")