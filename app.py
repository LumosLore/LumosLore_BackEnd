# app.py
from flask import Flask, request, render_template, redirect
from werkzeug.utils import secure_filename
import os
from pdfRead import extract_text_from_pdf as extract_text_read, answer_questions
from pdfQuestion import generate_questions_with_openai, chunk_text

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
openai_api_key = "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"  # Replace with your actual OpenAI API key

@app.route('/', methods=['GET', 'POST'])
def upload_and_process_pdf():
    if request.method == 'POST':
        # Ensure the uploads folder exists
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])

        file = request.files.get('file')
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Process the uploaded file
            text = extract_text_read(filepath)
            text_chunks = chunk_text(text)
            generated_questions = generate_questions_with_openai(text_chunks, openai_api_key)
            qa_pairs = answer_questions(text, generated_questions)
            
            # Pass the questions and answers to your template
            return render_template('question.html', qa_pairs=qa_pairs)

    return render_template('upload.html')  # Your file upload form

if __name__ == "__main__":
    app.run(debug=True)
