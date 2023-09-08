import requests
from bs4 import BeautifulSoup
import re
import nltk
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize

nltk.download("punkt")
nltk.download("stopwords")

def get_article_summary(article_text, num_sentences=3):
    sentences = sent_tokenize(article_text)
    word_frequency = FreqDist(word_tokenize(article_text.lower()))
    stop_words = set(stopwords.words("english"))

    # Calculate the importance score for each sentence
    sentence_scores = {}
    for sentence in sentences:
        words = word_tokenize(sentence.lower())
        sentence_scores[sentence] = sum(
            [word_frequency[word] for word in words if word not in stop_words]
        )

    # Get the top num_sentences sentences as the summary
    sorted_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)
    summary_sentences = [sentence for sentence, score in sorted_sentences[:num_sentences]]
    summary = " ".join(summary_sentences)
    return summary

def scrape_news_articles(keyword):
    url = f"https://news.google.com/rss/search?q={keyword}"
    response = requests.get(url)

    if response.status_code != 200:
        print("Failed to fetch news articles.")
        return []

    soup = BeautifulSoup(response.content, "xml")
    articles = soup.find_all("item")
    results = []

    for article in articles[:5]:  # Get only the top 5 articles
        title = article.title.text
        link = article.link.text
        description = article.description.text

        # Get the full article content
        article_response = requests.get(link)
        article_soup = BeautifulSoup(article_response.content, "html.parser")
        article_text = ""
        for paragraph in article_soup.find_all("p"):
            article_text += paragraph.get_text()

        # Summarize the article
        summary = get_article_summary(article_text, num_sentences=3)

        results.append({"title": title, "link": link, "description": description, "summary": summary})

    return results

if __name__ == "__main__":
    keyword = input("Enter the keyword for news articles: ")
    articles = scrape_news_articles(keyword)

    if articles:
        print(f"Found {len(articles)} news articles related to '{keyword}':\n")
        for i, article in enumerate(articles, 1):
            print(f"{i}. Title: {article['title']}")
            print(f"   Link: {article['link']}")
            print(f"   Description: {article['description']}")
            print(f"   Summary: {article['summary']}\n")
    else:
        print("No news articles found for the given keyword.")

