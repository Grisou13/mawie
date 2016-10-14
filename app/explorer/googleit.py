import sys
import os
if __name__ == '__main__':
    sys.path.append(os.path.join(os.getcwd(), "../../"))
from app.research import duckduckgoapi

q = "very bad trip"+" :imdb"


res = duckduckgoapi.query(q)
print(dir(res))
print(res.related)
# print(res.related[0])
for i in res.results:
    print(i.url)
sys.exit()
# from google.appengine.api import search

# https://developers.google.com/api-client-library/python/samples/simple_api_cmd_line_books.py
# https://developers.google.com/api-client-library/python/start/get_started#simple

class googleIt():
    def __init__(self):
        api_key = 'AIzaSyB5T9oBbyEfTNnhN3G2faflnE2-69YpXS0'
        self.service = build('customsearch', 'v1', developerKey=api_key)

    def letsGoogleThatMovie(self, searchfor):

        res = self.service.cse().list(
            q='lectures',
            cx='017576662512468239146:omuauf_lfve',
        ).execute()
        pprint.pprint(res)

        """
        if not type(searchfor) is str:
            raise QueryFormatNotValide("Search item must be a string")
        print(searchfor)
        request = self.service.PageMaps().list(source='public', q=searchfor)
        response = request.execute()
        print(json_loads(response))
        """

    def getIntoLink(self):
        pass

    def getIDFromURL(self):
        pass

gogogo = googleIt()
gogogo.letsGoogleThatMovie("harry potter")

"""
query = raw_input ( 'Query: ' )
query = urllib.urlencode ( { 'q' : query } )
response = urllib.urlopen ( http://ajax.googleapis.com/ajax/services/search/web?v=1.0& + query ).read()
json = m_json.loads ( response )
results = json [ 'responseData' ] [ 'results' ]
for result in results:
    title = result['title']
    url = result['url']   # was URL in the original and that threw a name error exception
    print ( title + '; ' + url )"""
