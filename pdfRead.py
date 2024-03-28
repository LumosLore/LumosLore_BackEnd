import fitz  # PyMuPDF
from transformers import pipeline

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def answer_questions(text, questions):
    qa_pipeline = pipeline("question-answering")
    answers = []
    for question in questions:
        try:
            result = qa_pipeline(question=question, context=text)
            answers.append((question, result['answer']))
        except Exception as e:
            print(f"Error answering question '{question}': {e}")
    return answers

# Example usage within Flask app:
# pdf_path = "path/to/your/uploaded/file.pdf"
# text = extract_text_from_pdf(pdf_path)
# questions = ["Your", "questions", "here"]
# answers = answer_questions(text, questions)
