import urllib.parse
import time
import requests
import json

state = ["Alabama","Alaska","Arizona","Arkansas","California","Colorado",
  "Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho","Illinois",
  "Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland",
  "Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana",
  "Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York",
  "North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania",
  "Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah",
  "Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"]

from selenium import webdriver

# scraping the site 
def get_all_hikes(browser):
    for st in state:
        browser.get(f'https://www.alltrails.com/us/{state}')
        while True:
            try:
                load_hikes = WebDriverWait(browser, 20).until(EC.visibility_of_element_located((By.XPATH,"//div[@id='load_more'] [@class='feed-item load-more trail-load'][//a]")))
                load_more_hikes.click()
                time.sleep(7)
            except:
                break
        soup = BeautifulSoup(browser.page_source)
        return soup


# scraping the details
def parse_meta_data(hike_soup):
    header = hike_soup.find('div', id='title-and-menu-box')
    hike_name = header.findChild('h1').text
    difficulty = header.findChild('span').text
    stars = header.findChild('meta')['content']
    num_reviews = header.find('span', itemprop='reviewCount').text
    area = hike_soup.select('div.trail-rank')
    try:
        hike_region = area[0].findChild('span', itemprop='name').text
    except:
        hike_region = area[0].findChild('a').text
    # directions = header.select('li.bar-icon.trail-directions')
    try:
        distance = hike_soup.select('span.distance-icon')[0].text
    except:
        distance = None
    try:
        elevation_gain = hike_soup.select('span.elevation-icon')[0].text
    except:
        elevation_gain = None
    try:
        route_type = hike_soup.select('span.route-icon')[0].text
    except:
        route_type = None
    tags = hike_soup.select('section.tag-cloud')[0].findChildren('h3')
    hike_attributes = []
    for tag in tags:
        hike_attributes.append(tag.text)
    user_ratings = []
    users = hike_soup.select('div.feed-user-content.rounded')
    for user in users:
        if user.find('span', itemprop='author') != None:
            user_name = user.find('span', itemprop='author').text
            user_name = user_name.replace('.', '')
            try:
                rating = user.find('span', itemprop="reviewRating").findChildren('meta')[0]['content']
                user_ratings.append({user_name: rating})
            except:
                pass
    row_data = {}
    row_data['hike_name'] = hike_name
    row_data['hike_difficulty'] = difficulty
    row_data['stars'] = stars
    row_data['num_reviews'] = num_reviews
    row_data['hike_region'] = hike_region
    row_data['total_distance'] = distance
    row_data['elevation_gain'] = elevation_gain
    row_data['route_type'] = route_type
    row_data['hike_attributes'] = hike_attributes
    row_data['ratings'] = user_ratings
    return row_data

browser = webdriver.Chrome()
soup = get_all_hikes(browser)
create_db(soup, browser)