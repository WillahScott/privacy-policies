import sys
from selenium import webdriver
import pandas as pd

# URLs
URL_FREE = 'https://www.apple.com/itunes/charts/free-apps/'
URL_PAID = 'https://www.apple.com/itunes/charts/paid-apps/'

# Webdriver
wd = webdriver.Chrome('/Users/will/Google Drive/Programming/Webdrivers/chromedriver')

# URL Parser --> app name and app id
RE_PATTERN = re.compile('.*/([a-z-]*)/(id[0-9]*)\?.*')
def parse_app_url(url):
    return re.match(RE_PATTERN, url)


# Obtains the information for the top app category selected (free/paid)
def get_top_apps(catalogue_url, category):
    # Got to page
    wd.get(catalogue_url)

    # Parse all app elements
    applist = wd.find_elements_by_css_selector'.section-content li')
    hrefs = [ x.find_elements_by_tag_name('a')[0].get_attribute('href') for x in applist ]

    # Create a dataframe with Name, ID, CATEGORY and URL
    df = pd.DataFrame(zip(*[ parse_app_url(u) for u in hrefs ]),
                      columns=['name', 'id'])
    df['full_url'] = hrefs
    df['categ'] = category

    return df


# Scrape information for both free and paid categories
free_apps = get_top_apps(URL_FREE, 'free')
paid_apps = get_top_apps(URL_PAID, 'paid')
