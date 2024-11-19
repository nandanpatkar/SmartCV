# SmartCV: AI-Based Resume Generator and ATS Analyzer with Job Description

SmartCV is a user-friendly web application that uses AI to help users build professional resumes and analyze them against job descriptions using ATS (Applicant Tracking System) algorithms. It also offers visual analytics to highlight key insights about resume performance.

---

## 🛠️ Features

### Resume Builder
- Interactive interface to input user details like work experience, education, skills, and more.
- AI-powered customization using Google Generative AI for error-free and professional resumes.
- Download the generated resume as a PDF.

### ATS Analyzer
- Compare resumes with job descriptions using an ATS scoring system.
- Provides detailed evaluation including:
  - Overall fit score (in percentage).
  - Identifies missing and present skills.
  - Matches keywords from job descriptions with resume content.
  - Generates a structured analysis report.

### Visual Analytics
- Displays ATS score trends over time.
- Interactive visualizations including:
  - Keyword match distribution (pie chart).
  - Skills analysis (table and pie chart).
  - Competency mapping (radar chart).
  - Overall resume fit score (gauge).
- Experience timeline for job relevance insights.

---

## 🚀 Technologies Used

- **Streamlit**: For building the interactive web application.
- **Google Generative AI**: For resume content generation and ATS analysis.
- **Python Libraries**:
  - `pandas`: For data processing in analytics.
  - `plotly`: For interactive visualizations.
  - `reportlab`: For generating downloadable PDF resumes.
  - `pdf2image` & `Pillow`: For handling uploaded resume PDFs.
  - `dotenv`: For secure API key management.

---

## 🧰 Installation & Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/smartcv.git
   cd smartcv

   
## Install Dependencies: Use the requirements.txt file to set up the environment:
 pip install -r requirements.txt


##Set Up API Key:

- Obtain an API key from Google Generative AI.
- Create a .env file in the project directory and add:
  google_api_key="YOUR_API_KEY"

##Run the Application: Start the Streamlit app:
streamlit run app.py





##🖥️ How to Use
##Resume Builder:

- Navigate to the "Resume Builder" tab.
- Fill in your details in the provided fields (e.g., name, education, work experience).
- Click Generate Resume to view and download your professional resume.

##ATS Analyzer:

-Navigate to the "ATS Analyzer" tab.
-Upload your resume (PDF) and provide the job description.
-Click Evaluate Resume for qualitative analysis or Get ATS Score for a quantitative score.
-View detailed structured output or visualizations.

##Visual Analytics:

-Navigate to the "Visual Analytics" tab.
-Analyze ATS scores, keyword matches, skills, and competency insights.
-Review experience timelines and other insights.


##📂 Project Structure

smartcv/
├── app.py                # Main Streamlit application file
├── requirements.txt      # Dependencies
├── .env                  # API key (not included in repo)
├── README.md             # Project documentation
└── assets/               # Images for analytics (if applicable)


##📧 Contact
Developer: Nandan Patkar 
Email: nandanpatkar14114@gmail.com
