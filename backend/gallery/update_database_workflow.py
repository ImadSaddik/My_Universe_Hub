import requests

from .models import Gallery
from bs4 import BeautifulSoup
from datetime import datetime


def addNonExistingImages():
    print("Adding non-existing entries to the database.")
    a_tags = getATags()
    
    for tag in a_tags:
        item = scrape_a_tag(tag)
        if item['image_url'] is None:
            continue
        
        item['date'] = convertDate(item['date'])
        try:
            Gallery.objects.get(date=item['date'])
            print(f"{item['date']} is already in the database.")
            break
        except:
            print(f"{item['date']} is not in the database.")
            entry = Gallery.objects.create(
                date=item['date'],
                title=item['title'],
                explanation=item['explanation'],
                image_url=item['image_url'],
            )
            
            entry.save()
            
            
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

    dictionary['date'] = date
    dictionary['title'] = title
    dictionary['url'] = url
    dictionary['image_url'] = image
    dictionary['explanation'] = explanation

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


def convertDate(date):
    date = date.replace(':', '')
    return datetime.strptime(date, '%Y %B %d').date()


if __name__ == "__main__":
    addNonExistingImages()
