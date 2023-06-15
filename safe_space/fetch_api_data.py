import requests, json
from safe_space.chunking import get_chunks

def get_mod_data(text):
    """ 
        Fetches data from SightEngine Text Moderation api 
        parameters
        ----------
        text: str

    """

    # According to the text moderation API, text must not exceed 10,000 characters.
    # However, we don't know the number of characters that will be returned by text after scrapping
    # A walkaround will be to slice the text into by 9999 characters.

    data = {
    'text': text[0:9999],
    'mode': 'standard',
    'lang': 'en',
    'opt_countries': 'us,cm,ng,fr',
    'api_user': '431412659',
    'api_secret': 'xjcwb3jubEqTDHfmYqRr'
    }
    r = requests.post('https://api.sightengine.com/1.0/text/check.json', data=data)

    output = json.loads(r.text)

    return output

