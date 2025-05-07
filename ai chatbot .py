from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/scan', methods=['POST'])
def scan():
    file = request.files.get('file')
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # Placeholder for brain scan analysis
    result = "Detected possible abnormality in frontal lobe."

    return jsonify({"message": "Scan uploaded", "analysis": result})

@app.route('/report', methods=['GET'])
def report():
    # Placeholder for diagnostic report
    report_text = "The scan shows mild abnormalities that could indicate early signs of neurological issues."
    return jsonify({"report": report_text})

@app.route('/medical_info', methods=['GET'])
def medical_info():
    # Medical explanation
    info = "This condition may relate to early-stage dementia or a benign tumor."
    return jsonify({"medical_info": info})

@app.route('/human_info', methods=['GET'])
def human_info():
    # Human-readable explanation
    explanation = "There might be an issue in the brain’s front part, which affects planning and decision-making."
    return jsonify({"human_info": explanation})

@app.route('/result', methods=['GET'])
def result():
    # Final result
    final_result = "We recommend consulting a neurologist for further examination."
    return jsonify({"result": final_result})

if __name__ == '__main__':
    app.run(debug=True)