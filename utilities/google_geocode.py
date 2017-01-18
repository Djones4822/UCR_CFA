import dataset
import googlemaps
from tqdm import tqdm

from config import settings, constants


db = dataset.connect(settings.DB_URL)

working_table = db[constants.SOURCE_TABLE_NAME]
geocode_table = db[constants.GOOGLE_GEOCODE_TABLE_NAME]

# You can use this to run through only GA agencies...
ga_agencies = working_table.find(agency_name='GA')

gmaps = googlemaps.Client(settings.GOOGLE_API_KEY)


def fix_address(s):
    """
    Takes in a string and attempts to put a space between the street
    address and PO Box...

    This was needed to deal with the discover policing data that was
    scrape for the Code For Atlanta FBI UCR project.

    Args:
    __s__: string to convert

    Returns: converted string
    """
    if s.find('PO Box') > 1:
        loc = s.find('PO Box')
        fixed_address = s[:loc] + ' ' + s[loc:]
    elif s.find('P.O. Box') > 1:
        loc = s.find('P.O. Box')
        fixed_address = s[:loc] + ' ' + s[loc:]
    elif s.find('P. O. Box') > 1:
        loc = s.find('P. O. Box')
        fixed_address = s[:loc] + ' ' + s[loc:]
    elif s.find('P O Box') > 1:
        loc = s.find('P O Box')
        fixed_address = s[:loc] + ' ' + s[loc:]
    else:
        fixed_address = s
    return fixed_address


for agency in tqdm(ga_agencies):
    geocoded_data = {}
    address_to_geocode = fix_address(agency[constants.ADDRESS_FIELD])
    results = gmaps.geocode(address_to_geocode)

    if len(results) > 0:
        r = results[0]
        geocoded_data.update({
            'google_formatted_address': r['formatted_address'],
            'location_type': r['geometry']['location_type'],
            'latitude': r['geometry']['location']['lat'],
            'longitude': r['geometry']['location']['lng'],
            })
        geocode_table.insert(geocoded_data)
