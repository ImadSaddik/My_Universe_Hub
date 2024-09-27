import os
import json
import time
import requests
import google.generativeai as genai

from tqdm import tqdm
from bs4 import BeautifulSoup
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

dir_path = os.path.dirname(os.path.realpath(__file__)) # /Development/backend/utils
backend_dir = os.path.abspath(os.path.join(dir_path, os.pardir)) # /Development/backend
data_path = os.path.join(backend_dir, 'data', 'apod_data.json')


def scrapeAPODWebsite():
    print("Scraping the APOD website.")
    createOutputFileIfNotExists()

    a_tags = getATags()
    rpm_counter = 0
    start_time = time.time()
    for tag in tqdm(a_tags, total=len(a_tags)):
        try:
            item = scrape_a_tag(tag)
            if item['image_url'] is None:
                # This means that this is a video link, we don't want to include it
                continue

            with open(data_path, 'r') as file:
                data = json.load(file)

            if itemExistsInData(data, item):
                print(
                    f"Item for date {item['date']} already exists in the data. Stop scraping.")
                break
            else:
                data.append(item)

            # Write the updated data back to the file
            with open(data_path, 'w') as file:
                json.dump(data, file, indent=4)
                
            # to avoid hitting the rate limit of 15 requests per minute
            end_time = time.time()
            if end_time - start_time < 60:
                rpm_counter += 1
                if rpm_counter == 10: # 10 requests per minute just to leave a margin
                    time.sleep(60)
                    rpm_counter = 0
                    start_time = time.time()
        except Exception as e:
            print(f"An error occurred while scraping: {e}")
            continue


def createOutputFileIfNotExists():
    if not os.path.exists(data_path):
        with open(data_path, 'w') as file:
            file.write('[]')


def getATags():
    source = requests.get('https://apod.nasa.gov/apod/archivepix.html').text
    soup = BeautifulSoup(source, 'lxml')

    b_tag = soup.find_all('b')[1]
    return b_tag.find_all('a')


def scrape_a_tag(a_tag):
    dictionary = {}

    date = a_tag.find_previous(string=True).strip()
    title = a_tag.text.strip()
    url = f'https://apod.nasa.gov/apod/{a_tag["href"]}'
    image, explanation = getImageAndExplanation(url)
    authors = getAuthors(url)

    dictionary['date'] = date
    dictionary['title'] = title
    dictionary['url'] = url
    dictionary['image_url'] = image
    dictionary['explanation'] = explanation
    dictionary['authors'] = authors

    return dictionary


def getImageAndExplanation(url):
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')

    p_tags = soup.find_all('p')
    img_tag = soup.find('img')
    explanation = p_tags[2].get_text()

    try:
        img_url = f'https://apod.nasa.gov/apod/{img_tag["src"]}'
    except:
        img_url = None

    return img_url, explanation


def getAuthors(url):
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')

    center_tags = soup.find_all('center')
    credit_center_tag = center_tags[1]
    authors = extractAuthorsWithGemini(credit_center_tag)

    return authors


def extractAuthorsWithGemini(center_tag):
    query = f"""Given the following HTML code snippet, your role is to extract the credit information from the center tag.
The extracted credit information should be returned as a string and separated by a comma to denote multiple authors.
Dont't include prefix text like "Image Credit" or "Illustration Credit".

The HTML code snippet is as follows:
{center_tag}
"""

    model = genai.GenerativeModel('models/gemini-1.5-flash-002')
    response = model.generate_content(query)
    return response.text


def convertDate(date):
    date = date.replace(':', '')
    return datetime.strptime(date, '%Y %B %d').date()


def itemExistsInData(data, item):
    for entry in data:
        if entry['date'] == item['date']:
            return True
    return False


if __name__ == "__main__":
    scrapeAPODWebsite()
