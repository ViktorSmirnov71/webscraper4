# Web Scraper for Blog Posts

## Overview

This project is a web scraper designed to extract blog posts from the ShareAction website, summarize their content, and save the results to an Excel file. This tool helps in efficiently gathering and summarizing information from online sources.

## Features

- **Web Scraping**: Extracts blog post details including headers, publication times, authors, and content.
- **Content Summarization**: Utilizes advanced NLP models to generate concise summaries of blog content.
- **Data Export**: Saves the extracted data and summaries into an Excel file for easy access and analysis.

## Requirements

- Python 3.x
- `requests`
- `beautifulsoup4`
- `pandas`
- `transformers`
- `openpyxl`

## Limitations

While this web scraper is designed to efficiently extract and summarize blog content, there are a few limitations to be aware of:

1. **Content Length Limitations**:
   - The summarization model used may not handle very long articles effectively. If a blog post exceeds the model's token limit, the summarization might be incomplete or fail to capture the full essence of the content. As a result, some blog posts may not be summarized in their entirety.

2. **Website-Specific Design**:
   - The current implementation of the scraper is tailored to the specific structure and class names used on the ShareAction website. This means that the scraper relies on predefined HTML classes and structures which can vary significantly between different websites. Consequently, it may not work as intended for other websites where class names and HTML structures differ. Adapting the scraper to handle multiple websites would require customizations for each new site, which involves updating the class selectors and parsing logic accordingly.

3. **Class and Structure Variability**:
   - Websites often use different HTML structures and CSS classes to format their content. Because of this variability, the scraper may not be able to consistently extract elements such as headers, URLs, and publication times from sites with different design patterns. This limitation restricts the scraper’s usability to websites with a similar layout to the one it was originally designed for.

