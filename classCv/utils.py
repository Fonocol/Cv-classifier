# classCv/utils.py

from transformers import pipeline

# Charger le pipeline de sentiment une seule fois
sentiment_pipeline = pipeline("sentiment-analysis")

def predict_sentiment(comment):
    result = sentiment_pipeline(comment)
    return result[0]  # Retourne un dictionnaire avec 'label' et 'score'
