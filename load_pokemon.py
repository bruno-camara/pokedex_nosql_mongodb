import sqlite3
from pymongo import MongoClient

import time

locs = []

con = sqlite3.connect('../sql/tp/pokedex.sqlite') # TODO change path

for [id, identifier, species_id, weight, height] in con.cursor().execute('select id, identifier, species_id, weight, height from pokemon'):
	# create object with basic entries
	loc = { 'id': id, 'identifier': identifier, 'weight' : weight, 'height' : height, 'types': [], 'moves': {}, 'encounters': [] }

	# # add name entry to object (as language map)
	# langQuery = 'select local_language_id, name from location_names where local_language_id in (5, 9) and location_id = "{}"'.format(id)
	# for [langId, name] in con.cursor().execute(langQuery):
	# 	if langId == 5:
	# 		loc['name']['fr'] = name
	# 	elif langId == 9:
	# 		loc['name']['en'] = name

	# add move entry to object
	if species_id != None:
		# moveQuery = 'select move_names.name from pokemon_moves inner join move_names on pokemon_moves.move_id=move_names.move_id where pokemon_moves.pokemon_id = "{}" and move_names.local_language_id=5;'.format(species_id)
		moveQuery = 'select m.identifier as move, m.damage_class_id, t.identifier, te.damage_factor*m.power/100 as damage \
					from pokemon_moves pm \
					inner join moves m on pm.move_id = m.id \
					inner join type_efficacy te on m.type_id = te.damage_type_id and te.target_type_id = pm.version_group_id \
					inner join types t on t.id = te.target_type_id \
					where pm.pokemon_id = {}'.format(species_id)
		for [move, damage_class, target_type, damage] in con.cursor().execute(moveQuery):

			if move not in loc['moves']:
				loc['moves'][move] = {}
			
			if target_type not in loc['moves'][move]:
				loc['moves'][move][target_type] = damage
			
	# add type entry to object
	if species_id != None:
		typeQuery = 'select type_names.name from pokemon_types inner join type_names on pokemon_types.type_id=type_names.type_id where pokemon_id = "{}" and local_language_id=5;'.format(species_id)
		for [type] in con.cursor().execute(typeQuery):
			if type != None:
				loc['types'].append(type)

	# add encounters entry to object
	if species_id != None:
		#encounterQuery = 'select location_areas.identifier from pokemon inner join encounters on pokemon.species_id=encounters.pokemon_id inner join location_areas on location_areas.location_id=encounters.location_area_id where pokemon_id = "{}";'.format(species_id)
		encounterQuery = 'select distinct region_names.name as "name_region" from encounters join pokemon on encounters.pokemon_id = pokemon.species_id join pokemon_species_names on pokemon.species_id = pokemon_species_names.pokemon_species_id join location_areas on encounters.location_area_id = location_areas.id join locations on location_areas.location_id = locations.id join regions on locations.region_id = regions.id join region_names on regions.id = region_names.region_id where region_names.local_language_id = 5 and pokemon.species_id="{}";'.format(species_id)
		for [encounter] in con.cursor().execute(encounterQuery):
			if encounter != None:
				loc['encounters'].append(encounter)

	# append object to list of locations
	locs.append(loc)

# check that object creation ran without error
#assert len(locs) == 781
print(locs[0])

# load all objects to MongoDB using pyMongo
client = MongoClient('mongodb://localhost:27017/')
pokedex = client['pokedex']['inventory']

start = time.time()

for loc in locs:
	loc['_id'] = loc['id'] # _id is interpreted by MongoDB as the document's key
	pokedex.insert_one(loc)

end = time.time()
print("Temps d'exécution pour l'import dans MongoDB: ", end - start, "s")

# TODO query MongoDB using pokedex.find_one() and pokedex.find()
# see also https://pymongo.readthedocs.io/en/stable/tutorial.html#getting-a-single-document-with-find-one
# see also https://pymongo.readthedocs.io/en/stable/tutorial.html#querying-for-more-than-one-document