import fitz  # Import PyMuPDF
from transformers import pipeline
from transformers import BartForConditionalGeneration, BartTokenizer

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def preprocess_text(text):
    paragraphs = text.split('\n\n')  # Split text into paragraphs
    clean_paragraphs = [p.strip() for p in paragraphs if len(p.strip()) > 0]
    return clean_paragraphs

def generate_questions(text):
    try:
        model_name = "t5-small"  # Using a well-known and widely available model
        qg_pipeline = pipeline('text-generation', model=model_name)

        prompt = "generate question: " + text  # Prompting the model
        questions = qg_pipeline(prompt, max_length=100, num_return_sequences=1)

        # Processing the output to fit the expected format
        return [{"question": q['generated_text'].split('?')[0] + '?', "answer": "This needs manual verification."} for q in questions]
    except Exception as e:
        print(f"Error generating questions: {e}")
        return []


def main(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    paragraphs = preprocess_text(text)
    for para in paragraphs[:5]:  # Let's limit to the first 5 paragraphs for demonstration
        questions = generate_questions(para)
        for q in questions:
            print("Question:", q['question'])
            print("Answer:", q['answer'])
            print("---")

def answer_questions(text, questions):
    qa_pipeline = pipeline("question-answering")
    for question in questions:
        try:
            result = qa_pipeline(question=question, context=text)
            print(f"Question: {question}")
            print(f"Answer: {result['answer']}\n")
        except Exception as e:
            print(f"Error answering question '{question}': {e}")

# Example usage:
if __name__ == "__main__":
    pdf_path = "OOP_Concepts_PDF.pdf"
    text = extract_text_from_pdf(pdf_path)
    questions = [
        "What is Object-Oriented Programming?",
        "Describe the concept of Encapsulation.",
        "How does Inheritance work?",
        "Explain Polymorphism and its benefits."
    ]
    answer_questions(text, questions)

def convert_statements_to_questions(statements):
    tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
    model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')
    questions = []

    for statement in statements:
        inputs = tokenizer.encode("paraphrase: " + statement + " </s>", return_tensors="pt", add_special_tokens=False)
        question_encodings = model.generate(inputs, max_length=100, num_return_sequences=1)
        question = tokenizer.decode(question_encodings[0], skip_special_tokens=True)
        questions.append(question)

    return questions


# Example usage
if __name__ == "__main__":
    pdf_path = "OOP_Concepts_PDF.pdf"
    # Assume the existence of `extract_key_statements` and `extract_text_from_pdf`
    text = extract_text_from_pdf(pdf_path)
    key_statements = ["Your key statements here"]  # Placeholder
    generated_questions = convert_statements_to_questions(key_statements)

    #for question in generated_questions:
        #print("Generated Question:", question)

