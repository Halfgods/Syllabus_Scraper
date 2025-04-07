from flask import Flask, render_template, request
import os
import fitz  # PyMuPDF

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    extracted_text = ""
    if request.method == 'POST':
        pdf = request.files['pdf']
        if pdf:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], pdf.filename)
            pdf.save(filepath)

            extracted_text = extract_semester_table(filepath)

    return render_template('index.html', extracted_text=extracted_text)

def extract_semester_table(filepath):
    doc = fitz.open(filepath)
    full_text = ""
    for page in doc:
        text = page.get_text()
        if "SEMESTERWISE CURRICULUM STRUCTURE" in text:
            full_text += text
    return full_text or "Table not found 🫠"

if __name__ == '__main__':
    app.run(debug=True)
