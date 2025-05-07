import streamlit as st
import os

# Set upload directory
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

st.set_page_config(page_title="AI Brain Scan Chatbot", layout="centered")
st.title("🧠 AI Chatbot for Brain Scan Analysis")

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

    # Simulated brain scan analysis
    st.subheader("🧠 Analysis Result")
    st.info("Detected possible abnormality in frontal lobe.")

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