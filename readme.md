# Social Media Content Analyzer

## Description
This Streamlit app analyzes social media posts for engagement, sentiment, and provides actionable suggestions for improvement. It supports:
- Text extraction from PDFs and scanned PDFs (using OCR).
- Sentiment analysis.
- Keyphrase extraction.
- Engagement suggestions using Hugging Face APIs.

## Features
- Upload files (PDFs, scanned PDFs, or images).
- Text extraction using PyMuPDF and Tesseract.
- Intelligent suggestions powered by Hugging Face models.

## Requirements
The app uses the following Python libraries:
- `streamlit`
- `pytesseract`
- `paddleocr`
- `spacy`
- `PyPDF2`
- `PyMuPDF`
- `textblob`
- `huggingface-hub`

## Usage
1. Clone the repository:
   ```bash
   git clone https://github.com/MayankAiran786/Social_media_analyzer_2.0.git
# Install the dependencies:

pip install -r requirements.txt
# Run the app:

streamlit run app.py

## Deployment
This app can be deployed on Streamlit Community Cloud or any platform supporting Python.

## Acknowledgments
Built with Streamlit and Hugging Face APIs.
