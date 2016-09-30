"""Initial setup

Revision ID: 7d28b515fd64
Revises: 
Create Date: 2016-09-30 00:34:37.039575

"""
from alembic import op
import sqlalchemy as sa
import geoalchemy2 as ga


# revision identifiers, used by Alembic.
revision = '7d28b515fd64'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('states',
                    sa.Column('state_id', sa.Integer, primary_key=True),
                    sa.Column('description', sa.String(40), nullable=False),
                    sa.Column('abbreviation', sa.String(5)))
    op.create_table('cities',
                    sa.Column('city_id', sa.Integer, primary_key=True),
                    sa.Column('state_id', sa.Integer, sa.ForeignKey('states.state_id'), nullable=False),
                    sa.Column('description', sa.String(200), nullable=False))
    op.create_table('counties',
                    sa.Column('county_id', sa.Integer, primary_key=True),
                    sa.Column('description', sa.String(200), nullable=False),
                    sa.Column('state_id', sa.Integer, sa.ForeignKey('states.state_id'), nullable=False))
    op.create_table('city_county_relate',
                    sa.Column('city_id', sa.Integer, sa.ForeignKey('cities.city_id')),
                    sa.Column('county_id', sa.Integer, sa.ForeignKey('counties.county_id')),
                    sa.PrimaryKeyConstraint('city_id', 'county_id'))
    op.create_table('zip_codes',
                    sa.Column('zip_code', sa.Numeric(5,0), primary_key=True),
                    sa.Column('county_id', sa.Integer, sa.ForeignKey('counties.county_id')))
    op.create_table ('locations',
                    sa.Column('location_id', sa.Integer, primary_key=True),
                     sa.Column('description', sa.Integer, nullable=False),
                     sa.Column('city_id', sa.Integer, sa.ForeignKey('cities.city_id'), nullable=False),
                     sa.Column('county_id', sa.Integer, sa.ForeignKey('counties.county_id'), nullable=False),
                     sa.Column('zip_code', sa.Numeric(5,0), sa.ForeignKey('zip_codes.zip_code'), nullable=True),
                     sa.Column('geom', ga.Geography, nullable=False),
                     sa.Column('is_exact', sa.Boolean, nullable=False))
    op.create_table('agencies',
                    sa.Column('agency_id', sa.Integer, primary_key=True),
                    sa.Column('description', sa.String(200), nullable=False),
                    sa.Column('number_of_officers', sa.Integer, nullable=True),
                    sa.Column('population_served', sa.Integer, nullable=True),
                    sa.Column('last_update', sa.Date, nullable=True),
                    sa.Column('location_id', sa.Integer, sa.ForeignKey('locations.location_id')))
    op.create_table('agency_fuzzy_names',
                    sa.Column('agency_id', sa.Integer, sa.ForeignKey('agencies.agency_id')),
                    sa.Column('fuzzy_description', sa.String(200)),
                    sa.PrimaryKeyConstraint('agency_id', 'fuzzy_description'))
    op.create_table('agency_types',
                    sa.Column('agency_type_id', sa.Integer, primary_key=True),
                    sa.Column('description', sa.String(200), nullable=False))
    op.create_table('agency_type_relate',
                    sa.Column('agency_id', sa.Integer, sa.ForeignKey('agencies.agency_id')),
                    sa.Column('agency_type_id', sa.Integer, sa.ForeignKey('agency_types.agency_type_id')),
                    sa.PrimaryKeyConstraint('agency_id', 'agency_type_id'))
    op.create_table('agency_phone_numbers',
                    sa.Column('agency_id', sa.Integer, sa.ForeignKey('agencies.agency_id')),
                    sa.Column('phone_number', sa.String(30)),
                    sa.PrimaryKeyConstraint('agency_id', 'phone_number'))
    op.create_table('crimes',
                    sa.Column('crime_id', sa.Integer, primary_key=True),
                    sa.Column('description', sa.String(300), nullable=False))
    op.create_table('crime_types',
                    sa.Column('crime_type_id', sa.Integer, primary_key=True),
                    sa.Column('description', sa.String(300), nullable=False),
                    sa.Column('parent_crime_type_id', sa.Integer, sa.ForeignKey('crime_types.crime_type_id'), nullable=True))
    op.create_table('crime_type_relate',
                    sa.Column('crime_id', sa.Integer, sa.ForeignKey('crimes.crime_id')),
                    sa.Column('crime_type_id', sa.Integer, sa.ForeignKey('crime_types.crime_type_id')),
                    sa.PrimaryKeyConstraint('crime_id', 'crime_type_id'))
    op.create_table('crime_stats_local',
                    sa.Column('agency_id', sa.Integer, sa.ForeignKey('agencies.agency_id')),
                    sa.Column('crime_id', sa.Integer, sa.ForeignKey('crimes.crime_id')),
                    sa.Column('year', sa.Integer, nullable=False),
                    sa.Column('date_interval', sa.Interval, nullable=False),
                    sa.Column('occurrences', sa.Integer, nullable=False),
                    sa.PrimaryKeyConstraint('agency_id', 'crime_id', 'year'))
    op.create_table('crime_stats_ucr',
                sa.Column('agency_id', sa.Integer, sa.ForeignKey('agencies.agency_id')),
                sa.Column('crime_id', sa.Integer, sa.ForeignKey('crimes.crime_id')),
                sa.Column('year', sa.Integer, nullable=False),
                sa.Column('date_interval', sa.Interval, nullable=False),
                sa.Column('occurrences', sa.Integer, nullable=False),
                sa.PrimaryKeyConstraint('agency_id', 'crime_id', 'year'))

def downgrade():
        op.drop_table('crime_stats_ucr')
        op.drop_table('crime_stats_local')
        op.drop_table('crime_type_relate')
        op.drop_table('crime_types')
        op.drop_table('crimes')
        op.drop_table('agency_phone_numbers')
        op.drop_table('agency_type_relate')
        op.drop_table('agency_types')
        op.drop_table('agency_fuzzy_names')
        op.drop_table('agencies')
        op.drop_table ('locations')
        op.drop_table('zip_codes')
        op.drop_table('city_county_relate')
        op.drop_table('counties')
        op.drop_table('cities')
        op.drop_table('states')
