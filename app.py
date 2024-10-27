import streamlit as st
import pandas as pd
import joblib
from PyPDF2 import PdfReader  # Replaced fitz with PyPDF2 for PDF parsing

# Load the saved model
loaded_model = joblib.load("./resume_screening_model.pkl")

# Helper function to extract text from PDF
def extract_text_from_pdf(pdf):
    reader = PdfReader(pdf)
    text = ""
    for page in reader.pages:
        extracted_text = page.extract_text()
        if extracted_text:
            text += extracted_text
    return text

# Helper function to extract features from text
def extract_features_from_text(text):
    features = {
        "gender": 1 if "she" in text.lower() else 0,
        "african_descent": 1 if "africa" in text.lower() else 0,
        "finance_degree": 1 if "finance" in text.lower() else 0,
        "leadership_experience": 1 if "leader" in text.lower() or "manager" in text.lower() else 0,
        "extraprofessional_work": 1 if "volunteer" in text.lower() else 0,
        "analytical_skills": 1 if "modeling" in text.lower() or "statistics" in text.lower() else 0,
        "communication_skills": 1 if "presentation" in text.lower() or "public speaking" in text.lower() else 0,
    }
    return features

# Streamlit App UI
st.title("Womentor Program - Resume Screening")

st.write("Upload a PDF resume to evaluate the candidate's fit.")

# Upload resume
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    # Extract text from uploaded PDF
    resume_text = extract_text_from_pdf(uploaded_file)
    
    # Extract features from the resume text
    candidate_features = extract_features_from_text(resume_text)
    
    # Convert features to DataFrame for model prediction
    candidate_df = pd.DataFrame([candidate_features])
    
    # Predict fit score and probability
    fit_prediction = loaded_model.predict(candidate_df)[0]
    fit_probability = loaded_model.predict_proba(candidate_df)[0][1] * 100

    # Display the results
    if fit_prediction == 1:
        st.success(f"This candidate is a good fit! Probability of high fit: {fit_probability:.2f}%")
    else:
        st.warning(f"This candidate may not be a good fit. Probability of high fit: {fit_probability:.2f}%")
