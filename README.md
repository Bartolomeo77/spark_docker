# spark_docker

# Spark Cluster with Docker & docker-compose

# General

Un clúster independiente de Spark simple para los fines de su entorno de pruebas. Una solución *docker-compose up* alejada de usted para su entorno de desarrollo Spark.

Docker Compose creará los siguientes contenedores:

container|Exposed ports
---|---
spark-master|9090 7077
spark-worker-1|9091
spark-worker-2|9092
demo-database|5432

# Installation

Los siguientes pasos le permitirán ejecutar los spark cluster's containers.

## Pre requisites

* Docker installed

* Docker compose  installed

## Build the image
```sh
cd spark_docker
```

```sh
docker build -t cluster-apache-spark:3.0.2 .
```

## Run the docker-compose

El último paso para crear su clúster de prueba será ejecutar compose file:

```sh
docker-compose up -d
```

## Validate your cluster

valide su clúster accediendo a la interfaz de usuario de Spark en cada URL maestra y de trabajador.

### Spark Master

http://localhost:9090/

### Spark Worker 1

http://localhost:9091/

### Spark Worker 2

http://localhost:9092/


# Resource Allocation 

Este clúster se envía con 2 trabajadores y un maestro, cada uno de los cuales tiene un conjunto particular de asignación de recursos (básicamente asignación de núcleos de RAM y CPU).
* La asignación predeterminada de núcleos de CPU para cada Spark Worker es 1 núcleo.

* La RAM predeterminada para cada spark-worker es 1024 MB.

* La asignación de RAM predeterminada para los ejecutores Spark es 256 MB.

* La asignación de RAM predeterminada para el controlador Spark es 128 MB

* Si desea modificar estas asignaciones, simplemente edite el archivo env/spark-worker.sh. o el archivo docker compose file

# Binded Volumes

Para facilitar la ejecución de la aplicación, he enviado dos montajes de volumen que se describen en el siguiente cuadro:

Host Mount|Container Mount|Purposse
---|---|---
apps|/opt/spark-apps| Se utiliza para que los archivos jar, py de su aplicación estén disponibles para todos los trabajadores y maestros.
data|/opt/spark-data| Se utiliza para que los datos de su aplicación estén disponibles para todos los trabajadores y maestros


# Run Sample applications

## NY Bus Stops Data [Pyspark]

This programs just loads archived data from [MTA Bus Time](http://web.mta.info/developers/MTA-Bus-Time-historical-data.html) and apply basic filters using spark sql, the result are persisted into a postgresql table.

The loaded table will contain the following structure:

userid|movieid|ratingid|stamtimeid
---|---|---|---
196|242|3|881250949
			

To submit the app connect to one of the workers or the master and execute:
```sh
docker exec -it spark_docker_spark-master_1 /bin/bash
root@959b7c958f23:/opt/spark#
```

```sh
/opt/spark/bin/spark-submit --master spark://spark-master:7077 \
--jars /opt/spark-apps/postgresql-42.2.22.jar \
--driver-memory 1G \
--executor-memory 1G \
/opt/spark-apps/main.py
```


Postgres:
```sh
docker exec -it prueba4-demo-dbin/bash
```
```sh
postgres=# psql -U postgres
postgres-# \c movilens
postgres-# SELECT * FROM movilens;

```


![alt text](./articles/images/pyspark-demo.png "Spark UI with pyspark program running")

## MTA Bus Analytics[Scala]

This program takes the archived data from [MTA Bus Time](http://web.mta.info/developers/MTA-Bus-Time-historical-data.html) and make some aggregations on it, the calculated results are persisted on postgresql tables.

Each persisted table correspond to a particullar aggregation:

Table|Aggregation
---|---
day_summary|A summary of vehicles reporting, stops visited, average speed and distance traveled(all vehicles)
speed_excesses|Speed excesses calculated in a 5 minute window
average_speed|Average speed by vehicle
distance_traveled|Total Distance traveled by vehicle


To submit the app connect to one of the workers or the master and execute:

```sh
/opt/spark/bin/spark-submit --deploy-mode cluster \
--master spark://spark-master:7077 \
--total-executor-cores 1 \
--class mta.processing.MTAStatisticsApp \
--driver-memory 1G \
--executor-memory 1G \
--jars /opt/spark-apps/postgresql-42.2.22.jar \
--conf spark.driver.extraJavaOptions='-Dconfig-path=/opt/spark-apps/mta.conf' \
--conf spark.executor.extraJavaOptions='-Dconfig-path=/opt/spark-apps/mta.conf' \
/opt/spark-apps/mta-processing.jar
```

You will notice on the spark-ui a driver program and executor program running(In scala we can use deploy-mode cluster)

![alt text](./articles/images/stats-app.png "Spark UI with scala program running")


# Summary

* We compiled the necessary docker image to run spark master and worker containers.

* We created a spark standalone cluster using 2 worker nodes and 1 master node using docker && docker-compose.

* Copied the resources necessary to run demo applications.

* We ran a distributed application at home(just need enough cpu cores and RAM to do so).

# Why a standalone cluster?

* This is intended to be used for test purposes, basically a way of running distributed spark apps on your laptop or desktop.

* This will be useful to use CI/CD pipelines for your spark apps(A really difficult and hot topic)

# Steps to connect and use a pyspark shell interactively

* Follow the steps to run the docker-compose file. You can scale this down if needed to 1 worker. 

```sh
docker-compose up --scale spark-worker=1
docker exec -it docker-spark-cluster_spark-worker_1 bash
apt update
apt install python3-pip
pip3 install pyspark
pyspark
```

# What's left to do?

* Right now to run applications in deploy-mode cluster is necessary to specify arbitrary driver port.

* The spark submit entry in the start-spark.sh is unimplemented, the submit used in the demos can be triggered from any worker
