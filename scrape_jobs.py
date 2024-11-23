import os
import pymongo
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
from time import sleep
import random
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Load environment variables
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://hr:thik%6090@cluster0.ktn8tna.mongodb.net/")
DB_NAME = "job_data"
COLLECTION_NAME = "jobs"

# Initialize Selenium ChromeDriver
def init_chrome_driver():
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome("D:/Work/chromedriver-win64/chromedriver.exe", options=chrome_options)
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
    )
    return driver


def safe_action_move(driver, selector):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
        )
        ActionChains(driver).move_to_element(element).perform()
    except Exception as e:
        print(f"Error moving to element {selector}: {e}")


# Extract job links from a page
def extract_job_links(soup):
    job_links = []
    job_cards = soup.find_all("div", class_="job_seen_beacon")
    for card in job_cards:
        try:
            job_title = card.find("h2", class_="jobTitle")
            if job_title:
                job_link = job_title.find("a", href=True)
                if job_link:
                    full_link = f"https://www.indeed.com{job_link['href']}"
                    job_links.append(full_link)
        except Exception as e:
            print(f"Error extracting job link: {e}")
    return job_links

# Extract job details using requests

def extract_job_details(link):
    try:
        driver = init_chrome_driver()
        driver.get(link)
        safe_action_move(driver, "body")  # Adjusted to move to a generic element
        sleep(random.uniform(6, 10))
        safe_action_move(driver, "body")
        action = ActionChains(driver)
        action.move_to_element(driver.find_element(By.CSS_SELECTOR, "body")).perform()
        sleep(random.uniform(6, 10))
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Locate the main job details container
        details_container = soup.find("div", class_="jobsearch-JobComponent")

        # Extract job details with fallback for missing fields
        title = details_container.find("h1").text.strip() if details_container and details_container.find("h1") else "N/A"
        company = (details_container.find("div", class_="icl-u-lg-mr--sm") or
                   details_container.find("div", class_="jobsearch-InlineCompanyRating")).text.strip() if details_container else "N/A"
        location = details_container.find("div", class_="jobsearch-JobInfoHeader-subtitle").text.strip() if details_container else "N/A"
        description = details_container.find("div", class_="jobsearch-jobDescriptionText").text.strip() if details_container else "N/A"
        salary = details_container.find("div", class_="salary-snippet-container").text.strip() if details_container else "N/A"

        # Return job details as a dictionary
        return {
            "title": title,
            "company": company,
            "location": location,
            "salary": salary,
            "description": description,
            "scraped_at": datetime.utcnow().isoformat(),
            "link": link,
        }
    except requests.exceptions.RequestException as e:
        print(f"HTTP error extracting job details from {link}: {e}")
    except AttributeError as e:
        print(f"Parsing error extracting job details from {link}: {e}")
    except Exception as e:
        print(f"Unexpected error extracting job details from {link}: {e}")
    return None

# Check for pagination and collect all job links
def check_and_paginate(driver, pages_to_scrape=None):
    all_job_links = []
    current_page = 1

    while True:
        if pages_to_scrape and current_page > pages_to_scrape:
            print("Reached page limit.")
            break

        print(f"Scraping page {current_page}...")
        soup = BeautifulSoup(driver.page_source, "html.parser")
        job_links = extract_job_links(soup)
        all_job_links.extend(job_links)

        try:
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a[aria-label='Next Page']"))
            )
            safe_action_move(driver, "body")  # Adjusted to move to a generic element
            sleep(random.uniform(6, 10))
            safe_action_move(driver, "body")
            next_button.click()
            sleep(random.uniform(6, 10))
            current_page += 1
        except Exception as e:
            print(f"No more pages or error clicking 'Next': {e}")
            break

    return all_job_links

# Store data into MongoDB
def store_to_mongodb(data):
    if not data:
        print("No jobs found, nothing to insert.")
        return
    try:
        client = pymongo.MongoClient(MONGO_URI)
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]
        collection.insert_many(data)
        print(f"Inserted {len(data)} records into MongoDB.")
    except pymongo.errors.PyMongoError as e:
        print(f"MongoDB error: {e}")

# Main scraping function
def scrape_jobs(keyword="", city="", pages=1):
    base_url = f"https://www.indeed.com/jobs?q={keyword}&l={city}"
    driver = init_chrome_driver()
    driver.get(base_url)
    safe_action_move(driver, "body")  # Adjusted to move to a generic element
    sleep(random.uniform(6, 10))
    safe_action_move(driver, "body")
    action = ActionChains(driver)
    action.move_to_element(driver.find_element(By.CSS_SELECTOR, "body")).perform()
    sleep(random.uniform(6, 10))

    try:
        job_links = check_and_paginate(driver, pages_to_scrape=pages)
        print(f"Found a total of {len(job_links)} job links.")
        driver.quit()

        all_jobs = []
        for link in job_links:
            safe_action_move(driver, "body")  # Adjusted to move to a generic element
            sleep(random.uniform(6, 10))
            safe_action_move(driver, "body")
            sleep(random.uniform(3, 6))  # To avoid rate-limiting
            job_details = extract_job_details(link)
            if job_details:
                all_jobs.append(job_details)
            driver.quit()

        return all_jobs
    finally:
        driver.quit()

if __name__ == "__main__":
    keyword = "Python Developer"
    city = "Patna"
    jobs = scrape_jobs(keyword=keyword, city=city, pages=1)
    store_to_mongodb(jobs)