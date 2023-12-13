import requests

def get_quote():
        api_url = 'https://meowfacts.herokuapp.com/?count=3'
        response = requests.get(api_url)
        if response.status_code == requests.codes.ok:
            return response.json()["data"][0]
        else:
            return "Can't find any cat facts("