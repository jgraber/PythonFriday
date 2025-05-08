import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('goodreads_sentiment.csv', delimiter=',', encoding='utf-8')


# Set plot style
sns.set_style('whitegrid')


# Bubble Chart (Scatter Plot with size based on count)
rating_sentiment_counts = df.groupby(['Rating', 'Sentiment']).size().reset_index(name='Count')

plt.figure(figsize=(8, 5))
sns.scatterplot(
    data=rating_sentiment_counts,
    x='Rating',
    y='Sentiment',
    size='Count',
    sizes=(1, 2500),  # Adjust min/max bubble size
    alpha=0.6,
    edgecolor='black',
    legend=False
)

plt.xlim(df['Rating'].min() - 0.5, df['Rating'].max() + 0.5)
plt.ylim(df['Sentiment'].min() - 0.5, df['Sentiment'].max() + 0.5)

plt.title('Bubble Chart: Rating vs Sentiment (Size = Number of Reviews)')
plt.xlabel('Rating')
plt.ylabel('Sentiment')
plt.savefig('goodreads_plot1_bubble.png', bbox_inches='tight')
plt.clf()



df['Sentiment'] = df.Sentiment.astype(str)
df['Rating'] = df.Rating.astype(str)

# Barchart Sentiment to Rating
sentiment_order = ['1', '2', '3', '4', '5']
sns.countplot(data=df, x='Sentiment', 
              hue='Rating', 
              hue_order=sentiment_order, 
              order=sentiment_order, 
              palette='Set1', )
plt.title('Sentiment split into Rating')
plt.savefig('goodreads_plot2_sentiment.png', bbox_inches='tight')
plt.clf()

# Barchart Rating to Sentiment
sns.countplot(data=df, 
              x='Rating', 
              hue='Sentiment', 
              hue_order=sentiment_order, 
              order=sentiment_order, 
              palette='Set1', )
plt.title('Rating split into Sentiment')
plt.savefig('goodreads_plot3_rating.png', bbox_inches='tight')
plt.clf()

