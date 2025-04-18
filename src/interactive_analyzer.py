import os
from resume_parser import ResumeParser
from job_matcher import JobMatcher
from dotenv import load_dotenv

def display_results(results):
    print("\n=== Resume Analysis Results ===")
    print(f"\nMatch Score: {results['match_score']}%")
    
    print("\nMatching Skills:")
    for skill in results['matching_skills']:
        print(f"✓ {skill['skill']}")
        print(f"  Evidence: {skill['evidence']}")
    
    print("\nMissing Skills:")
    for skill in results['missing_skills']:
        print(f"✗ {skill['skill']}")
        print(f"  Reason: {skill['reason']}")
    
    print(f"\nDetailed Feedback:\n{results['feedback']}")

def main():
    load_dotenv()
    analyzer = ResumeParser()
    matcher = JobMatcher()

    while True:
        print("\n=== Resume Analyzer ===")
        print("1. Analyze a resume")
        print("2. Exit")
        
        choice = input("\nEnter your choice (1-2): ")
        
        if choice == "2":
            break
        elif choice == "1":
            resume_path = input("\nEnter path to resume PDF: ")
            if not os.path.exists(resume_path):
                print("Error: File not found!")
                continue
                
            print("\nEnter job description (press Enter twice when done):")
            job_description = ""
            while True:
                line = input()
                if line == "":
                    break
                job_description += line + "\n"
            
            try:
                resume_text = analyzer.parse_pdf(resume_path)
                results = matcher.calculate_match_score(resume_text, job_description)
                display_results(results)
            except Exception as e:
                print(f"Error: {str(e)}")
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()