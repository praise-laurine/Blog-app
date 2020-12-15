import urllib.request,json
base_url = None

def configure_request(app):
    global base_url
    base_url = app.config['QUOTE_API_BASE_URL']

def getQuotes():
    getQuote_url ='http://quotes.stormconsultancy.co.uk/random.json'
    with urllib.request.urlopen(getQuote_url) as url:
        getQuote_data = url.read()
        getQuote_response = json.loads(getQuote_data)
    return getQuote_response

# import request,json
# from config import Config
# from . models import Quotes


# quotes_url = Config.QUOTES_URL

# def getQuotes():
#     random_quote = request.get(quotes_url)
#     new_quote = random_quote.json()
#     author = new_quote.get("author")
#     quote = new_quote.get("quote")
#     permalink = new_quote.get("permalink")
#     quote_object = Quotes(author,quote,permalink)
#     print(quote_object)
#     return quote_object


# def get_quotes():
#     response = requests.get('http://quotes.stormconsultancy.co.uk/random.json')
#     if response.status_code == 200:
#         quote = response.json()
#         return quote    