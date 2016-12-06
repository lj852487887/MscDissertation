import org.elasticsearch.spark._

val sc = new SparkContext(new SparkConf())
val rdd = sc.esRDD("radio/artists","!me*")

#####################################

import org.elasticsearch.spark._

case class Artist(name: String,albums:Int) 

val u2 = Artist("U2",12)
val h2 = Map("name"->"Buckethead","albums"->95,"age"->45)

sc.makeRDD(Seq(u2,h2)).saveToEs("radio/artists")