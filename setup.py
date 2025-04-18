from setuptools import setup, find_packages

setup(
    name="resume_analyzer",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "streamlit",
        "python-dotenv",
        "PyPDF2",
        "spacy",
        "openai",
        "scikit-learn",
    ],
)