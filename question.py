import fitz  # PyMuPDF for reading PDF
import spacy
import re
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

# Load an enhanced spaCy model (if available and downloaded)
nlp = spacy.load("en_core_web_lg")  # Change to en_core_web_lg for a more detailed model


# Function to extract text from PDF
def extract_text_from_pdf(pdf_paths):
    doc = fitz.open(pdf_paths)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

# Function to preprocess text
nlp = spacy.load("en_core_web_sm")

def preprocess_text(text):
    # Convert text to lowercase
    text = text.lower()

    # Remove non-alphanumeric characters
    text = re.sub(r'[^\w\s]','', text)

    # Remove digits
    text = re.sub(r'\d+','', text)

    # Tokenize and lemmatize using spaCy
    doc = nlp(text)
    lemmatized_text = " ".join([token.lemma_ for token in doc if not token.is_stop])

    return lemmatized_text

# Function to extract entities
def extract_text_from_pdf(pdf_path):
    # Code to extract text from PDF
    pass

# Function to preprocess text
def preprocess_text(text):
    # Code for text preprocessing
    pass # getting the correct output

# Function to extract entities
def extract_entities(text):
    doc = nlp(text)
    entities = [(ent.text.strip(), ent.label_) for ent in doc.ents]
    return entities

# Function to extract keywords using TF-IDF
def extract_keywords_tfidf(text, max_features=20, ngram_range=(1, 2)):
    vectorizer = TfidfVectorizer(max_features=max_features, ngram_range=ngram_range)
    tfidf_matrix = vectorizer.fit_transform([text])
    feature_names = np.array(vectorizer.get_feature_names_out())
    sorted_indices = np.argsort(tfidf_matrix.toarray()).flatten()[::-1]
    top_keywords = feature_names[sorted_indices][:max_features]
    return top_keywords

# Path to your PDF file
pdf_path = "OOP_Concepts_PDF.pdf"

# Extract text from PDF
extracted_text = extract_text_from_pdf(pdf_path)

# Preprocess text
preprocessed_text = preprocess_text(extracted_text)

# Extract entities and keywords
entities = extract_entities(preprocessed_text)
keywords = extract_keywords_tfidf(preprocessed_text)

# Print extracted entities and keywords
print("Extracted Entities:", entities)
print("Extracted Keywords:", keywords)


# Corrected function to enhance keywords with entities
def enhance_keywords_with_entities(keywords, entities, max_features=20):
    # Combine keywords and entities, ensuring uniqueness
    all_keywords = set(keywords)
    for entity, _ in entities:
        all_keywords.add(entity.lower())
    # Now correctly uses the provided max_features parameter
    return list(all_keywords)[:max_features]

# Extract, preprocess text, and then extract entities and keywords
extracted_text = extract_text_from_pdf(pdf_path)
preprocessed_text = preprocess_text(extracted_text)
entities = extract_entities(preprocessed_text)
keywords = extract_keywords_tfidf(preprocessed_text)

# Print extracted entities and keywords
print("Extracted Entities:", entities)
print("Extracted Keywords:", keywords)

# Enhance keywords with entities
enhanced_keywords = enhance_keywords_with_entities(keywords, entities)


# Basic function to generate questions from keywords
def generate_questions(keywords):
    questions = []
    for keyword in keywords:
        questions.append(f"What is {keyword}?")  # Simple template-based question
    return questions

# Generate and print questions
questions = generate_questions(enhanced_keywords)
for question in questions:
    print(question)



# Function to generate questions from keywords and entities
def generate_questions(keywords, entities):
    questions = []
    
    for keyword in keywords:
        questions.append(f"What is {keyword.capitalize()}?")  # Modified to capitalize the keyword
        questions.append(f"Can you elaborate on the concept of {keyword.lower()}?")  # Added another question template
        
    for entity, label in entities:
        questions.append(f"Explain {entity.title()} and its significance in {label.capitalize()}.")  # Modified to capitalize the label
        questions.append(f"Could you provide some insight into {entity.lower()} and its role in {label.lower()}?")  # Added another question template
        
    return questions

