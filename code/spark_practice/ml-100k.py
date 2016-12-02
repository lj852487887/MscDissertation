
# coding: utf-8

# In[1]:

user_data = sc.textFile("./data/ml-100k/u.user")
user_fields = user_data.map(lambda line:line.split("|"))
num_users = user_fields.map(lambda fields:fields[0]).count()
num_genders = user_fields.map(lambda fields:fields[2]).distinct().count()
num_occupations = user_fields.map(lambda fields:fields[3]).distinct().count()
num_zipcodes = user_fields.map(lambda fields:fields[4]).distinct().count()
print "Users:",num_users,",genders:",num_genders,",occupations:",num_occupations,",zip codes:",num_zipcodes


# In[2]:

import matplotlib.pyplot as plt
get_ipython().magic('matplotlib inline')
ages = user_fields.map(lambda x:int(x[1])).collect()
plt.hist(ages,bins=20,color='lightblue',normed=True)
fig = plt.gcf()
fig.set_size_inches(16,10)


# In[3]:

import numpy as np
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


# In[4]:

count_by_occupation2 = user_fields.map(lambda fields: fields[3]).countByValue()
print "Map-reduce approach:"
print dict(count_by_occupation2)
print ""
print "countByValue approach:"
print dict(count_by_occupation)


# In[5]:

movie_data = sc.textFile("%s/ml-100k/u.item" % "./data")
print movie_data.first()
num_movies = movie_data.count()
print "Movies: %d" % num_movies


# In[6]:

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


# In[7]:

rating_data_raw = sc.textFile("%s/ml-100k/u.data" % "./data")
print rating_data_raw.first()
num_ratings = rating_data_raw.count()
print "Ratings: %d" % num_ratings


# In[8]:

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


# In[9]:

ratings.stats()


# In[10]:

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


# In[11]:

# to compute the distribution of ratings per user, we first group the ratings by user id
user_ratings_grouped = rating_data.map(lambda fields: (int(fields[0]), int(fields[2]))).groupByKey() 
# then, for each key (user id), we find the size of the set of ratings, which gives us the # ratings for that user 
user_ratings_byuser = user_ratings_grouped.map(lambda (k, v): (k, len(v)))
user_ratings_byuser.first()


# In[12]:

user_ratings_byuser_local = user_ratings_byuser.map(lambda (k, v): v).collect()
plt.hist(user_ratings_byuser_local, bins=200, color='lightblue', normed=False)
fig = plt.gcf()
fig.set_size_inches(16,10)


# In[13]:

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


# In[14]:

all_occupations = user_fields.map(lambda fields: fields[3]).distinct().collect()
all_occupations.sort()
idx = 0
all_occupations_dict = {}
for o in all_occupations:
    all_occupations_dict[o] = idx
    idx +=1
print "encoding of doctor : %d" % all_occupations_dict['doctor']
print "encoding of programer : %d" % all_occupations_dict['programmer']


# In[15]:

k = len(all_occupations_dict)
binary_x = np.zeros(k)
k_programmer = all_occupations_dict['programmer']
binary_x[k_programmer]=1
print "binary feature vector: %s" % binary_x
print "length of binary vector: %d" % k


# In[16]:

def extract_datetime(ts):
    import datetime
    return datetime.datetime.fromtimestamp(ts)
timestamps = rating_data.map(lambda fields: int(fields[3]))
hour_of_day = timestamps.map(lambda ts:extract_datetime(ts).hour)
hour_of_day.take(5)


# In[17]:

# a function for assigning "time-of-day" bucket given an hour of the day
def assign_tod(hr):
    times_of_day = {
                'morning' : range(7, 12),
                'lunch' : range(12, 14),
                'afternoon' : range(14, 18),
                'evening' : range(18, 22),
                'night' : range(22,24),
                'over-night' : range(0,7)
                }
    for k, v in times_of_day.iteritems():
        if hr in v: 
            return k

# now apply the "time of day" function to the "hour of day" RDD
time_of_day = hour_of_day.map(lambda hr: assign_tod(hr))
time_of_day.take(5)


# In[18]:

# we define a function to extract just the title from the raw movie title, removing the year of release
def extract_title(raw):
    import re
    grps = re.search("\((\w+)\)", raw)    # this regular expression finds the non-word (numbers) between parentheses
    if grps:
        return raw[:grps.start()].strip() # we strip the trailing whitespace from the title
    else:
        return raw

# first lets extract the raw movie titles from the movie fields
raw_titles = movie_fields.map(lambda fields: fields[1])
# next, we strip away the "year of release" to leave us with just the title text
# let's test our title extraction function on the first 5 titles
for raw_title in raw_titles.take(5):
    print extract_title(raw_title)


# In[19]:

# ok that looks good! let's apply it to all the titles
movie_titles = raw_titles.map(lambda m: extract_title(m))
# next we tokenize the titles into terms. We'll use simple whitespace tokenization
title_terms = movie_titles.map(lambda t: t.split(" "))
print title_terms.take(5)


# In[20]:

# next we would like to collect all the possible terms, in order to build out dictionary of term <-> index mappings
all_terms = title_terms.flatMap(lambda x: x).distinct().collect()
# create a new dictionary to hold the terms, and assign the "1-of-k" indexes
idx = 0
all_terms_dict = {}
for term in all_terms:
    all_terms_dict[term] = idx
    idx +=1
num_terms = len(all_terms_dict)
print "Total number of terms: %d" % num_terms
print "Index of term 'Dead': %d" % all_terms_dict['Dead']
print "Index of term 'Rooms': %d" % all_terms_dict['Rooms']


# In[21]:

# we could also use Spark's 'zipWithIndex' RDD function to create the term dictionary
all_terms_dict2 = title_terms.flatMap(lambda x: x).distinct().zipWithIndex().collectAsMap()
print "Index of term 'Dead': %d" % all_terms_dict2['Dead']
print "Index of term 'Rooms': %d" % all_terms_dict2['Rooms']


# In[22]:


np.random.seed(42)
x = np.random.randn(10)
norm_x_2 = np.linalg.norm(x)
normalized_x = x / norm_x_2
print "x:\n%s" % x
print "2-Norm of x: %2.4f" % norm_x_2
print "Normalized x:\n%s" % normalized_x
print "2-Norm of normalized_x: %2.4f" % np.linalg.norm(normalized_x)


# In[23]:

from pyspark.mllib.feature import Normalizer
normalizer = Normalizer()
vector = sc.parallelize([x])
normalized_x_mllib = normalizer.transform(vector).first().toArray()

print "x:\n%s" % x
print "2-Norm of x: %2.4f" % norm_x_2
print "Normalized x MLlib:\n%s" % normalized_x_mllib
print "2-Norm of normalized_x_mllib: %2.4f" % np.linalg.norm(normalized_x_mllib)


# In[24]:

def create_vector(terms, term_dict):
    from scipy import sparse as sp
    x = sp.csc_matrix((1, num_terms))
    for t in terms:
        if t in term_dict:
            idx = term_dict[t]
            x[0, idx] = 1
    return x
all_terms_bcast = sc.broadcast(all_terms_dict)
term_vectors = title_terms.map(lambda terms: create_vector(terms, all_terms_bcast.value))
term_vectors.take(5)


# In[ ]:



