# Organisation des Données 2 - NoSQL
> Cours du défi Big Data de l'École des Mines de Saint-Étienne

## MongoDB

### Requirements:
- Docker

### How to run:
```bash
docker run -d -p 27017:27017 --name od2_nosql mongo # in another terminal
python3 ./main.py
docker stop od2_nosql # to stop the container
docker rm od2_nosql # to remove the container
```

### MongoDB notation:
- Documents --> Data
- Collection --> Table
- A collection is composed by documents

## HBase

### How to run
```bash
./start-hbase.sh
./hbase-daemon.sh start thrift -p 9090 --infoport 9091
```

### Standalone HBase
```bash
./hbase shell
```

