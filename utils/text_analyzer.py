from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.sentiment import SentimentIntensityAnalyzer

def analyze_text(text):
    """Performs basic text analysis."""
    try:
        # Tokenize text
        words = word_tokenize(text)
        sentences = sent_tokenize(text)

        # Calculate word and sentence counts
        word_count = len(words)
        sentence_count = len(sentences)

        # Sentiment analysis (using VADER)
        sia = SentimentIntensityAnalyzer()
        sentiment = sia.polarity_scores(text)

        return {
            "word_count": word_count,
            "sentence_count": sentence_count,
            "sentiment": sentiment,
        }
    except Exception as e:
        print(f"Error analyzing text: {e}")
        return None