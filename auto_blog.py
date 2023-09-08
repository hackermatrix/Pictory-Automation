import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import asyncio

def  get_article_summary_with_chatgpt(article_text):
    time.sleep(3)
    # Set up Selenium WebDriver (Chrome) with the custom profile
    s=Service("./chromedriver")

    chrome_profile_path = "~/.config/google-chrome/Profile 1"
    options = webdriver.ChromeOptions()
    options.add_argument(r"--user-data-dir=/home/popeye/.config/google-chrome/") # e.g. /home/username/.config/google-chrome/Profile 3
    options.add_argument(r'--profile-directory=Profile 1') 
    options.add_argument("--remote-debugging-port=9222")

    driver = webdriver.Chrome(service=s,options=options)

    driver.get('https://chat.openai.com/?model=text-davinci-002-render-sha')


    # Wait for the page to load (you may need to adjust the wait time based on your internet speed)
    time.sleep(5)

    #Click cancel button on AIPRM
    cancel_click = driver.find_element(By.XPATH,'//button[@id="quotaMessageModalCancel"]')
    cancel_click.click()

    #Search For the News Prompt:
    search_prompt = driver.find_element(By.XPATH,'//input[@id="promptSearchInput"]')
    search_prompt.send_keys("news")
    
    # wait for prompt to appear:
    time.sleep(2)

    #Select the first Prompt:
    prompt_select = driver.find_element(By.XPATH,'//h3[contains(text(),"AI News Reporter V1.6 -- 100% Accuracy")]')
    prompt_select.click()


    # Find the input field to interact with ChatGPT
    input_field = driver.find_element(By.XPATH, '//textarea[@id="prompt-textarea"]')

    # Set the article text as the input to ChatGPT
    input_field.send_keys(article_text)

    bt = driver.find_element(By.XPATH,'//button[@class="absolute p-1 rounded-md md:bottom-3 md:p-2 md:right-3 dark:hover:bg-gray-900 dark:disabled:hover:bg-transparent right-2 disabled:text-gray-400 enabled:bg-brand-purple text-white bottom-1.5 transition-colors disabled:opacity-40"]')

    bt.click()
    # Wait for the response from ChatGPT (you may need to adjust the wait time based on the length of the article)
    time.sleep(25)

    # Get the response from ChatGPT
    output_element = driver.find_element(By.XPATH, '(//div[@class="flex flex-grow flex-col gap-3"])[2]')
    summary = output_element.text

    # Close the browser
    driver.quit()

    return summary

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
            print(f"   Description: {article['description']}")
            
            # Get the full article content
            article_response = requests.get(article['link'])
            article_soup = BeautifulSoup(article_response.content, "html.parser")
            article_text = ""
            for paragraph in article_soup.find_all("p"):
                article_text += paragraph.get_text()

            # Summarize the article with ChatGPT
            
            summary = get_article_summary_with_chatgpt(article_text)
            print(f"   Summary (using ChatGPT): {summary}\n")
    else:
        print("No news articles found for the given keyword.")

