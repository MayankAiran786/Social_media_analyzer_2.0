import streamlit as st
from PIL import Image
import pytesseract
from textblob import TextBlob
import spacy
import requests
import PyPDF2
import os

# Set Hugging Face API Token as an environment variable
HUGGINGFACE_API_KEY = "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"  # Replace with your actual Hugging Face API key

def analyze_text(text):
    """Performs enhanced text analysis using spaCy."""
    try:
        nlp = spacy.load("en_core_web_sm")  # Load spaCy's small English model
        doc = nlp(text)

        # Sentiment analysis using TextBlob
        blob = TextBlob(text)
        sentiment = blob.sentiment.polarity

        # Calculate word and sentence counts
        words = len(text.split())
        sentences = len(list(doc.sents))

        # Extract key phrases
        key_phrases = [str(phrase) for phrase in doc.noun_chunks]

        # Scale sentiment score to 0.0 - 1.0
        sentiment_score = (sentiment + 1) / 2

        return {
            "word_count": words,
            "sentence_count": sentences,
            "sentiment": sentiment_score,
            "key_phrases": key_phrases,
        }
    except Exception as e:
        print(f"Error analyzing text: {e}")
        return None

def display_sentiment_bar(sentiment_score):
    """Displays a sentiment bar chart using Streamlit."""
    if 0.0 <= sentiment_score <= 1.0:
        st.progress(sentiment_score)
    else:
        st.error("Invalid sentiment score. Please check the analysis logic.")

    if sentiment_score >= 0.7:
        st.write("Sentiment: Very Positive")
    elif sentiment_score >= 0.5:
        st.write("Sentiment: Positive")
    elif sentiment_score >= 0.3:
        st.write("Sentiment: Neutral")
    elif sentiment_score >= 0.1:
        st.write("Sentiment: Negative")
    else:
        st.write("Sentiment: Very Negative")

def get_engagement_suggestions_via_huggingface(text):
    """Generates intelligent engagement suggestions using Hugging Face API."""
    if not HUGGINGFACE_API_KEY:
        st.error("Hugging Face API key is missing. Please set it as an environment variable.")
        return ["Unable to generate suggestions due to missing API key."]

    api_url = "https://api-inference.huggingface.co/models/EleutherAI/gpt-neo-2.7B"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

    prompt = (
        f"Analyze the following social media post and suggest actionable ways to improve its engagement. "
        f"Provide clear, point-wise suggestions:\n\n{text}"
    )

    payload = {"inputs": prompt}

    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()  # Check for HTTP errors
        generated_text = response.json()[0]["generated_text"]
        # Clean up the generated text for point-wise display
        suggestions = [
            suggestion.strip("- ").strip() for suggestion in generated_text.strip().split("\n") if suggestion.strip()
        ]
        return suggestions
    except requests.exceptions.RequestException as e:
        st.error(f"Error generating suggestions: {e}")
        return ["Error generating suggestions. Please try again later."]

def extract_text_from_uploaded_file(uploaded_file):
    """Extracts text from uploaded PDFs or images."""
    file_bytes = uploaded_file.read()
    if uploaded_file.type == "application/pdf":
        try:
            reader = PyPDF2.PdfReader(uploaded_file)
            text = "".join(page.extract_text() for page in reader.pages)
        except Exception as e:
            text = None
            st.error(f"Error extracting text from PDF: {e}")
    elif uploaded_file.type in ["image/jpeg", "image/png"]:
        try:
            image = Image.open(uploaded_file)
            text = pytesseract.image_to_string(image)
        except Exception as e:
            text = None
            st.error(f"Error performing OCR on image: {e}")
    else:
        text = None
        st.error("Unsupported file type.")
    return text

def main():
    st.title("Enhanced Social Media Content Analyzer")

    uploaded_file = st.file_uploader("Upload file (PDF or scanned PDF)", type=["pdf", "jpg", "jpeg", "png"])

    if uploaded_file is not None:
        extracted_text = extract_text_from_uploaded_file(uploaded_file)

        if extracted_text:
            st.text("Extracted Text:")
            st.write(extracted_text)

            analysis = analyze_text(extracted_text)
            if analysis:
                st.subheader("Text Analysis")
                st.write(f"Word Count: {analysis['word_count']}")
                st.write(f"Sentence Count: {analysis['sentence_count']}")
                display_sentiment_bar(analysis["sentiment"])

                st.subheader("Key Phrases")
                st.write(", ".join(analysis["key_phrases"]))

                st.subheader("Engagement Suggestions")
                suggestions = get_engagement_suggestions_via_huggingface(extracted_text)
                for suggestion in suggestions:
                    st.write(f"- {suggestion}")

if __name__ == "__main__":
    main()
