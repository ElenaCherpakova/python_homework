from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import csv
import traceback

options = webdriver.ChromeOptions()

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
try:
    driver.get("https://owasp.org/www-project-top-ten/")

    see_h2 = driver.find_element(By.CSS_SELECTOR, '[id="top-10-web-application-security-risks"]')
    
    links = []
    if(see_h2):
        parent_div = see_h2.find_element(By.XPATH, '..')
        if parent_div:
            see_ul = parent_div.find_element(By.CSS_SELECTOR, 'ul')
            # print(see_ul)
            see_second_ul = see_ul.find_element(By.XPATH, 'following-sibling::ul')
            print(see_second_ul)
            link_elements = see_second_ul.find_elements(By.CSS_SELECTOR, 'a')
            for link in link_elements:
                print(f"{link.text}: {link.get_attribute('href')}")
                title = link.text.strip()
                url = link.get_attribute('href')
                if title and url:
                    links.append({'title': title, 'url': url})
    print(links) 
except Exception as e:
    print("could't get the web page")
    print(f"Exception: {type(e).__name__} {e}")
finally:
    driver.quit()
    
try:    
    with open('owasp_top_10.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'URL'])
        for link in links:
            writer.writerow([link['title'], link['url']])
except Exception as e:
        print(f"An error occurred while saving as CSV: {e}")
        traceback.print_exc()