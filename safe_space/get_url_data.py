import requests
from bs4 import BeautifulSoup


def url_data(url):
    """ 
        Parameters
        -----------
        url : str
          url to be scraped
    """

    response = requests.get(url)
    html_page = response.content
    content = BeautifulSoup(html_page, 'html.parser')
    text = content.find_all(string=True)

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
    'style'
    ]
    for site_content in text:
        if site_content.parent.name not in blacklist:
            output += f"{site_content}"

    return output
