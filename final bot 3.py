import streamlit as st
import os
import hashlib
from datetime import date, datetime
from fpdf import FPDF
from cryptography.fernet import Fernet
import base64

# Setup directories
os.makedirs("uploads", exist_ok=True)
os.makedirs("secure_data", exist_ok=True)

# Load/generate AES key
KEY_FILE = "secure_data/secret.key"
if not os.path.exists(KEY_FILE):
    with open(KEY_FILE, "wb") as f:
        f.write(Fernet.generate_key())
with open(KEY_FILE, "rb") as f:
    fernet = Fernet(f.read())

USER_DB = "secure_data/users.txt"

# Utility Functions
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    if not username or not password:
        return False
    if not os.path.exists(USER_DB):
        open(USER_DB, "w").close()
    with open(USER_DB, "r") as f:
        users = f.read().splitlines()
    for u in users:
        if u.split(",")[0] == username:
            return False
    with open(USER_DB, "a") as f:
        f.write(f"{username},{hash_password(password)}\n")
    return True

def authenticate_user(username, password):
    if not os.path.exists(USER_DB):
        return False
    with open(USER_DB, "r") as f:
        for line in f:
            stored_user, stored_hash = line.strip().split(",")
            if username == stored_user and hash_password(password) == stored_hash:
                return True
    return False

def encrypt_text(text):
    return fernet.encrypt(text.encode()).decode()

def decrypt_text(text):
    return fernet.decrypt(text.encode()).decode()

def save_history(username, record):
    enc = encrypt_text(record)
    with open(f"secure_data/{username}_history.txt", "a") as f:
        f.write(enc + "\n")

def get_history(username):
    path = f"secure_data/{username}_history.txt"
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        return [decrypt_text(line.strip()) for line in f.readlines()]

def create_pdf(patient_data, diagnosis, output_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, "Brain Scan Diagnostic Report", ln=True, align='C')
    pdf.ln(10)
    for k, v in patient_data.items():
        pdf.cell(200, 10, f"{k}: {v}", ln=True)
    pdf.ln(5)
    pdf.multi_cell(200, 10, f"Diagnosis:\n{diagnosis}")
    pdf.output(output_path)

# Streamlit App
st.set_page_config(page_title="Secure Brain Scan App", layout="centered")
st.title("🔒 Secure AI Brain Scan Chatbot")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = ""

menu = st.sidebar.selectbox("Menu", ["Login", "Register", "Upload & Analyze", "History", "Download Report"])

# Registration
if menu == "Register":
    st.subheader("Create Account")
    user = st.text_input("Username")
    pw = st.text_input("Password", type="password")
    if st.button("Register"):
        if register_user(user, pw):
            st.success("User registered! Please login.")
        else:
            st.error("Username already exists or invalid input.")

# Login
elif menu == "Login":
    st.subheader("Login")
    user = st.text_input("Username")
    pw = st.text_input("Password", type="password")
    if st.button("Login"):
        if authenticate_user(user, pw):
            st.session_state.authenticated = True
            st.session_state.username = user
            st.success("Logged in!")
        else:
            st.error("Invalid credentials.")

# Upload and Analyze
elif menu == "Upload & Analyze":
    if not st.session_state.authenticated:
        st.warning("Login required.")
    else:
        st.header("📤 Upload Brain Scan")
        name = st.text_input("Patient Name")
        age = st.number_input("Age", 0, 120)
        scan_date = st.date_input("Scan Date", date.today())
        scan_type = st.selectbox("Scan Type", ["MRI", "CT", "PET"])
        physician = st.text_input("Referring Physician")
        file = st.file_uploader("Upload Scan", type=["png", "jpg", "jpeg"])

        if file:
            filename = os.path.join("uploads", file.name)
            with open(filename, "wb") as f:
                f.write(file.getbuffer())
            st.image(filename, caption="Uploaded Scan", use_column_width=True)
            result = "Possible abnormality detected in the frontal lobe."
            st.success("Scan processed.")
            st.info(result)

            record = {
                "Patient Name": name,
                "Age": age,
                "Scan Date": str(scan_date),
                "Scan Type": scan_type,
                "Physician": physician,
                "Diagnosis": result,
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            save_history(st.session_state.username, str(record))
            st.success("Entry saved securely.")

# View History
elif menu == "History":
    if not st.session_state.authenticated:
        st.warning("Login required.")
    else:
        st.subheader("📜 Patient History")
        records = get_history(st.session_state.username)
        if records:
            for entry in reversed(records):
                st.json(entry)
        else:
            st.info("No history found.")

# Download Report
elif menu == "Download Report":
    if not st.session_state.authenticated:
        st.warning("Login required.")
    else:
        st.subheader("📄 Download PDF Report")
        name = st.text_input("Patient Name")
        age = st.number_input("Age", 0, 120)
        scan_date = st.date_input("Scan Date")
        scan_type = st.selectbox("Scan Type", ["MRI", "CT", "PET"])
        physician = st.text_input("Referring Physician")
        diagnosis = st.text_area("Diagnosis")

        if st.button("Generate PDF"):
            patient_info = {
                "Name": name,
                "Age": age,
                "Scan Date": str(scan_date),
                "Scan Type": scan_type,
                "Physician": physician
            }
            output_path = f"secure_data/{name.replace(' ', '_')}_report.pdf"
            create_pdf(patient_info, diagnosis, output_path)
            with open(output_path, "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
                dl_link = f'<a href="data:application/pdf;base64,{b64}" download="{name}_report.pdf">📥 Download PDF Report</a>'
                st.markdown(dl_link, unsafe_allow_html=True)
