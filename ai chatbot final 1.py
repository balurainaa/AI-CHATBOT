import streamlit as st
import os
from datetime import date
from PIL import Image

# Set page config
st.set_page_config(page_title="AI Brain Scan Chatbot", layout="centered")

# Upload folder
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Dummy login credentials
USERNAME = "admin"
PASSWORD = "brain123"

# Session state to track login
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Login form
def login_form():
    st.title("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == USERNAME and password == PASSWORD:
            st.session_state.authenticated = True
            st.success("Login successful!")
            st.experimental_rerun()
        else:
            st.error("Incorrect username or password.")

# Main app
def brain_scan_app():
    st.title("🧠 AI Chatbot for Brain Scan Analysis")

    st.header("🧾 Patient Information")
    patient_name = st.text_input("Patient Name")
    patient_age = st.number_input("Age", min_value=0, max_value=120, value=30)
    scan_date = st.date_input("Date of Scan", value=date.today())
    scan_type = st.selectbox("Scan Type", ["MRI", "CT", "PET", "SPECT"])
    referring_physician = st.text_input("Referring Physician")

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

        with st.expander("👤 Patient Summary"):
            st.markdown(f"""
            - **Name**: {patient_name}
            - **Age**: {patient_age}
            - **Date of Scan**: {scan_date}
            - **Scan Type**: {scan_type}
            - **Referring Physician**: {referring_physician}
            """)

        with st.expander("📄 Diagnostic Report"):
            st.write(
                "Scan analysis shows mild abnormalities potentially related "
                "to early signs of neurological conditions such as Alzheimer's "
                "or minor traumatic injury."
            )

        with st.expander("💊 Medical Information"):
            st.write(
                "Abnormalities in the frontal lobe may impact decision-making, "
                "emotional control, or behavior. Conditions could include dementia, "
                "tumors, or traumatic brain injuries."
            )

        with st.expander("🗣️ Human-Understandable Explanation"):
            st.write(
                "Your scan suggests something might be affecting the part of the brain "
                "that helps you plan, make decisions, or control your emotions. "
                "It's important to talk to a doctor."
            )

        st.subheader("✅ Final Suggestion")
        st.success("Based on the scan, it's recommended to consult a neurologist for further evaluation.")

        # 3D Brain Model (Static Image as Placeholder)
        st.subheader("🧠 Brain Model Viewer (Illustrative)")
        
        # Load a placeholder brain model (use your own model images here)
        brain_image = Image.open("path_to_3d_brain_image.png")  # Replace with the actual path to your 3D model image
        st.image(brain_image, caption="3D Brain Model", use_column_width=True)

# Run app
if not st.session_state.authenticated:
    login_form()
else:
    brain_scan_app()
