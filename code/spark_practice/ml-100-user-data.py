from pyspark import SparkContext
sc = SparkContext("local[2]","python_test")
user_data = sc.textFile("file:///usr/hadoop/lijun/data/ml-100k/u.user")
user_fields = user_data.map(lambda line:line.split("|"))
num_users = user_fields.map(lambda fields:fields[0]).count()
num_genders = user_fields.map(lambda fields:fields[2]).distinct().count()
num_occupations = user_fields.map(lambda fields:fields[3]).distinct().count()
num_zipcodes = user_fields.map(lambda fields:fields[4]).distinct().count()
text_file = open("/usr/hadoop/lijun/code/output/testOutput","w")

text_file.write("Users:"+str(num_users)+" ,genders:, occupation:")
text_file.close()

                                                                        