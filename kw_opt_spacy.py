import PyPDF2
from docx import Document
import requests
from bs4 import BeautifulSoup
import spacy
from collections import Counter

# Load the spaCy English model
nlp = spacy.load('en_core_web_sm')

def read_pdf(file_path):
    text = ""
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text

def read_word(file_path):
    doc = Document(file_path)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

def fetch_url_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        return ' '.join(p.text for p in soup.find_all('p'))
    else:
        return ""

def analyze_text(text):
    doc = nlp(text)
    words = [token.lemma_.lower() for token in doc if token.is_alpha and not token.is_stop]
    total_words = len(words)
    word_counts = Counter(words)

    #Calculate kw density
    keyword_density = {word: count / total_words * 100 for word, count in word_counts.items()}

    return keyword_density, total_words

def suggest_optimizations(keyword_density, total_words):
    # Define best practices for kw density
    best_practice_range = (1, 3)  # for example, 1% to 3%
    suggestions = {}

    for keyword, density in keyword_density.items():
        if density < best_practice_range[0]:
            suggestions[keyword] = f"Increase usage to at least {best_practice_range[0]}%."
            elif density > best_practice_range[1]:
                suggestions[keyword] = f"Reduce usage to below {best_practice_range{1}%."

    return suggestions

def process_file_or_url(source):
    if source.endswith('.pdf'):
        text = read_pdf(source)
    elif source.endswith('.docx'):
        text = read_word(source)
    elif source.startswith('http'):
        text = fetch_url_content(source)
    else:
        return "Unsupported format"

    if text:
        keyword_density, total_words = analyze_text(text)
        optimizations = suggest_optimizations(keyword_density, total_words)
        return keyword_density, optimizations
    else:
        return "No text found"
if __name__ == "__main__":
    # Example usage
    sources = [
        'example.pdf', #Replace with your pdf file
        'example.docx', #Replace with your Word file
        'https://example.com', #Replace with your URL
    ]

    for source in sources:
        print(f"Processing: {source}")
        keyword_density, optimizations = process_file_or_url(source)
        print("Keyword Density:", keyword_density)
        print("Optimization Suggestions:", optimizations)
        print()

        