---------------------------------------------------------------------
-- Check your source data and make sure all looks good...
---------------------------------------------------------------------
select *
from discover_policing;

-- Make sure all the id(s) are unique so we can match back.
select id
from discover_policing
group by id
having count(*) > 1;

---------------------------------------------------------------------
-- Parse the address into it's common components...
---------------------------------------------------------------------
-- Remove the table parsed_data...
-- drop table parsed_data;

-- Run the Python address_parser.py program

-- Check your results..
select *
from parsed_data;

-- These are addresses where the po box number and street address
-- were concatenated together and there is not programmatic way to
-- break them apart. Somebody will need to research these further.
update parsed_data
  set address_type = 'Review Parsed Data'
where street_name is not null
  and usps_box_type is not null
  and parsed_data.usps_box_id is not null
  and parsed_data.address_number is null;


select address_type, count(*) as cnt
from parsed_data
group by address_type;

select *
from parsed_data
where address_type in('Parsing Error', 'Review Parsed Data');

---------------------------------------------------------------------
-- Google GeoCode the records...
---------------------------------------------------------------------
-- Remove the table google_geocoded...
-- drop table google_geocoded;

-- Check your results..
select *
from google_geocoded;

-- I had the Google GeoCoding crash so I had to tag the records
-- already geocoded so I could continue on with the process.
alter table parsed_data
    add geocoded boolean;

update parsed_data
  set geocoded = True
where id in (select id from google_geocoded)
  and geocoded = False;

select count(*)
from parsed_data
where geocoded = False;

---------------------------------------------------------------------
-- Google GeoCode was not able to GeoCode all records. We are going
-- to code these via zip code only.
-- This is the file I found to do this with. If we find a better
-- source we can re-tag these.
-- https://gist.github.com/erichurst/7882666
---------------------------------------------------------------------

-- Cleaning up the zip codes...
update parsed_data
  set zip_code = right('0000' || zip_code, 5)
where char_length(zip_code) <> 5;

update parsed_data
  set zip_code = right('0000' || trim(right(input_address, 5)), 5)
where zip_code is null
  and position(',' in right(input_address, 5)) = 0;

select count(*) as cnt
from parsed_data
where geocoded = False;
-- 910

insert into google_geocoded (id, location_type, latitude, longitude, input_address)
select a.id, 'ZIP CODE' as location_type, b.latitude, b.longitude, a.input_address
from parsed_data as a
  inner join zip_lat_long as b
    on rtrim(a.zip_code) = rtrim(b.zip_code)
where a.geocoded = False;
-- Match 834

select location_type, count(*) as cnt
from google_geocoded
group by location_type;

---------------------------------------------------------------------
-- Building the output table and then exporting it to a
-- discover_policing_geocoded.csv
---------------------------------------------------------------------
select a.id, a.department, a.address_type, a.input_address, a.fixed_address,
    trim(regexp_replace(
        concat_ws(' ',
            coalesce(a.address_number_prefix, ''),
            coalesce(a.address_number, ''),
            coalesce(a.address_number_suffix, ''),
            coalesce(a.street_name_pre_modifier, ''),
            coalesce(a.street_name_pre_directional, ''),
            coalesce(a.street_name_pre_type, ''),
            coalesce(a.street_name, ''),
            coalesce(a.street_name_post_type, ''),
            coalesce(a.street_name_post_directional, ''),
            coalesce(a.street_name_post_modifier, ''),
            coalesce(a.occupancy_type, ''),
            coalesce(a.occupancy_identifier)
        ), '\s+', ' ', 'g')) as address,
    trim(regexp_replace(
        concat_ws(' ',
            coalesce(a.usps_box_type, ''),
            coalesce(a.usps_box_id, ''),
            coalesce(a.usps_box_group_type),
            coalesce(a.usps_box_group_id)
        ), '\s+', ' ', 'g')) as po_box,
    a.place_name as city,
    a.state_name as state,
    a.zip_code,
    b.location_type as geocode_results,
    b.latitude,
    b.longitude,
    b.google_formatted_address
into discover_policing_geocoded
from parsed_data as a
  left join google_geocoded as b
    on a.id = b.id
order by a.id;

-- Checking the final table before exporting...
select *
from discover_policing_geocoded;

