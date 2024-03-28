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

        # Retrieve file from form
        file = request.files.get('file')
        if not file:
            # If no file is provided, return an error or redirect
            return "No file uploaded.", 400

        # Process the uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Extract text and generate questions
        try:
            text = extract_text_read(filepath)
            text_chunks = chunk_text(text)
            generated_questions = generate_questions_with_openai(text_chunks, openai_api_key)

            # Check if questions were successfully generated
            if not generated_questions:
                return "No questions were generated from the uploaded file.", 400

            # Pass the questions to your template
            return render_template('question.html', questions=generated_questions)

        except Exception as e:
            # Handle exceptions and return an error message
            print(f"An error occurred: {e}")
            return f"An error occurred while processing the file: {e}", 500

    # For GET requests or if no file was posted, show the upload form
    return render_template('upload.html')
if __name__ == "__main__":
    app.run(debug=True)
