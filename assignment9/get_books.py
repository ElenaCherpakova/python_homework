from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

import pandas as pd
import csv
import json
import traceback
import time

options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Enable headless mode
driver = webdriver.Chrome(service=ChromeService(
    ChromeDriverManager().install()), options=options)


def scraper(page_count, query):
    driver.get(
        f'https://durhamcounty.bibliocommons.com/v2/search?query={query}&searchType=smart&page={page_count}')
    title = driver.title
    print(f"Title: {title}")

    body = driver.find_element(By.CSS_SELECTOR, 'body')
    if body:
        lists = body.find_elements(
            By.CSS_SELECTOR, 'li[data-key="search-result-item"]')
        print(f"Length of the list: {len(lists)}")
    else:
        print("No body found")
    results = []
    for li in lists:
        try:
            title = li.find_element(
                By.CSS_SELECTOR, 'span.title-content').text.strip()
            print(f"Title: {title}")
            author_elements = li.find_elements(
                By.CSS_SELECTOR, 'a.author-link')
            author = '; '.join([author.text.strip()
                               for author in author_elements]) if author_elements else 'Unknown'
            format_info = li.find_element(
                By.CSS_SELECTOR, 'div.cp-format-info span.display-info-primary').text
            format, year = format_info.split(' | ')[0].split(' - ')
            book_data = {
                'Title': title,
                'Author': author,
                'Format-Year': f"{format}-{year}"
            }
            results.append(book_data)
        except Exception as e:
            print(f"An error occurred while processing the list item: {e}")
            traceback.print_exc()
            continue
    # Task 3: Create a DataFrame
    books_data_frame = pd.DataFrame(results)
    print(books_data_frame)

    # Task 4: Write out the Data
    # Write the DataFrame to a file called get_books.csv
    try:
        with open('get_books.csv', 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # check if the file is empty to write the header
            if file.tell() == 0: 
                writer.writerow(books_data_frame.columns)
            for row in books_data_frame.itertuples(index=False):
                writer.writerow(row)
    except Exception as e:
        print(f"An error occurred while saving as CSV: {e}")
        traceback.print_exc()

    # Write the results list out to a file called get_books.json
    data = {"books": results}
    try:
        try:
            with open('get_books.json', 'r', encoding='utf-8') as json_file:
                existing_data = json.load(json_file)
                existing_data['books'].extend(data['books'])
        except FileNotFoundError:
            existing_data = data
        with open('get_books.json', 'w', encoding='utf-8') as json_file:
            json.dump(existing_data, json_file, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"An error occurred while saving as JSON: {e}")
        traceback.print_exc()


page_count = 1
max_page_count = 3
query = 'learning%20spanish'

try:
    for page_count in range(1, max_page_count + 1):
        scraper(page_count, query)
        time.sleep(3)
except Exception as e:
    print("could't get the web page")
    print(f"Exception: {type(e).__name__} {e}")
finally:
    driver.quit()
