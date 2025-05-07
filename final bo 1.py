import streamlit as st
import os
from datetime import date
import hashlib
from PIL import Image

# Set page config
st.set_page_config(page_title="AI Brain Scan Chatbot", layout="centered")

# Upload folder
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# File paths
USER_FILE = "users.txt"  # Stores usernames and hashed passwords
PATIENT_HISTORY_FILE = "patient_history.txt"  # Stores patient scan history

# Function to load existing users from the file
def load_users():
    users = {}
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as file:
            for line in file:
                username, hashed_password = line.strip().split(":")
                users[username] = hashed_password
    return users

# Function to register new users with hashed passwords
def register_user(username, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    with open(USER_FILE, "a") as file:
        file.write(f"{username}:{hashed_password}\n")

# Function to validate password with SHA-256 hashing
def validate_password(stored_hash, password):
    return stored_hash == hashlib.sha256(password.encode()).hexdigest()

# Function to save patient history
def save_patient_history(patient_name, patient_age, scan_date, scan_type, referring_physician, analysis_result):
    with open(PATIENT_HISTORY_FILE, "a") as file:
        file.write(f"{patient_name},{patient_age},{scan_date},{scan_type},{referring_physician},{analysis_result}\n")

# Session state to track login
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Login form
def login_form():
    st.title("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        users = load_users()
        if username in users and validate_password(users[username], password):
            st.session_state.authenticated = True
            st.success("Login successful!")
            st.experimental_rerun()  # Refresh the page after login
        else:
            st.error("Incorrect username or password.")
    if st.button("Go to Registration Page"):
        st.session_state.authenticated = False
        st.session_state.page_mode = "register"
        st.experimental_rerun()

# Registration form
def registration_form():
    st.title("🔑 Register New Account")
    username = st.text_input("Choose a Username")
    password = st.text_input("Choose a Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Register"):
        if password != confirm_password:
            st.error("Passwords do not match!")
        else:
            users = load_users()
            if username in users:
                st.error("Username already exists. Please choose another one.")
            else:
                register_user(username, password)
                st.success("Account created successfully! Please login.")
                st.session_state.page_mode = "login"
                st.session_state.authenticated = False

# Main app (brain scan analysis)
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

        # Simulated brain scan analysis
        analysis_result = "Detected possible abnormality in frontal lobe."
        st.markdown("---")
        st.subheader("🧠 Analysis Result")
        st.info(analysis_result)

        # Patient history saving
        save_patient_history(patient_name, patient_age, scan_date, scan_type, referring_physician, analysis_result)

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
            st.write(
                "Scan analysis shows mild abnormalities potentially related "
                "to early signs of neurological conditions such as Alzheimer's "
                "or minor traumatic injury."
            )

        # Medical Information
        with st.expander("💊 Medical Information"):
            st.write(
                "Abnormalities in the frontal lobe may impact decision-making, "
                "emotional control, or behavior. Conditions could include dementia, "
                "tumors, or traumatic brain injuries."
            )

        # Human Explanation
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

# Display the patient history
def display_patient_history():
    st.title("📜 Patient Scan History")

    if os.path.exists(PATIENT_HISTORY_FILE):
        with open(PATIENT_HISTORY_FILE, "r") as file:
            st.write("### Previous Patient Scans")
            for line in file:
                patient_data = line.strip().split(",")
                st.write(f"**Name**: {patient_data[0]} | **Age**: {patient_data[1]} | **Scan Date**: {patient_data[2]} | **Scan Type**: {patient_data[3]} | **Referring Physician**: {patient_data[4]}")
                st.write(f"**Analysis Result**: {patient_data[5]}")
                st.markdown("---")
    else:
        st.write("No scan history found.")

# Run app
if "page_mode" not in st.session_state:
    st.session_state.page_mode = "login"

if not st.session_state.authenticated:
    if st.session_state.page_mode == "login":
        login_form()
    elif st.session_state.page_mode == "register":
        registration_form()
else:
    app_mode = st.sidebar.selectbox("Select App Mode", ["Brain Scan Analysis", "Patient Scan History"])
    if app_mode == "Brain Scan Analysis":
        brain_scan_app()
    elif app_mode == "Patient Scan History":
        display_patient_history()
