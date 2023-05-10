import happybase
import csv
import time

connection = happybase.Connection('127.0.0.1',9090, autoconnect=False)
table = connection.table('pokedex')

with open('./pokemon.csv') as csvfile:
    fieldnames = ['species_id', 'height', 'weight']
    writer = csv.DictReader(csvfile)

    for row in writer:
        pokemon_data = {}

        pokemon_data[b"species_id"] = row["species_id"].encode()
        pokemon_data[b"height"] = row["height"].encode()
        pokemon_data[b"weight"] = row["weight"].encode()

        table.put(row["id"].encode(), pokemon_data)

print(row)

connection.close()
