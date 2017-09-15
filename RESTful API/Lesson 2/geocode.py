import httplib2
import json

def getGeocodeLocation(inputString):
	google_api_key = "AIzaSyCY-MZwYJLNk4dRiZ10q4rXTRMmSBd-x8k"
	locationString = inputString.replace(" ","+")
	url = 'https://maps.googleapis.com/maps/api/geocode/json?address=%s,+Indonesia&key=%s' % (locationString, google_api_key)
	h = httplib2.Http()
	response, content = h.request(url,'GET')
	result = json.loads(content.decode('utf-8'))
	# print ("Response header : %s \n\n" % response)

	lat = result['results'][0]['geometry']['location']['lat']
	lng = result['results'][0]['geometry']['location']['lng']

	return (lat, lng)

