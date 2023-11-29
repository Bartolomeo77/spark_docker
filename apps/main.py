from pyspark.sql import SparkSession
from pyspark.sql.functions import col,date_format

def init_spark():
  sql = SparkSession.builder\
    .appName("trip-app")\
    .config("spark.jars", "/opt/spark-apps/postgresql-42.2.22.jar")\
    .getOrCreate()
  sc = sql.sparkContext
  return sql,sc

def main():
  url = "jdbc:postgresql://demo-database:5432/movilens"
  properties = {
    "user": "postgres",
    "password": "casa1234",
    "driver": "org.postgresql.Driver"
  }
  file = "/opt/spark-data/u.data"
  sql,sc = init_spark()

  df = sql.read.load(file, format="csv", inferSchema="true", sep="\t", header=False) \
        .withColumnRenamed("_c0", "userid") \
        .withColumnRenamed("_c1", "movieid") \
        .withColumnRenamed("_c2", "ratingid") \
        .withColumnRenamed("_c3", "timeid")

  # Filter invalid coordinates
  df.write \
        .jdbc(url=url, table="movilens", mode='append', properties=properties) 

  
if __name__ == '__main__':
  main()
