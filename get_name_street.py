import requests
from bs4 import BeautifulSoup
import time
import csv


def get_addresses():

    #area coordinates in the format min_longitude, min_latitude, max longitude, max_latitude
    input_box = ['58.4277,51.2125,58.4881,51.2645', '58.4881,51.2147,58.5255,51.2464',
                 '58.2477000,51.2874000,58.2712000,51.3037000',
                 '58.5458,51.1903,58.5884,51.2174']

    #the header of the table
    buildings = [['city', 'street', 'number', 'latitude', 'longitude']]
    list_id = list()
    list_cites = list()

    for element_input in input_box:
        r = requests.get('https://www.openstreetmap.org/api/0.6/map?bbox='+element_input)
        soup = BeautifulSoup(r.text, 'lxml')
        string_cite = 'https://nominatim.openstreetmap.org/lookup?format=xml&osm_ids='
	
	#building identifier list
        for element in soup.find_all('way'):
            if element.find('tag', {'k': 'addr:housenumber'}):
                list_id.append('W'+element.get('id'))

	#this part is used as needed
        '''for element in soup.find_all('relation'):
            if element.find('tag', {'k': 'addr:housenumber'}):
                list_id.append('R'+element.get('id'))
        for element in soup.find_all('node'):
            if element.find('tag', {'k': 'addr:housenumber'}):
                list_id.append('N'+element.get('id'))'''

    #Nominatim OSM API allows you to request data on only 50 objects
    while len(list_id) > 49:
        for element in list_id[:49]:
            string_cite += str(element) + ','
        del list_id[:49]
        list_cites.append(string_cite)
        string_cite = 'https://nominatim.openstreetmap.org/lookup?format=xml&osm_ids='

    #list of sites that provide information about objects
    for element in list_id:
        string_cite += str(element) + ','
    list_cites.append(string_cite)

    for element in list_cites:
        r1 = requests.get(element)
        soup1 = BeautifulSoup(r1.text, 'xml')

        #finding the name of the city, street, house number, latitude and longitude
        for i in soup1.find_all('place'):
            if i.city and i.road and i.house_number:
                buildings.append([i.city.string, i.road.string, i.house_number.string, i.get('lat'), i.get('lon')])
            elif i.town and i.road and i.house_number:
                buildings.append([i.town.string, i.road.string, i.house_number.string, i.get('lat'), i.get('lon')])
            elif i.village and i.road and i.house_number:
                buildings.append([i.village.string, i.road.string, i.house_number.string, i.get('lat'), i.get('lon')])

    #write to csv file
    with open('ourput_newapi.csv', "w", newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(buildings)


start_time = time.time()
get_addresses()
print(f"{time.time() - start_time} seconds")
