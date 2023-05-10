from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
pokedex = client['pokedex']['inventory']

# Structure: loc = { 'id': id, 'identifier': identifier, 'weight' : weight, 'height' : height, 'types': [], 'moves': {}, 'encounters': [] }

# la répartition géographique des Pokémon sur les lieux de Kanto

# cursor = pokedex.find({'encounters': 'Kanto'})

# for doc in cursor:
#     print(doc)

# l'effet des attaques sur les Pokémons en fonction de leur type
# Pegar o efeito de um ataque em cada pokemon
# attaque : {
#   "pokemon" : 80,
#   "pokemon2": 90
# }

cursor = pokedex.find(
    {
        'moves' : 'cut'
    }
)

for doc in cursor:
    print(doc)