from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import os

# 1. Critical Windows Fix: Point to your winutils folder
os.environ['HADOOP_HOME'] = "C:/hadoop"

# 2. Wrap the builder in ( ) so the dots work on new lines
spark = (SparkSession.builder
    .appName("MyFirstLocalJob")
    .master("local[*]")
    .config("spark.driver.bindAddress", "127.0.0.1")
    .getOrCreate())

data = [("Laptop", "Electronics", 1200), 
        ("Phone", "Electronics", 800), 
        ("Coffee Maker", "Kitchen", 150), 
        ("Toaster", "Kitchen", 50)]

columns = ["Product", "Category", "Price"]

df = spark.createDataFrame(data, columns)

# 3. Again, wrap the transformation in ( ) or keep it on one line
result = (df.filter(col("Price") > 100)
            .groupBy("Category")
            .count())

print("\n--- Sales Count by Category (Price > 100) ---")
result.show()

print("Spark is running. Check http://localhost:4040 in your browser.")
print("Press Enter to stop...")
input()

spark.stop()