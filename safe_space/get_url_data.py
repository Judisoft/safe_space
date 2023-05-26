import requests
from bs4 import BeautifulSoup


def url_data(url):
    """ Takes a url as argument and returns its text content """
    # url = 'https://www.troyhunt.com/the-773-million-record-collection-1-data-reach/'
    response = requests.get(url)
    html_page = response.content
    content = BeautifulSoup(html_page, 'html.parser')
    text = content.find_all(text=True)

    output = ''
    blacklist = [
    '[document]',
    'noscript',
    'header',
    'html',
    'meta',
    'head', 
    'input',
    'script',
    ]
    for site_content in text:
        if site_content.parent.name not in blacklist:
            output += f"{site_content}"

    return output