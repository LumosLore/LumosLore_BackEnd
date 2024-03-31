from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
import os
from pdfRead import extract_text_from_pdf as extract_text_read, answer_questions
from pdfQuestion import generate_questions_with_openai, chunk_text
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

openai_api_key = os.getenv("OPENAI_API_KEY")  # Make sure this is set in your environment variables

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def upload_and_process_pdf():
    if request.method == 'POST':
        file = request.files.get('file')
        
        # Check if the post request has the file part
        if 'file' not in request.files or file.filename == '':
            return "No file part in the request or no file selected.", 400
        
        # Check if file is allowed
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
        else:
            return "Unsupported file type.", 400
        
        try:
            text = extract_text_read(filepath)
            text_chunks = chunk_text(text)
            generated_questions = generate_questions_with_openai(text_chunks, openai_api_key)

            if not generated_questions:
                return "No questions were generated from the uploaded file.", 400

            return render_template('question.html', questions=generated_questions)
        except Exception as e:
            print(f"An error occurred during file processing: {e}")
            return f"An error occurred while processing the file: {e}", 500

    return render_template('upload.html')

if __name__ == "__main__":
    app.run(debug=True)
