Using graphx with pyspark.

It is not easy to work with graphx with pyspark.
People should use Scala for a better experience.

However, this are the folowing steps

1. Download the graphframes jar
2. Unjar it
3. Zip it
4. Run using pyspark 
> pyspark --py-files graphframes.zip     --packages graphframes:graphframes:0.6.0-spark2.3-s_2.11


One might have to use sc.addPyFile("graphframes.zip")
