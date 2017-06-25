# Download the Android Privacy Policies from jreardon's folder
#    June, 2017

import os
from urllib import request
import pandas as pd


URL_BASE = 'https://meatwad.cs.berkeley.edu/~jreardon/policies'
DATA_PATH = '../data/raw/android/'

# If not there, create the ../data/raw/android/ folder
if not os.path.exists(DATA_PATH):
    print('Creating the folder path: {}'.format(DATA_PATH))
    os.makedirs(DATA_PATH)


def download_html(subfolder=''):
    response = request.urlopen(URL_BASE + '/' + subfolder)
    return response.read().decode('utf-8')


meta_html = download_html()

# extract only the html table with pandas
_start = meta_html.index('<table>')
_end = meta_html.index('</table>')
meta_table = meta_html[_start:_end]

# our data is the first table
metadata = pd.read_html(meta_table)[0]

# process the table
metadata.columns = metadata.ix[0]
metadata.drop(0, axis=0, inplace=True)
metadata['Extract'] = metadata.Name.apply( lambda x: x.startswith('policy__') )
metadata['File_type'] = metadata.Name.apply(
    lambda x: 'html'*int(x.endswith('.html'))+'folder'*int(x.endswith('_files/'))
    )

# Save as META
metadata.to_csv('../data/raw/android_list.csv')


# Download each policy
downloadable = metadata.loc[metadata.File_type.isin(['html']), 'Name'].values()

for _html in downloadable:
    print('  - Downloading: {}'.format(_html))
    with open( os.path.join(DATA_PATH, _html), 'w' ) as f:
        f.write(download_html(_html))
