import googlemaps
from datetime import datetime
import json

API_KEY = ### INSERT YOUR GOOGLE MAPS API KEY HERE ###


# This files was used to generate the lattitude and longitude coordinates
# stored in cood_county_coordinates_zips.json. Those coordinates
# are a necessary ingredient of the post made to the county care website.

def gen_zip_list():
    """
    This function takes our list of zip codes and converts them to a python list.
    """
    f = open("cook_county_zips.txt")
    zips = f.read()
    zip_list = zips.split()
    f.close()
    return zip_list

def gen_lat_long_pairs():
    """
    This function takes our list of zip codes and returns a csv file with each
    zip code associated with a lat and long pair from the google maps API.

    Returns: A JSON file with one column representing zip codes and anotehr 
    representing lat-long pairs.
    """
    gmaps = googlemaps.Client(key=API_KEY)
    
    zip_list = gen_zip_list()

    zip_searches = {}

    for z in zip_list:
        address = z + ", IL"
        geocode_result = gmaps.geocode(address)
        coordinates = geocode_result[0]["geometry"]["location"]
        lat_lng = str(coordinates["lat"]) + "," + str(coordinates["lng"])
        zip_searches[z] = lat_lng
    
    with open("cook_county_coordinates_zips.json", "w") as f:
        json.dump(zip_searches, f, indent=4, sort_keys=True)
    
