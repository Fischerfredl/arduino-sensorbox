import argparse
import shapefile

# setup argument parser
parser = argparse.ArgumentParser(
    description='Transforms csv data from sensorbox to a shapefile.'
)
parser.add_argument('-i', '--infile', help='The csv to read from', required=True)
parser.add_argument('-o', '--outfile', help='The shapefile to write', required=True)
parser.add_argument('--date', help='filter by date (%d%m%y). Not zero padded')
args = vars(parser.parse_args())
print(args)

# define fields as (field name, shapefile type, python type)
FIELDS = [
    ('ID', 'N', int),
    ('millis', 'N', int),
    ('date', 'C', str),
    ('time', 'C', str),
    ('lat', 'N', float),
    ('lon', 'N', float),
    ('alt', 'N', float),
    ('sats', 'N', int),
    ('hdop', 'N', int),
    ('lux', 'N', int),
    ('pm01', 'N', int),
    ('pm25', 'N', int),
    ('pm10', 'N', int),
    ('temp', 'N', float),
    ('hum', 'N', float)
]

# initialize shapefile writer
shp = shapefile.Writer(args['outfile'], shapeType=shapefile.POINT)
shp.autoBalance = 1  # ensures geometry and attributes match

# create fields
for field in FIELDS:
    shp.field(field[0], field[1])

# parse csv
with open(args['infile'], 'r') as infile:
    for line in infile:
        # parse line to dict
        line = line.split(',')
        line = { f[0]: f[2](line[idx]) for idx, f in enumerate(FIELDS) }
        # filter outliers
        if not (47 < line['lat'] < 49 or 10 < line['lon'] < 12):
            continue
        # filter by date
        if args['date'] and line['date'] != args['date']:
            continue
        # process entry
        shp.point(line['lon'], line['lat'])
        shp.record(**line)

# close the shapefile
shp.close()
