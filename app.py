from dotenv import load_dotenv
import base64
import streamlit as st
import os
import io
import plotly.graph_objects as go
import pandas as pd
import pdf2image
import re
import json
from PIL import Image
import google.generativeai as genai
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet

# Load API key
load_dotenv()
genai.configure(api_key=os.getenv("google_api_key"))

# Function to get a generative response based on user input
def get_gemini_response(user_input, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([user_input, prompt])
    return response.text

# Function to process uploaded PDF resume
def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        pdf_parts = [{"mime_type": "image/jpeg", "data": base64.b64encode(img_byte_arr).decode()}]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Extract percentage score from AI response
def extract_percentage(text):
    try:
        match = re.search(r"(\d+)%", text)
        if match:
            return int(match.group(1))
        else:
            st.warning("No percentage score found in the response.")
    except ValueError:
        st.warning("Could not extract score from response.")
    return None









# Improved function to generate a PDF with ReportLab
def generate_pdf(resume_data):
    buffer = io.BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=letter)

    # Define styles
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    title_style.fontSize = 24  # Larger font for the name
    title_style.alignment = 1  # Center-align

    contact_style = styles['Normal']
    contact_style.fontSize = 12  # Smaller font for contact details
    contact_style.alignment = 1  # Center-align

    heading_style = styles['Heading2']
    body_style = styles['BodyText']

    # Content layout
    content = []

    # Adding header
    content.append(Paragraph(f"<b>{resume_data['full_name']}</b>", title_style))
    contact_details = f"Email: {resume_data['contact_email']} | Phone: {resume_data['contact_phone']}"
    content.append(Paragraph(contact_details, contact_style))
    content.append(Spacer(1, 24))  # Add space after the header

    # Adding Professional Title
    content.append(Paragraph(f"{resume_data['professional_title']}", body_style))
    content.append(Spacer(1, 12))

    # Professional Summary
    content.append(Paragraph("Professional Summary", heading_style))
    content.append(Paragraph(resume_data['professional_summary'], body_style))
    content.append(Spacer(1, 12))

    # Work Experience
    content.append(Paragraph("Work Experience", heading_style))
    for experience in resume_data['work_experience'].split("\n"):
        match = re.match(r"(.*) at (.*)", experience)  # Example format: "Software Engineer at Company X"
        if match:
            job_title, company_name = match.groups()
            content.append(Paragraph(f"<b>{company_name}</b>, {job_title}", body_style))
        else:
            content.append(Paragraph(experience, body_style))
    content.append(Spacer(1, 12))

    # Education
    content.append(Paragraph("Education", heading_style))
    for level, details in [
        ("10th Grade", resume_data['education_10th']),
        ("12th Grade", resume_data['education_12th']),
        ("Undergraduate", resume_data['ug_degree']),
        ("Postgraduate", resume_data['pg_degree'])
    ]:
        content.append(Paragraph(f"<b>{level}</b>: {details}", body_style))
    content.append(Spacer(1, 12))

    # Key Skills
    content.append(Paragraph("Key Skills", heading_style))
    skills = " | ".join(filter(None, resume_data['key_skills'].split(",")))  # Concatenate skills with "|"
    content.append(Paragraph(skills, body_style))
    content.append(Spacer(1, 12))

    # Projects
    content.append(Paragraph("Projects", heading_style))
    for project in resume_data['projects'].split("\n"):
        match = re.match(r"(.*): (.*)", project)  # Example format: "Project Title: Description"
        if match:
            title, description = match.groups()
            content.append(Paragraph(f"<b>{title}</b>: {description}", body_style))
        else:
            content.append(Paragraph(project, body_style))
    content.append(Spacer(1, 12))

    # Certifications
    content.append(Paragraph("Certifications", heading_style))
    for certification in resume_data['certifications'].split("\n"):
        match = re.match(r"(.*) by (.*)", certification)  # Example format: "Certification Name by Provider"
        if match:
            cert_title, provider = match.groups()
            content.append(Paragraph(f"- <b>{provider}</b>: {cert_title}", body_style))
        else:
            content.append(Paragraph(f"- {certification}", body_style))
    content.append(Spacer(1, 12))

    # Languages Known
    content.append(Paragraph("Languages Known", heading_style))
    content.append(Paragraph(resume_data['languages_known'], body_style))
    content.append(Spacer(1, 12))

    # Build PDF
    pdf.build(content)
    buffer.seek(0)
    return buffer.getvalue()









# Streamlit App Configuration
st.set_page_config(page_title=" SmartCV : AI Resume Builder & ATS Analyzer")
st.markdown("<h1 style='color: lavender; font-size: 36px;'>SmartCV : AI Resume Builder & ATS Analyzer</h1>", unsafe_allow_html=True)

# Tabs for different functionalities
tab1, tab2, tab3 = st.tabs(["Resume Builder", "ATS Analyzer", "Visual Analytics"])

# --- Tab 1: Resume Builder ---
with tab1:
    st.subheader("Resume Builder")
    resume_data = {
        "full_name": st.text_input("Full Name"),
        "professional_title": st.text_input("Professional Title"),
        "contact_email": st.text_input("Email Address"),
        "contact_phone": st.text_input("Phone Number"),
        "professional_summary": st.text_area("Professional Summary"),
        "work_experience": st.text_area("Work Experience"),
        "education_10th": st.text_input("10th Grade (School Name, Year)"),
        "education_12th": st.text_input("12th Grade (School Name, Year)"),
        "ug_degree": st.text_input("Undergraduate Degree"),
        "pg_degree": st.text_input("Postgraduate Degree"),
        "key_skills": st.text_area("Key Skills"),
        "projects": st.text_area("Projects"),
        "certifications": st.text_area("Certifications"),
        "languages_known": st.text_area("Languages Known"),
    }

    submit_resume = st.button("Generate Resume")
    resume_prompt = """You are a professional resume builder You are a professional resume builder. Create a customized resume using the provided information, 
    and ensure there are no grammatical or spelling errors. 
    The resume should be structured with the following sections:
    1. Full Name
    2. Professional Title
    3. Contact Information (Email Address and Phone Number)
    4. Professional Summary
    5. Work Experience (Job Title, Company Name, Employment Period) Add bullet points summarizing key responsibilities and achievements, using action verbs and technical terminology relevant to the field.
    6. Education (10th, 12th, UG, PG)
    7. Key Skills
    8. Projects (Brief descriptions including Project Title and technologies used)
    9. Certifications
    10. Languages Known
    Make sure the resume is concise, well-organized, and free from grammatical or spelling mistakes.
      Highlight the candidate's strengths based on the input."""  # Keep the full prompt as in original code

    if submit_resume:
        if resume_data["full_name"] and resume_data["professional_title"]:
            user_input = "\n".join(f"{key}: {value}" for key, value in resume_data.items())
            generated_resume = get_gemini_response(user_input, resume_prompt)
            st.subheader("Generated Resume")
            st.write(generated_resume)

            # Create a downloadable PDF resume
            pdf_data = generate_pdf(resume_data)
            st.download_button(
                label="Download Resume as PDF",
                data=pdf_data,
                file_name="generated_resume.pdf",
                mime="application/pdf"
            )
        else:
            st.write("Please fill out the required fields (Full Name and Professional Title) to generate the resume.")



# Add Tab 2 and Tab 3 from the original code without changes
# ... continue with remaining code for ATS Analyzer and Visual Analytics tabs

with tab2:
    st.subheader("ATS Analyzer")
    input_text = st.text_area("Enter the Job Description:", key="input")
    uploaded_file = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])

    submit_analysis1 = st.button("Evaluate Resume")
    submit_analysis2 = st.button("Get ATS Score")
    submit_structured_output = st.button("Generate Structured Format")

    input_prompt1 = """You are an experienced Technical Human Resource Manager. Your task is to review the provided resume against the job description. 
    Please share your professional evaluation on whether the candidate's profile aligns with the role. 
    Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
    """
    input_prompt3 = """
    You are a highly skilled ATS system. Analyze the following resume against the provided job description. 
    Please share your professional evaluation with a percentage score and provide insights into the resume's strengths and weaknesses.
    Provide a structured output that includes:
    - match_score: A percentage indicating the overall fit.
    - missing_skills: A list of skills the candidate lacks according to the job description.
    - present_skills: A list of skills the candidate possesses.
    - keyword_match: A dictionary showing the keywords from the job description matched in the resume along with their counts.
    - experience_timeline: A timeline of relevant experience related to the job description.
    Provide insights into the resume's strengths and weaknesses.
    """

    ats_analysis_result = None  # Store ATS analysis result for later use
    structured_output = {}  # Initialize structured output

    if submit_analysis1:
        try:
            pdf_parts = input_pdf_setup(uploaded_file)
            first_page_data = pdf_parts[0]["data"]
            st.image(f"data:image/jpeg;base64,{first_page_data}", use_column_width=True)

            if input_text.strip():
                evaluation_input = f"Resume: {uploaded_file.name}\nJob Description: {input_text}"
                analysis_result = get_gemini_response(evaluation_input, input_prompt1)
                st.subheader("Evaluation Result")
                st.write(analysis_result)
            else:
                st.write("Please enter a job description to evaluate the resume.")
        except Exception as e:
            st.write("Error processing the resume:", str(e))

    if submit_analysis2:
        try:
            pdf_parts = input_pdf_setup(uploaded_file)
            first_page_data = pdf_parts[0]["data"]
            st.image(f"data:image/jpeg;base64,{first_page_data}", use_column_width=True)

            if input_text.strip():
                scoring_input = f"Resume: {uploaded_file.name}\nJob Description: {input_text}"
                ats_score_result = get_gemini_response(scoring_input, input_prompt3)
                
                # Debugging line to inspect ATS score result
                st.write("Debug - ATS Score Result:", ats_score_result) 

                # Extract ATS score and other relevant data from ats_score_result
                match_score = extract_percentage(ats_score_result) or 0
                
                # Mock data for structured output; replace with actual results from ATS evaluation
                missing_skills = ["Skill A", "Skill B"]  # Example missing skills
                present_skills = ["Skill C", "Skill D"]  # Example present skills
                keyword_match = {"Keyword 1": 10, "Keyword 2": 5}  # Example keyword match
                experience_timeline = {2020: "Job A", 2021: "Job B"}  # Example experience

                # Create structured output
                structured_output = {
                    "match_score": match_score,
                    "missing_skills": missing_skills,
                    "present_skills": present_skills,
                    "keyword_match": keyword_match,
                    "experience_timeline": experience_timeline
                }

                # Display ATS score
                st.subheader("ATS Score Result")
                st.write(f"ATS Score: {match_score}%")
                
                # Store the structured output for use in Visual Analytics
                st.session_state.ats_analysis_result = structured_output
            else:
                st.write("Please enter a job description to get ATS score.")
        except Exception as e:
            st.write("Error processing the resume:", str(e))

    if submit_structured_output:
        if structured_output:
            st.subheader("Structured Output from ATS Analyzer")
            st.json(structured_output)  # Display structured output in a formatted way

# --- Tab 3: Visual Analytics ---
with tab3:
    st.subheader("Visual Analytics")

    if 'historical_ats_scores' in st.session_state:
        ats_data = pd.DataFrame({
            'Evaluation Index': list(range(1, len(st.session_state.historical_ats_scores) + 1)),
            'ATS Score': st.session_state.historical_ats_scores
        })

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=ats_data['Evaluation Index'],
            y=ats_data['ATS Score'],
            name='ATS Score',
            marker_color='indigo'
        ))
        fig.update_layout(title='ATS Scores over Time',
                          xaxis_title='Evaluation Index',
                          yaxis_title='ATS Score (%)')
        st.plotly_chart(fig)

    # Additional visual analytics based on the structured output from ATS analysis
    if 'ats_analysis_result' in st.session_state:
        result_data = st.session_state.ats_analysis_result

        # Extract relevant data
        match_score = result_data.get("match_score", 0)
        missing_skills = result_data.get("missing_skills", [])
        present_skills = result_data.get("present_skills", [])
        keyword_match = result_data.get("keyword_match", {})
        experience_timeline = result_data.get("experience_timeline", {})

        # Pie Chart for Keyword Matching
        fig_keywords = go.Figure(data=[go.Pie(labels=list(keyword_match.keys()), values=list(keyword_match.values()))])
        fig_keywords.update_layout(title='Keyword Match Distribution')
        st.plotly_chart(fig_keywords)

        # Replace Bar Graph for Skills with a Table and add a Pie Chart for Skills
        st.subheader("Skills Analysis")
        skills_table_data = {
            'Skill Type': ['Present Skills', 'Missing Skills'],
            'Count': [len(present_skills), len(missing_skills)]
        }
        skills_df = pd.DataFrame(skills_table_data)
        st.table(skills_df)  # Display the table for Skills analysis

        # Pie Chart for Skills Analysis
        fig_skills_pie = go.Figure(data=[go.Pie(
            labels=['Present Skills', 'Missing Skills'],
            values=[len(present_skills), len(missing_skills)],
            marker=dict(colors=['green', 'red'])
        )])
        fig_skills_pie.update_layout(title='Skills Present vs Missing')
        st.plotly_chart(fig_skills_pie)

        # Radar Chart for Competency Mapping
        competencies = ['Communication', 'Technical Skills', 'Teamwork', 'Problem Solving', 'Creativity']
        scores = [4, 5, 3, 4, 2]  # Example scores; these should be derived from analysis_result
        
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=scores + [scores[0]],  # Closing the radar chart
            theta=competencies + [competencies[0]],
            fill='toself',
            name='Competency Scores'
        ))
        fig_radar.update_layout(title='Competency Mapping', polar=dict(radialaxis=dict(visible=True)))
        st.plotly_chart(fig_radar)

        # Gauge for Overall Resume Fit
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=match_score,
            title={"text": "Overall Resume Fit Score"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "darkblue"},
                "steps": [
                    {"range": [0, 50], "color": "red"},
                    {"range": [50, 75], "color": "yellow"},
                    {"range": [75, 100], "color": "green"}
                ],
            }
        ))

        st.plotly_chart(fig_gauge)

        # Timeline for Experience Relevance
        st.subheader("Experience Timeline")
        for year, job in experience_timeline.items():
            st.write(f"{year}: {job}")

