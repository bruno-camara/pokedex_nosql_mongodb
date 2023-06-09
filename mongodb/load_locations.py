import sqlite3
from pymongo import MongoClient

locs = []

con = sqlite3.connect('../sql/tp/pokedex.sqlite') # TODO change path

for [id, identifier, regionId] in con.cursor().execute('select id, identifier, region_id from locations'):
	# create object with basic entries
	loc = { 'id': id, 'identifier': identifier, 'name': {}, 'areas': [], 'encounters': [] }

	# add name entry to object (as language map)
	langQuery = 'select local_language_id, name from location_names where local_language_id in (5, 9) and location_id = "{}"'.format(id)
	for [langId, name] in con.cursor().execute(langQuery):
		if langId == 5:
			loc['name']['fr'] = name
		elif langId == 9:
			loc['name']['en'] = name

	# add region entry to object
	if regionId != None:
		regionQuery = 'select identifier from regions where id = "{}"'.format(regionId)
		region = con.cursor().execute(regionQuery).fetchone()[0]
		loc['region'] = region

	# add area list to object
	areasQuery = 'select id, identifier from location_areas where location_id = "{}"'.format(id)
	for [areaId, areaIdentifier] in con.cursor().execute(areasQuery):
		if areaIdentifier != None:
			loc['areas'].append(areaIdentifier)

		# add Pokémon encounter list to location (aggregating for all areas in the location)
		encountersQuery = 'select distinct p.identifier from encounters as e, pokemon as p where e.pokemon_id = p.id and e.location_area_id = "{}"'.format(areaId)
		for [pokemonIdentifier] in con.cursor().execute(encountersQuery):
			if not pokemonIdentifier in loc['encounters']:
				loc['encounters'].append(pokemonIdentifier)

	# append object to list of locations
	locs.append(loc)

# check that object creation ran without error
assert len(locs) == 781
print(locs[15])

# load all objects to MongoDB using pyMongo
client = MongoClient('mongodb://localhost:27017/')
pokedex = client['pokedex']['inventory']

for loc in locs:
	loc['_id'] = loc['id'] # _id is interpreted by MongoDB as the document's key
	pokedex.insert_one(loc)

# TODO query MongoDB using pokedex.find_one() and pokedex.find()
# see also https://pymongo.readthedocs.io/en/stable/tutorial.html#getting-a-single-document-with-find-one
# see also https://pymongo.readthedocs.io/en/stable/tutorial.html#querying-for-more-than-one-document