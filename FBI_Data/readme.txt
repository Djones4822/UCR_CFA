There are a couple files here - I have 52 files downloaded from the UCR (found here: http://www.ucrdatatool.gov/) for the most recent here. There is one duplicate file, I don't know which, I didn't really care. 

I wrote a python script to merge them all, not included here (don't know where that one went) and the final merging is "all_state_data.csv"

Then I broke the name into fragments, like "Atlanta City" and "Police Department" to isolate the area name from the agency type and used google places to find a location of each department. This worked for all but 4 (they're still blank). I then used google geolocating to get all the longitudes and latitudes. In this process I also removed the duplicates. 

This final file is called "FBI_all_states_geolocated.csv" which I've included in the root directory. There is a total of 4391 agencies reporting.
