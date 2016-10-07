import urllib.request
import json
from apiclient.discovery import build

# https://developers.google.com/api-client-library/python/samples/simple_api_cmd_line_books.py
# https://developers.google.com/api-client-library/python/start/get_started#simple

class googleIt():
    def __init__(self):
        self.service = build('mawie', 'v1', developerKey='AIzaSyBwMtM1gMtMi-92SLUsmwoWUj9X_e8SV4g')

    def letsGoogleThatMovie(self, searchfor):
        if not type(searchfor, str):
            raise QueryFormatNotValide("Search item must be a string")
        print(searchfor)
        request = service.volumes().list(source='public', q=searchfor)
        response = request.execute()
        print(json_loads(response))

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
