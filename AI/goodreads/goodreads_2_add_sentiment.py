import pandas as pd
from transformers import pipeline

def sentiment(review):
    review = review[:512] if len(review) > 512 else review
    result = model(review)
    label = result[0]['label']
    stars = int(label[0])
    return stars

df = pd.read_csv('goodreads_cleaned.csv', delimiter=',', encoding='utf-8')
print(df)

reviews = df['Review'].values.flatten().tolist()

model = pipeline('sentiment-analysis', model='nlptown/bert-base-multilingual-uncased-sentiment')
df['Sentiment'] = df['Review'].apply(sentiment)

print(df)

df.to_csv('goodreads_sentiment.csv', index=False, encoding='utf-8')