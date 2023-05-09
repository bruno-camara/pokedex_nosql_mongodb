# TP - Introduction à NoSQL

## MongoDB

### Prise en main

* assurez-vous d'avoir Python3\* sur votre machine
* accédez à la base de données SQLite en utilisant le module Python [`sqlite3`](https://docs.python.org/3/library/sqlite3.html) (qui est inclut dans la bibliothèque standard de Python3)
  * pour tester, reprenez l'une des requêtes du [TP précédent](https://seafile.emse.fr/f/48d9d580997047f388a1/) et affichez le résultat dans la console
* installez MongoDB
  * téléchargez le [serveur MongoDB](https://www.mongodb.com/try/download/community)
  * pour Linux ou OS X, vérifiez que le démon `mongod` a démarré (`sudo service restart mongod`)
  * pour Windows, cochez la case "Install MongoDB as a Service"
  * installez un client Python pour MongoDB, par exemple [PyMongo](https://pypi.org/project/pymongo/)
  * pour accéder manuellement au DBMS, installez `mongosh` ou Compass (avec interface graphique)

_(__**\***__) ou le langage de script de votre choix ; la plupart des langages permet d'accéder à une base de données SQLite ou NoSQL_

### Écriture de données

1.1. Inspectez le script [`load.py`](https://seafile.emse.fr/f/950b2fe45f954826a4da/) qui construit un document JSON pour chaque lieu connu de l'univers Pokémon, avec les sous-espaces du lieu (s'il y en a), la région à laquelle il appartient et les types Pokémons que l'on trouver à ce lieu, avec leur habitat. Les documents construits par le script ont la structure suivante (exemple de Jadielle) :

```json
{
  "id": "154",
  "identifier": "viridian-city",
  "name": {
    "fr": "Jadielle",
    "en": "Viridian City"
  },
  "region": "kanto",
  "areas": [],
  "encounters": [ "magikarp", "goldeen", "poliwag", "tentacool" ]
}

```

1.2. Adaptez ce script pour construires des documents JSON décrivant cette fois chacun un Pokémon, avec sa taille, son poids, ses types, ses attaques et les lieux où on le trouve. Les attaques doivent être associées à une valeur de dégâts, selon le type des Pokémons ciblés.

1.3. Stockez l'ensemble de ces documents JSON dans MongoDB en leur associant une clé, avec la commande [`insertOne`](https://pymongo.readthedocs.io/en/stable/tutorial.html#inserting-a-document). Quelle clé associez-vous à chaque document ? Notez le temps d'exécution pour l'import dans MongoDB. Comparez au temps d'exécution nécessaire à l'import des fichiers CSV correspondant dans SQLite.

_N'utilisez pas l'import « bulk » ou « batch », pour se rapprocher d'un cas d'utilisation réel._

### Lecture de données

Dans le TP précédent, vous avez étudié deux requêtes :

* la répartition géographique des Pokémon sur les lieux de Kanto
* l'effet des attaques sur les Pokémons en fonction de leur type

  2.1. Ces requêtes peuvent-elles être exprimées en une seule requête sur MongoDB (pour répondre, lisez le guide ["Read MongoDB data with queries"](https://www.mongodb.com/docs/guides/server/read_queries/) et le suivant) ?

  2.2. Reproduisez chacune de ces requêtes dans le langage de requête de MongoDB, depuis Python. Indiquez la différence en temps d'exécution par rapport à SQLite.

  2.3. La requête sur la répartition géographique des Pokémons peut être exécutées sur MongoDB de deux manières différentes : en partant des lieux ou en partant des Pokémons. Testez les deux en utilisant autant que possible [les opérateurs de sélection sur des listes](https://www.mongodb.com/docs/manual/tutorial/query-arrays/). Observez-vous une différence ? Pourquoi ?

## HBase

### Prise en main

* installez Apache HBase
  * sur Linux ou macOS
    * téléchargez la [dernière version du code](https://hbase.apache.org/downloads.html) (colonne **Download**, choisir **bin**)
    * décompressez l'archive téléchargée et placez-vous dans le dossier `hbase-<version>` créé
    * suivez le [Quickstart d'HBase](https://hbase.apache.org/book.html#quickstart)
      * identifiez le chemin d'accès vers votre installation Java
      * ouvrez le fichier `conf/hbase-env.sh`, indiquez le chemin vers Java comme valeur de la variable `JAVA_HOME` et décommentez la ligne 
      * lancez `bin/start-hbase.sh`
      * ouvrez un shell avec `bin/hbase shell`
  * sur Windows
    * reproduisez les étapes ci-dessus avec le [_Windows Subsystem for Linux (WSL)_](https://learn.microsoft.com/fr-fr/windows/wsl/install)
    * en cas d'échec, essayez via [Docker](https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe)
      * installez Docker Desktop, qui devrait aussi installer l'outil en ligne de commande `docker`
      * ouvrez un terminal et compilez une image Docker contenant HBase avec `docker build -t hbase https://github.com/vcharpenay/hbase-docker.git`
      * démarrez ensuite un conteneur sur la base de cette image avec `docker run -p 16000:16000 -p 16010:16010 -p 9090:9090 -i hbase`
      * vous devriez maintenant avoir un shell HBase accessible depuis le conteneur actif
* pour vérifier que votre instance de HBase est accessible, consultez le tableau de bord d'HBase à l'URL <http://localhost:16010> et/ou, dans le shell HBase, tapez `help` 
* installez un client Python pour HBase, par exemple [`happybase`](https://pypi.org/project/happybase/)

### Écriture de données

3.1. Dans la première partie, vous avez restructuré le Pokédex pour en stocker les informations principales dans une base de documents. Faites de même avec HBase en adaptant la structure des tables contenant lieux et Pokémons à celle d'une base de données à colonne extensible. Quel choix de familles de colonne faites-vous ? Déclarez ces familles dans le shell HBase avec la commande `create 'pokedex' 'cf1' 'cf2' 'cf3' ...` (où `cfi` est le nom d'une famille de colonnes) et importez les données dans HBase avec la commande [`put`](https://happybase.readthedocs.io/en/latest/api.html#happybase.Table.put). Comparez le temps d'exécution de l'import à SQLite.

### Lecture de données

4.1. De la même manière que vous avez traduit des requêtes SQL en un langage adapté à MongoDB, vous allez maintenant traduire ces requêtes (répartition géographique et effets des attaques de Pokémons) avec les opérations disponibles sur HBase : `get` et `scan`. Lisez la [remarque sur les Joins](https://hbase.apache.org/book.html#joins) puis repartez [du début](https://hbase.apache.org/book.html#quickstart) pour comprendre comment fonctionne `get` et `scan`.


