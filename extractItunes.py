## Extract Top Apps' iTunes IDs
#
# USAGE:
# $python extractItunes.py [OUT_PATH]

import sys
from selenium import webdriver
import pandas as pd
import re

# URLs
URL_FREE = 'https://www.apple.com/itunes/charts/free-apps/'
URL_PAID = 'https://www.apple.com/itunes/charts/paid-apps/'

# CHROME path
CHROME_URL = '/Users/will/Google Drive/Programming/Webdrivers/chromedriver'

# Webdriver
def init_webdriver(headless=False):
    return webdriver.PhantomJS() if headless else webdriver.Chrome(CHROME_URL)


# URL Parser --> app name and app id
RE_PATTERN = re.compile('.*/([a-zA-F0-9%-]*)/(id[0-9]*)\?.*')
def parse_app_url(url):
    return re.match(RE_PATTERN, url)


# Obtains the information for the top app category selected (free/paid)
def get_top_apps(wd, catalogue_url, category):
    # Got to page
    wd.get(catalogue_url)

    # Parse all app elements
    applist = wd.find_elements_by_css_selector('.section-content li')
    hrefs = [ x.find_elements_by_tag_name('a')[0].get_attribute('href') for x in applist ]

    # Create a dataframe with Name, ID, CATEGORY and URL
    df = pd.DataFrame( [ parse_app_url(u).groups() for u in hrefs ],
                      columns=['name', 'id'])
    df['full_url'] = hrefs
    df['categ'] = category

    return df


# Scrape information for both free and paid categories
def main(out_path):
    wd = init_webdriver()

    print('Grabbing Top FREE apps...')
    free_apps = get_top_apps(wd, URL_FREE, 'free')

    print('Grabbing Top PAID apps...')
    paid_apps = get_top_apps(wd, URL_PAID, 'paid')

    # Close the webdriver
    wd.close()

    # Merge the dataframes and save
    all_apps = pd.concat([free_apps, paid_apps], ignore_index=True)
    all_apps.to_csv(out_path)

    print( 'Saved list to: {}'.format(out_path) )


if __name__ == '__main__':
    out_path = sys.argv[2] if len(sys.argv) > 1 else 'data/app_ids.csv'
    main(out_path)
