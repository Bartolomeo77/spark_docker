from pyspark import SparkConf, SparkContext

# Configurar la aplicación Spark
conf = SparkConf().setAppName("HolaMundo").setMaster("local[1]")

# Crear el contexto Spark
sc = SparkContext(conf=conf)
# Leer el archivo de datos de calificaciones
lines = sc.textFile("../data/u.data")

ratings = lines.map(lambda x: x.split('\t')[2])  

result = ratings.countByValue()

# Mostrar el resultado
print("Frecuencia de Calificaciones:")
sorted_result = sorted(result.items())

for key, value in sorted_result:
    print(f"Calificación {key}: {value} ocurrencias")
    
# Cambiar el nombre de la variable en el bucle for
for line in lines.take(5):
    print(line)
