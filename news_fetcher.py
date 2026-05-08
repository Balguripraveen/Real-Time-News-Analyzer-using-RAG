import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("NEWS_API_KEY")


# -----------------------------------
# Fetch News Based on Topic
# -----------------------------------
def fetch_news(topic="technology"):

    url = "https://newsapi.org/v2/everything"

    params = {
        "q": topic,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 20,
        "apiKey": API_KEY
    }

    response = requests.get(url, params=params)

    data = response.json()

    articles = []

    for article in data["articles"]:

        title = article.get("title", "")
        description = article.get("description", "")
        content = article.get("content", "")

        full_text = f"""
        Title: {title}

        Description: {description}

        Content: {content}
        """

        articles.append(full_text)

    return articles