from bs4 import BeautifulSoup
import requests
import pandas as pd
from transformers import pipeline
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

summariser = pipeline("summarization")

def scrape_individual_post(url):
    post_details = {}
    page = requests.get(url)

    if page.status_code == 200:
        print(f"Successfully retrieved individual blog post page: {url}")
        soup = BeautifulSoup(page.text, "html.parser")
        author_tag = soup.find('address', class_='max-w-[220px] mb-4')
        author = author_tag.get_text(strip=True).replace("By ", "") if author_tag else 'Author not found'
        content_tag = soup.find('article',
                                class_='flex-1 sm:pl-10 sm:ml-10 border-border sm:border-l o-wysiwyg')
        content = content_tag.get_text(strip=True) if content_tag else 'Content not found'
        post_details['author'] = author
        post_details['content'] = content
    else:
        print(f"Failed to retrieve the individual blog post page. Status code: {page.status_code}")

    return post_details

def generate_summary(text):
    if pd.isna(text) or len(text) < 100:
        return text
    try:
        summaries = summariser(text, max_length=200, min_length=50, do_sample=False)
        return summaries[0]['summary_text']
    except Exception as e:
        return f"Error: {str(e)}"

''' Main shareaction parser'''
def parse_shareaction():
    base_url = "https://shareaction.org"
    blog_url = f"{base_url}/news/blog"
    print(f"Requesting main blog page: {blog_url}")
    page_to_scrape = requests.get(blog_url)

    if page_to_scrape.status_code == 200:
        print(f"Successfully retrieved main blog page")
        soup = BeautifulSoup(page_to_scrape.text, "html.parser")
        articles = soup.findAll('a', class_='block w-1/2 pl-10 mb-10 md:w-1/4')

        print(f"Found {len(articles)} articles")
        results = []

        for article in articles:
            header = article.find('h6')
            header_text = header.get_text(strip=True) if header else 'No Header Found'
            time_posted = article.find('time').get_text(strip=True) if article.find('time') else 'Time not found'
            link = article.get('href')
            post_url = link if link.startswith('http') else f"{base_url}{link}"

            if post_url:
                print(f"Requesting individual blog post page: {post_url}")
                post_details = scrape_individual_post(post_url)
                author = post_details.get('author', 'Author not found')
                content = post_details.get('content', 'Content not found')
            else:
                author = 'Author not found'
                content = 'Content not found'

            results.append({
                'Header': header_text,
                'Time Posted': time_posted,
                'URL': post_url,
                'Author': author,
                'Content': content
            })

        df = pd.DataFrame(results)
        df.to_excel('blog_posts.xlsx', index=False)
        print("Data has been written to blog_posts.xlsx")
    else:
        print(f"Failed to retrieve the webpage. Status code: {page_to_scrape.status_code}")

'''Scrapes a single shareaction page'''
def scrape_page():
    print('Scraping page...')
    pass

'''Goes to the next page of UNPRI'''
def next_page():
    print('Going to next page...')
    pass

# Function which scrapes signatories from all pages in UNPRI
def find_signatories():
    print('Finding signatories...')
    for page in range(0, 9):  # you can parse this number from the bottom of the page if you think it should be dynamic
        scrape_page()
        next_page()
    pass

# A function to click the 'Download' button based on its HTML class
def download_signatories():
    print('Downloading signatories...')

    
    download_directory = os.getcwd()
    chrome_options = Options()
    chrome_options.add_experimental_option('prefs', {
        "download.default_directory": download_directory,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })

    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        
        url = 'https://www.unpri.org/signatories/signatory-resources/signatory-directory'
        driver.get(url)

        
        wait = WebDriverWait(driver, 20)
        try:
            download_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.button[href$='.xlsx']")))
            download_button.click()

            
            time.sleep(10)

            
            files = os.listdir(download_directory)
            excel_files = [f for f in files if f.endswith('.xlsx')]
            excel_files.sort(key=lambda x: os.path.getmtime(os.path.join(download_directory, x)), reverse=True)

            if excel_files:
                latest_file = excel_files[0]
                print(f"Download complete. The file '{latest_file}' has been downloaded successfully.")
            else:
                print("Download completed, but no Excel file found.")

        except Exception as e:
            print(f"Could not find the download button. Printing page source for debugging:\n{driver.page_source}")
            raise e

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        
        driver.quit()

# https://www.unpri.org/signatories/signatory-directory
def parse_unpri():
    find_signatories()
    download_signatories()
    pass

# https://www.unepfi.org/net-zero-alliance/alliance-members/
def parse_unepfi():
    pass


parse_shareaction()
parse_unpri()

