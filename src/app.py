import streamlit as st
import os
from resume_parser import ResumeParser
from job_matcher import JobMatcher
from dotenv import load_dotenv
from setup import download_spacy_model

def init_app():
    # Download spaCy model if needed
    download_spacy_model()
    
    # Load environment variables
    load_dotenv()
    
    # Set page config
    st.set_page_config(
        page_title="Resume Analyzer",
        page_icon="📝",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
    st.markdown("""
        <style>
        .stProgress > div > div > div > div {
            background-color: #00cc00;
        }
        .css-1v0mbdj.e115fcil1 {
            border: 1px solid #ddd;
            padding: 20px;
            border-radius: 5px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Add title and description
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("🤖 AI Resume Analyzer")
        st.markdown("""
        Upload your resume and job description to get an AI-powered analysis of the match.
        Our system will:
        - 📊 Calculate match score
        - ✨ Identify matching skills
        - 🎯 List missing qualifications
        - 💡 Provide detailed feedback
        """)

def analyze_resume(resume_file, job_description):
    # Save uploaded file temporarily
    temp_path = f"temp_{resume_file.name}"
    with open(temp_path, "wb") as f:
        f.write(resume_file.getvalue())
    
    try:
        # Analyze resume
        analyzer = ResumeParser()
        matcher = JobMatcher()
        
        resume_text = analyzer.parse_pdf(temp_path)
        results = matcher.calculate_match_score(resume_text, job_description)
        
        # Remove temporary file
        os.remove(temp_path)
        return results
    except Exception as e:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise e

def display_results(results):
    # Create tabs for different sections
    tab1, tab2, tab3 = st.tabs(["Match Score", "Skills Analysis", "Detailed Feedback"])
    
    with tab1:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(f"### Overall Match")
            st.progress(results['match_score'] / 100)
            st.metric("Match Score", f"{results['match_score']}%")
    
    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("✅ Matching Skills")
            for skill in results['matching_skills']:
                with st.expander(f"**{skill['skill']}**"):
                    st.info(f"*Evidence:* {skill['evidence']}")
        
        with col2:
            st.subheader("❌ Missing Skills")
            for skill in results['missing_skills']:
                with st.expander(f"**{skill['skill']}**"):
                    st.warning(f"*Reason:* {skill['reason']}")
    
    with tab3:
        st.markdown("### 📋 Detailed Feedback")
        st.markdown(results['feedback'])

def main():
    init_app()
    
    # File uploader for resume
    resume_file = st.file_uploader("Upload Resume (PDF)", type=['pdf'])
    
    # Text area for job description
    job_description = st.text_area(
        "Enter Job Description",
        height=200,
        placeholder="Paste the job description here..."
    )
    
    # Analyze button
    if st.button("Analyze Resume"):
        if resume_file is None:
            st.error("Please upload a resume file")
            return
        if not job_description:
            st.error("Please enter a job description")
            return
        
        with st.spinner("Analyzing resume..."):
            try:
                results = analyze_resume(resume_file, job_description)
                display_results(results)
            except Exception as e:
                st.error(f"Error analyzing resume: {str(e)}")

if __name__ == "__main__":
    main()