import streamlit as st
import os
from datetime import date
import plotly.graph_objects as go

# Hardcoded credentials (for demo)
USERNAME = "admin"
PASSWORD = "brain123"

# Set upload directory
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Session state for login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    st.set_page_config(page_title="Login | AI Brain Chatbot", layout="centered")
    st.title("🔐 Login to AI Brain Scan Chatbot")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == USERNAME and password == PASSWORD:
            st.session_state.logged_in = True
            st.success("Login successful! Redirecting...")
            st.experimental_rerun()
        else:
            st.error("Invalid username or password.")

# Show login if not logged in
if not st.session_state.logged_in:
    login()
    st.stop()

# Main Application
st.set_page_config(page_title="AI Brain Scan Chatbot", layout="centered")
st.title("🧠 AI Chatbot for Brain Scan Analysis")

# Patient Info
st.header("🧾 Patient Information")
patient_name = st.text_input("Patient Name")
patient_age = st.number_input("Age", min_value=0, max_value=120, value=30)
scan_date = st.date_input("Date of Scan", value=date.today())
scan_type = st.selectbox("Scan Type", ["MRI", "CT", "PET", "SPECT"])
referring_physician = st.text_input("Referring Physician")

# Upload Scan
st.header("📤 Upload Brain Scan")
uploaded_file = st.file_uploader("Upload a brain scan image (e.g., MRI, CT)", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    filename = uploaded_file.name
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    with open(filepath, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("✅ Scan uploaded successfully!")
    st.image(filepath, caption="Uploaded Brain Scan", use_column_width=True)

    st.markdown("---")
    st.subheader("🧠 Analysis Result")
    st.info("Detected possible abnormality in frontal lobe.")

    # Patient summary
    with st.expander("👤 Patient Summary"):
        st.markdown(f"""
        - **Name**: {patient_name}
        - **Age**: {patient_age}
        - **Date of Scan**: {scan_date}
        - **Scan Type**: {scan_type}
        - **Referring Physician**: {referring_physician}
        """)

    # Diagnostic Report
    with st.expander("📄 Diagnostic Report"):
        report_text = (
            "Scan analysis shows mild abnormalities potentially related "
            "to early signs of neurological conditions such as Alzheimer's "
            "or minor traumatic injury."
        )
        st.write(report_text)

    # Medical Information
    with st.expander("💊 Medical Information"):
        medical_info = (
            "Abnormalities in the frontal lobe may impact decision-making, "
            "emotional control, or behavior. Conditions could include dementia, "
            "tumors, or traumatic brain injuries."
        )
        st.write(medical_info)

    # Human Explanation
    with st.expander("🗣️ Human-Understandable Explanation"):
        human_info = (
            "Your scan suggests something might be affecting the part of the brain "
            "that helps you plan, make decisions, or control your emotions. "
            "It's important to talk to a doctor."
        )
        st.write(human_info)

    # Final Result
    st.subheader("✅ Final Suggestion")
    st.success("Based on the scan, it's recommended to consult a neurologist for further evaluation.")

    # 3D Brain Model Viewer
    st.subheader("🧠 3D Brain Model Viewer (Illustrative)")
    fig = go.Figure(data=go.Mesh3d(
        x=[0, 0, 1, 1, 0, 0, 1, 1],
        y=[0, 1, 1, 0, 0, 1, 1, 0],
        z=[0, 0, 0, 0, 1, 1, 1, 1],
        i=[0, 0, 0, 1, 1, 2, 2, 3, 4, 4, 5, 6],
        j=[1, 2, 3, 2, 3, 3, 0, 0, 5, 6, 6, 7],
        k=[2, 3, 0, 3, 0, 0, 1, 1, 6, 7, 7, 4],
        color='lightblue',
        opacity=0.5,
    ))
    fig.update_layout(
        margin=dict(l=0, r=0, b=0, t=0),
        scene=dict(
            xaxis_title='X',
            yaxis_title='Y',
            zaxis_title='Z',
            aspectratio=dict(x=1, y=1, z=1)
        )
    )
    st.plotly_chart(fig, use_container_width=True)