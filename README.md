# Organisation des Données 2 - NoSQL
> Cours du défi Big Data de l'École des Mines de Saint-Étienne

## Challenge
"Ton challenge si tu l'acceptes, est :
1. D'installer une base de données Mongodb
2. D'insérer les données du fichier data.json.codechallenge.janv22.RHOBS.json
3. Répondre aux exercices suivants en écrivant le code python :
       1. Compter le nombre de femmes / d'hommes.
       2. Écrire une fonction qui renvoie les entreprises de plus de N personnes.
       3. Écrire une fonction qui prend en paramètre un métier et qui renvoie la pyramide des âges pour ce métier. "

## Requirements:
- Docker

## How to run:
```bash
docker run -d -p 27017:27017 --name od2_nosql mongo # in another terminal
python3 ./main.py
docker stop m1 # to stop the container
docker rm m1 # to remove the container
```

## MongoDB notation:
- Documents --> Data
- Collection --> Table
- A collection is composed by documents
