# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service as ChromeService
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.common.by import By

# options = webdriver.ChromeOptions()
# options.add_argument('--headless')  # Enable headless mode
# options.add_argument('--disable-gpu')  # Optional, recommended for Windows
# options.add_argument('--window-size=1920x1080')  # Optional, set window size

# driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=options)

# driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
# try:
#     driver.get("https://en.wikipedia.org/wiki/Web_scraping")

#     title = driver.title
#     print(f"Title: {title}")

#     body = driver.find_element(By.CSS_SELECTOR, 'body')
#     if body:
#         links = body.find_elements(By.CSS_SELECTOR, 'a')
#         if len(links) > 0:
#             print("href: ", links[0].get_attribute('href'))

#     # list comprehension to get all images with src attributes
#     images = [(img.get_attribute('src')) for img in body.find_elements(By.CSS_SELECTOR, 'img[src]')]
#     print("Image Sources: ", images)
# except Exception as e:
#     print("could't get the web page")
#     print(f"Exception: {type(e).__name__} {e}")
# finally:
#     driver.quit()
# image_entries = driver.find_elements(By.CSS_SELECTOR, 'img[src]')

# images = []
# for img in image_entries:
#     images.append(img.get_attribute('src'))
# print("Image Sources: ", images)


# driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
# robots_url = "https://en.wikipedia.org/robots.txt"
# driver.get(robots_url)
# print(driver.page_source)
# driver.quit()



# driver.get("https://en.wikipedia.org/wiki/Web_scraping")

# see_also_h2 = driver.find_element(By.CSS_SELECTOR, '[id="See_also"]')

# links = []
# if(see_also_h2):
#     parent_div=see_also_h2.find_element(By.XPATH, '..')
#     if parent_div:
#         see_also_div = parent_div.find_element(By.XPATH, 'following-sibling::div')
#         link_elements = see_also_div.find_elements(By.CSS_SELECTOR, 'a')
#         for link in link_elements:
#             print(f"{link.text}: {link.get_attribute('href')}")
#             name = link.text.strip()
#             url = link.get_attribute('href')
            
#             if name and url:
#                 links.append({'name': name, 'url': url})
# driver.quit()

# import csv

# with open('scraped_data.csv', 'w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerow(['Name', 'Link'])
#     for link in links:
#         writer.writerow([link['name'], link['url']])
        
# import json
# data = {"links": links}
# with open('scraped_data.json', 'w') as json_file:
#     json.dump(data, json_file, indent=4)