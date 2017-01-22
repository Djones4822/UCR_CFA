import dataset
import googlemaps

from config import settings, constants


db = dataset.connect(settings.DB_URL)

working_table = db[constants.PARSED_TABLE_NAME]
geocode_table = db[constants.GOOGLE_GEOCODE_TABLE_NAME]

# You can use this to run through only GA agencies...
#ga_agencies = working_table.find(state_name='GA')
chunk = working_table.find(geocoded=False)

gmaps = googlemaps.Client(settings.GOOGLE_API_KEY)


for agency in chunk:
    geocoded_data = {}
    address_to_geocode = agency['fixed_address']
    print(address_to_geocode)
    results = gmaps.geocode(address_to_geocode)

    if len(results) > 0:
        r = results[0]
        geocoded_data.update({
            'google_formatted_address': r['formatted_address'],
            'location_type': r['geometry']['location_type'],
            'latitude': r['geometry']['location']['lat'],
            'longitude': r['geometry']['location']['lng'],
            'input_address': address_to_geocode,
            'id': agency['id'],
            })
        geocode_table.insert(geocoded_data)
