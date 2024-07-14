from bs4 import BeautifulSoup
import requests
import pandas as pd
from transformers import pipeline

def webscrape():
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

def scrape_individual_post(url):
    post_details = {}
    page = requests.get(url)
    
    if page.status_code == 200:
        print(f"Successfully retrieved individual blog post page: {url}")
        soup = BeautifulSoup(page.text, "html.parser")
        author_tag = soup.find('address', class_='max-w-[220px] mb-4')
        author = author_tag.get_text(strip=True).replace("By ", "") if author_tag else 'Author not found'
        content_tag = soup.find('article', class_='flex-1 sm:pl-10 sm:ml-10 border-border sm:border-l o-wysiwyg')
        content = content_tag.get_text(strip=True) if content_tag else 'Content not found'
        post_details['author'] = author
        post_details['content'] = content
    else:
        print(f"Failed to retrieve the individual blog post page. Status code: {page.status_code}")

    return post_details

webscrape()

df = pd.read_excel('blog_posts.xlsx')

summariser = pipeline("summarization")

def generate_summary(text):
    if pd.isna(text) or len(text) < 100:
        return text
    try:
        summaries = summariser(text, max_length=200, min_length=50, do_sample=False)
        return summaries[0]['summary_text']
    except Exception as e:
        return f"Error: {str(e)}"

df['Summary'] = df['Content'].apply(generate_summary)

df.to_excel('output.xlsx', index=False)

print("Summaries have been generated and saved to 'output.xlsx'.")


