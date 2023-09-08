import requests
from bs4 import BeautifulSoup
import re

def scrape_news_articles(keyword):
    url = f"https://news.google.com/rss/search?q={keyword}&hl=en-US&gl=US&ceid=US%3Aen"
    response = requests.get(url)

    if response.status_code != 200:
        print("Failed to fetch news articles.")
        return []

    soup = BeautifulSoup(response.content, "xml")
    articles = soup.find_all("item")
    results = []

    for article in articles:
        title = article.title.text
        link = article.link.text
        description = article.description.text

        # You can perform additional filtering or processing on the description here
        # For example, you may want to extract relevant content from the description

        results.append({"title": title, "link": link, "description": description})

    return results

if __name__ == "__main__":
    keyword = input("Enter the keyword for news articles: ")
    articles = scrape_news_articles(keyword)

    if articles:
        print(f"Found {len(articles)} news articles related to '{keyword}':\n")
        for i, article in enumerate(articles, 1):
            print(f"{i}. Title: {article['title']}")
            print(f"   Link: {article['link']}")
            print(f"   Description: {article['description']}\n")
    else:
        print("No news articles found for the given keyword.")


