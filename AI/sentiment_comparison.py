import time
import pandas as pd
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline
import nltk
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import torch
import torch.nn.functional as F
from transformers import logging

# Optional: suppress warnings
logging.set_verbosity_error()


# Sample review texts
reviews = [
    "This product is fantastic! I love it.",
    "Terrible quality, broke after one use.",
    "Absolutely wonderful. Highly recommend!",
    "Worst purchase I have ever made.",
    "Pretty decent, does the job.",
    "Not worth the money.",
    "Exceeded my expectations!",
    "Very disappointing experience.",
    "It's okay, not the best but not the worst.",
    "I am extremely satisfied with this.",
    "It works.",
    "It is fine.",
    "OK for the price.",
    ":-(",
    ":-)",
]


def vader(reviews):
    """
    Model 1: VADER (Valence Aware Dictionary and sEntiment Reasoner) 
    """
    # Download the necessary NLTK data
    nltk.download('vader_lexicon')

    start = time.time()
    # Initialize the Sentiment Intensity Analyzer
    sia = SentimentIntensityAnalyzer()

    pred = []
    for index, sentence in enumerate(reviews):
        sentiment_scores = sia.polarity_scores(sentence)

        if index == 0:
            print(f"VADER: \t\t {sentiment_scores}")

        if sentiment_scores['compound'] >= 0.05:
            pred.append("positive")
        elif sentiment_scores['compound'] <= -0.05:
            pred.append("negative")
        else:
            pred.append("neutral")
    
    end = time.time()
    duration = round(end - start, 4)

    return pred, duration


def distilbert(reviews):
    """
    Model 2: distilbert-base-uncased-finetuned-sst-2-english
    """    
    start = time.time()

    model = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
    results = model(reviews)
    print(f"distilbert: \t {results[0]}")

    pred = [r['label'].lower() for r in results]
    
    end = time.time()
    duration = round(end - start, 4)
    
    return pred, duration


def roberta(reviews):
    """
    Model 3: cardiffnlp/twitter-roberta-base-sentiment
    """
    start = time.time()

    model_name = "cardiffnlp/twitter-roberta-base-sentiment"
    
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)

    sentiment_pipeline = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
    results = sentiment_pipeline(reviews)
    print(f"roberta: \t {results[0]}")

    label_map = {'LABEL_0': 'negative', 'LABEL_2': 'positive'}
    pred = [label_map.get(r['label'], 'neutral') for r in results]
    
    end = time.time()
    duration = round(end - start, 4)

    return pred, duration


def roberta_latest(reviews):
    """
    Model 4: cardiffnlp/twitter-roberta-base-sentiment-latest
    """
    start = time.time()
    
    model_name = "cardiffnlp/twitter-roberta-base-sentiment-latest"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)

    # Sentiment labels
    labels = ['negative', 'neutral', 'positive']
    
    pred = []
    for index, sentence in enumerate(reviews):
        encoded_input = tokenizer(sentence, return_tensors='pt')
        with torch.no_grad():
            output = model(**encoded_input)

            if index == 1:
                print(f"roberta latest:  {output}")

            scores = F.softmax(output.logits, dim=1)
            predicted_class = torch.argmax(scores).item()
            pred.append(labels[predicted_class])

    end = time.time()
    duration = round(end - start, 4)

    return pred, duration


def bert(reviews):
    """
    Model 5: nlptown/bert-base-multilingual-uncased-sentiment    
    """

    start = time.time()

    model = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")
    results = model(reviews)
    print(f"bert: \t\t {results[0]}")

    # This model outputs star ratings: 1-2 stars = negative, 4-5 = positive, 3 = neutral
    pred = []
    for r in results:
        label = r['label']
        stars = int(label[0])
        if stars <= 2:
            pred.append('negative')
        elif stars >= 4:
            pred.append('positive')
        else:
            pred.append('neutral')
    
    end = time.time()
    duration = round(end - start, 4)

    return pred, duration


vader_result, vader_time = vader(reviews)
dist_result, dist_time = distilbert(reviews)
roberta_result, roberta_time = roberta(reviews)
roberta_latest_result, roberta_latest_time = roberta_latest(reviews)
bert_result, bert_time = bert(reviews)


# -------- Build Comparison Table --------
df = pd.DataFrame({
    "text": reviews,
    "VADER": vader_result,
    "DistilBERT": dist_result,
    "roBERTa": roberta_result,
    "roBERTa Latest": roberta_latest_result,
    "Bert": bert_result
})

# Add timing row
times = [f"{t:.4f} sec" for t in [vader_time, dist_time, roberta_time, roberta_latest_time, bert_time]]
df.loc["time used"] = [""] + times

# Print table
print(df.to_markdown(index=False))
