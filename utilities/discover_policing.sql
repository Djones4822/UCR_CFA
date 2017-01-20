---------------------------------------------------------------------
-- Parse the address into it's common components...
---------------------------------------------------------------------
-- Remove the table parsed_data...
-- drop table parsed_data;

-- Run the Python address_parser.py program

-- These are addresses where the po box number and street address
-- were concatenated together and there is not programmatic way to
-- break them apart. Somebody will need to research these further.
update parsed_data
  set address_type = 'Review Parsed Data'
where street_name is not NULL
  and usps_box_type is not NULL
  and parsed_data.usps_box_id is not NULL
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

select a.id, a.address_type, a.input_address, a.fixed_address,
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
    b.location_type,
    b.latitude,
    b.longitude,
    b.google_formatted_address
from parsed_data as a
  inner join google_geocoded as b
    on a.id = b.id;
