from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

def drive():
    s=Service("./chromedriver")

    chrome_profile_path = "~/.config/google-chrome/Profile 1"
    options = webdriver.ChromeOptions()
    options.add_argument(r"--user-data-dir=/home/popeye/.config/google-chrome/") # e.g. /home/username/.config/google-chrome/Profile 3
    options.add_argument(r'--profile-directory=Profile 1') 
    options.add_argument("--remote-debugging-port=9222")

    driver = webdriver.Chrome(service=s,options=options)

    driver.get('https://chat.openai.com/?model=text-davinci-002-render-sha')

if __name__=="__main__":
    drive()
