import requests, json

def get_mod_data(text):
    """ Fetches data from Text Moderation api """
    data = {
    'text': text,
    'mode': 'standard',
    'lang': 'en',
    'opt_countries': 'us,gb,fr',
    'api_user': '431412659',
    'api_secret': 'xjcwb3jubEqTDHfmYqRr'
    }
    r = requests.post('https://api.sightengine.com/1.0/text/check.json', data=data)

    output = r.text

    return output