"""
FAQ Bot based on the course "Python Chatbot Bootcamp with Pandas, NumPy and SciKit"
https://mammothclub.com/course-learn/python-chatbot-bootcamp-with-pandas-numpy-and-scikit
"""

import pandas
import numpy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load the FAQ data
df = pandas.read_csv("faq.csv")
print(df)
df.dropna(inplace=True)

# Initialize the vectorizer and fit it to the questions and answers
vectorizer = TfidfVectorizer()
vectorizer.fit(numpy.concatenate((df.Question,
                                  df.Answer)))

# Embed the questions into a vectorized format
vectorized_questions = vectorizer.transform(df.Question)
print(vectorized_questions)

print("FAQ Bot is ready. Type your question or 'exit' to quit.")
while True:
    user_input = input("Question? ")
    if user_input.lower() == 'exit':
        print("Exiting the chat. Goodbye!")
        break
    print(user_input)

    # Vectorize the user input and compute similarities with the questions
    vectorized_input = vectorizer.transform([user_input])
    similarities = cosine_similarity(vectorized_input, vectorized_questions)

    # Find the closest question based on cosine similarity
    closest_question = numpy.argmax(similarities,
                                    axis=1)

    print("Similarities: ", similarities)
    print("Closest question: ", closest_question)

    answer = df.Answer.iloc[closest_question].values[0]
    print("Answer:\n", answer)
