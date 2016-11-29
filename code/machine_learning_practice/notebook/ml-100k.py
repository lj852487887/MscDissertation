import matplotlib.pyplot as plt
import numpy as np
%matplotlib inline

user_data = sc.textFile("./data/ml-100k/u.user")
user_fields = user_data.map(lambda line:line.split("|"))
num_users = user_fields.map(lambda fields:fields[0]).count()
num_genders = user_fields.map(lambda fields:fields[2]).distinct().count()
num_occupations = user_fields.map(lambda fields:fields[3]).distinct().count()
num_zipcodes = user_fields.map(lambda fields:fields[4]).distinct().count()
print "Users:",num_users,",genders:",num_genders,",occupations:",num_occupations,",zip codes:",num_zipcodes



ages = user_fields.map(lambda x:int(x[1])).collect()
plt.hist(ages,bins=20,color='lightblue',normed=True)
fig = plt.gcf()
fig.set_size_inches(16,10)




count_by_occupation = user_fields.map(lambda fields: (fields[3], 1)).reduceByKey(lambda x, y: x + y).collect()
x_axis1 = np.array([c[0] for c in count_by_occupation])
y_axis1 = np.array([c[1] for c in count_by_occupation])
x_axis = x_axis1[np.argsort(y_axis1)]
y_axis = y_axis1[np.argsort(y_axis1)]

pos = np.arange(len(x_axis))
width = 1.0

ax = plt.axes()
ax.set_xticks(pos + (width / 2))
ax.set_xticklabels(x_axis)

plt.bar(pos, y_axis, width, color='lightblue')
plt.xticks(rotation=30)
fig = plt.gcf()
fig.set_size_inches(16, 10)






count_by_occupation2 = user_fields.map(lambda fields: fields[3]).countByValue()
print "Map-reduce approach:"
print dict(count_by_occupation2)
print ""
print "countByValue approach:"
print dict(count_by_occupation)



movie_data = sc.textFile("%s/ml-100k/u.item" % "./data")
print movie_data.first()
num_movies = movie_data.count()
print "Movies: %d" % num_movies



def convert_year(x):
    try:
        return int(x[-4:])
    except:
        return 1900 
movie_fields = movie_data.map(lambda lines: lines.split("|"))
years = movie_fields.map(lambda fields: fields[2]).map(lambda x: convert_year(x))
years_filtered = years.filter(lambda x: x != 1900)
movie_ages = years_filtered.map(lambda yr: 1998-yr).countByValue()
values = movie_ages.values()
bins = movie_ages.keys()
plt.hist(values, bins=bins, color='lightblue', normed=True)
fig = plt.gcf()
fig.set_size_inches(16,10)



rating_data = rating_data_raw.map(lambda line: line.split("\t"))
ratings = rating_data.map(lambda fields: int(fields[2]))
max_rating = ratings.reduce(lambda x, y: max(x, y))
min_rating = ratings.reduce(lambda x, y: min(x, y))
mean_rating = ratings.reduce(lambda x, y: x + y) / float(num_ratings)
median_rating = np.median(ratings.collect())
ratings_per_user = num_ratings / num_users
ratings_per_movie = num_ratings / num_movies
print "Min rating: %d" % min_rating
print "Max rating: %d" % max_rating
print "Average rating: %2.2f" % mean_rating
print "Median rating: %d" % median_rating
print "Average # of ratings per user: %2.2f" % ratings_per_user
print "Average # of ratings per movie: %2.2f" % ratings_per_movie


ratings.stats()


count_by_rating = ratings.countByValue()
x_axis = np.array(count_by_rating.keys())
y_axis = np.array([float(c) for c in count_by_rating.values()])
y_axis_normed = y_axis / y_axis.sum()

pos = np.arange(len(x_axis))
width = 1.0

ax = plt.axes()
ax.set_xticks(pos + (width / 2))
ax.set_xticklabels(x_axis)

plt.bar(pos, y_axis_normed, width, color='lightblue')
plt.xticks(rotation=30)
fig = plt.gcf()
fig.set_size_inches(16, 10)



# to compute the distribution of ratings per user, we first group the ratings by user id
user_ratings_grouped = rating_data.map(lambda fields: (int(fields[0]), int(fields[2]))).groupByKey() 
# then, for each key (user id), we find the size of the set of ratings, which gives us the # ratings for that user 
user_ratings_byuser = user_ratings_grouped.map(lambda (k, v): (k, len(v)))
user_ratings_byuser.first()


user_ratings_byuser_local = user_ratings_byuser.map(lambda (k, v): v).collect()
plt.hist(user_ratings_byuser_local, bins=200, color='lightblue', normed=False)
fig = plt.gcf()
fig.set_size_inches(16,10)


years_pre_processed = movie_fields.map(lambda fields: fields[2]).map(lambda x: convert_year(x)).collect() 
years_pre_processed_array = np.array(years_pre_processed) 
mean_year = np.mean(years_pre_processed_array[years_pre_processed_array!=1990])
median_year = np.median(years_pre_processed_array[years_pre_processed_array!=1990])
index_bad_data = np.where(years_pre_processed_array==1990)[0]
print np.where(years_pre_processed_array==1990)[0]
years_pre_processed_array[index_bad_data] = median_year
print "mean year of release: %d" % mean_year
print "median year of release: %d" % median_year
print "index of '1990' after assigning median: %s" % np.where(years_pre_processed_array==1990)[0]















