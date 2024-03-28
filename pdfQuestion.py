
import pdfminer
from pdfminer.high_level import extract_text
import openai
import json

def extract_text_from_pdf(pdf_path):
    return extract_text(pdf_path)

def chunk_text(text, chunk_size=4000):
    """Break text into chunks without exceeding the OpenAI token limit."""
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def generate_questions_with_openai(text_chunks, openai_api_key):
    openai.api_key = openai_api_key
    questions = []

    for chunk in text_chunks:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": f"Based on the following content, generate simple yet insightful questions that a student might ask to understand the key concepts better:\n\n{chunk}"}
                ],
                max_tokens=4096
            )
            questions_chunk = response['choices'][0]['message']['content'].strip()
            questions.extend(questions_chunk.split('\n'))
        except Exception as e:
            print(f"Error generating questions for a chunk: {e}")
    return questions

def main(pdf_path, openai_api_key):
    text = extract_text_from_pdf(pdf_path)
    text_chunks = chunk_text(text)
    questions = generate_questions_with_openai(text_chunks, openai_api_key)
    
    # Save questions to a JSON file
    with open('questions.json', 'w') as json_file:
        json.dump(questions, json_file)
    print("Questions generated and saved to questions.json.")

if __name__ == "__main__":
    #PDF_PATH = "sdgp.pdf"  # Specify the PDF path
    OPENAI_API_KEY = "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"  # Use your actual OpenAI API key
    main(PDF_PATH, OPENAI_API_KEY)