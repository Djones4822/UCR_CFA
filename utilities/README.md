# FBI Utilities

These processes are using PostgreSQL as the backend database.

Packages Used:

* dataset
* googlemaps
* psycopg2
* usaddress

To utilize these you need to follow these steps.

Step #1 - Install the following packages: dataset, googlemaps, psycopg2 & usaddress.

Step #2 - In the config directory you will need a settings.py file that contains the
database URL and your Google API Key. Will look like this.

DB_URL = "postgres://username:password@server:5432/database"

GOOGLE_API_KEY = "BlaBlaBla..."

You will need to register for the Google API key and this geocoder is limited to 2,500
requests per day. So you either have to split things up by day or pay a small fee to get
these geocoded.

Step #3 - Ensure you have your source data loaded into a table. Make adjustments to
the constrants.py file so it matches your source data and address field, etc. Below
are the settings I used for my run.

SOURCE_TABLE_NAME = 'discover_policing'
ADDRESS_FIELD = 'address'

PARSED_TABLE_NAME = 'parsed_data'
GOOGLE_GEOCODE_TABLE_NAME = 'google_geocoded'

Step #4 - Look over the address_parser.py program and once you are comfortable with
it and have everything setup for your environment go ahead and run the program. This
process takes about 1 minute for 10K records...

Step #5 - Check your results in PostgreSQL. You can use one of the .sql scripts.

Step #6 - Look over the google_geocode.py program and once you are comfortable with
it and have everything setup for your environment go ahead and run the program. This
process take a very long time as I was getting about 1-2 records geocoded per second.

Step #7 - Check your results in PostgreSQL. You can use one of the .sql scripts.

Step #8 - Once you are happy with the results I join the two tables and create the
desired results.

*NOTE: While getting things setup and test I would recommend you use the commented
out process that pulls only the GA records.
