#!/usr/bin/env python
# ----------------------------------------------------------------------
# Coding Challenge for Insight Data Engineering
# Name: Duc Nguyen
# Email: duc.nguyen@my.colby-sawyer.edu
# Github: 
# ----------------------------------------------------------------------

# import json module to handle tweets.txt
import json

# Initialize some constants
filename = "./tweet_input/tweets.txt"
month = {	"Jan": "01",
			"Feb": "02",
			"Mar": "03",
			"Apr": "04",
			"May": "05",
			"Jun": "06",
			"Jul": "07",
			"Aug": "08",
			"Sep": "09",
			"Oct": "10",
			"Nov": "11",
			"Dec": "12"		}	

# lists to track the 60-second interval
time_list = [] 			# tweets within last 60 seconds
hashtags_list = []		# hashtags within last 60 seconds
edges_list = [] 		# edges between hashtags within last
						# 60 seconds


def combine_time(tweet, tweet_time):
	""" Combine a fully formatted tweet (that has unicode
	removed and escape characters replaced) with time.

	:param tweet: a fully processed tweet
	:type tweet: string
	:param tweet_time: the time from json handle which is converted
					   from unicode to string
	:type tweet_time: string
	:returns: a formatted string of datetime
	:rtype: string
	"""
	
	return tweet + " (timestamp: " + tweet_time + ")";


def clean_unicode(tweet):
	""" Remove unicode characters from a raw tweet and notify whether the
	tweet has unicode characters

	:param tweet: a single tweet that needs to be formatted
	:type tweet: string or unicode
	:returns: formatted tweet with all unicode characters removed
	:rtype: string
	:returns: 1 or 0 to denote whether the tweet contains unicode or not
			  (respectively)
	:rtype: integer
	"""

	try:
		tweet = tweet.encode('ascii')
		return (tweet, 0)
	except:
		tweet = tweet.encode('ascii', 'ignore')
		return (tweet, 1)


def clean_escapes(tweet):
	""" Replace escape characters from a tweet that has unicode characters
	removed.

	:param tweet: a single tweet that needs to be formatted
	:type tweet: string (non-unicode)
	:returns: formatted tweet with all escape characters replaced
	:rtype: string
	"""

	result = """"""
	char_idx = 0

	# turn the tweet to raw string
	tweet = tweet.encode('string-escape')

	# clean escape characters:
	while char_idx < len(tweet):
		if ( tweet[char_idx] == '\\' ):
			if ( tweet[char_idx+1] == '\\' ):
				result += '\\'
				char_idx += 2
			elif ( (tweet[char_idx+1] == 'n') or
				   (tweet[char_idx+1] == 't') or
				   (tweet[char_idx+1] == 'r') ):
				result += ' '
				char_idx += 2
			elif ( tweet[char_idx+1] == '\'' ):
				result += "'"
				char_idx += 2
			continue
		else:
			result += tweet[char_idx]
			char_idx += 1

	return result


def clean_all(tweet):
	""" Remove unicode and replace escape characters from a raw tweet.

	:param tweet: a single tweet that needs to be formatted
	:type tweet: string or unicode
	:returns: formatted tweet with all unicode removed and escape characters replaced
	:rtype: string
	:returns: 1 or 0 to denote whether the tweet contains unicode or not
			  (respectively)
	:rtype: integer
	"""


	# check if a string contains unicode characters and strip unicode
	tweet, unicode_track = clean_unicode(tweet)

	# clean escape characters:
	tweet = clean_escapes(tweet)

	return (tweet, unicode_track)


def parse_time(string_time):
	""" Encode the string time to an integer for better compute
	the 60-second interval. The integer will look like
	YYYYMMDDHHmmSS. For example, Jan 02 2015 12:23:34
	will be encoded to 20150102122334.

	:param string_time: string of time, obtained from the API
	:type string_time: string
	:return: an integer representing that time
	:type: integer
	"""

	result = ""
	result += string_time[26:30] + month[string_time[4:7]] \
			+ string_time[8:10] + string_time[11:13]        \
			+ string_time[14:16] + string_time[17:19]

	return int(result)


def get_hashtags(list_of_json):
	""" Get all hashtags from the Twitter API hashtags.

	:param list_of_json: list of json hashtags in Twitter API,
						 can be obtained with
						 tweet[u'entities'][u'hashtags'] 
	:type list_of_json: list
	:return: a set of all of the hashtags or an empty set (when
			 the number of hashtags is smaller than 2)
	:rtype: set
	"""

	# if the tweet contains less than 2 hashtags, ignore
	if len(list_of_json) < 2:
		return set()
	
	result = set()
	for each_json in list_of_json:
		raw_hashtag = clean_unicode(each_json[u'text'])[0].lower()
		if raw_hashtag != '':
			result.add('#' + raw_hashtag)

	# check for the case that a tweet contain the same hashtag but
	# has different uppercases
	if len(result) >= 2:
		return result
	else:
		return set()


def edge_generator(list_of_hashtags):
	""" From a set of hashtags, generate a set of edges that
	connect those hashtags. For example, set([#hashtag1, #hashtag2,
	#hashtag3]) will generate set(set([#hashtag1, #hashtag2]),
	set([#hashtag1, #hashtag3]), set([#hastag2, #hashtag3])).

	:param list_of_hashtags: a set of hashtags
	:type list_of_hashtags: list or set
	:return: set of edges connecting the hashtags
	:type: set
	"""

	length = len(list_of_hashtags)

	if length < 2:
		return set()

	list_of_hashtags = list(list_of_hashtags)
	result = set()

	for idx1 in xrange(length):
		for idx2 in xrange(idx1+1, length):
			result.add(frozenset([list_of_hashtags[idx1],
								  list_of_hashtags[idx2]]))

	return result


def combine_sets(list_of_sets):
	""" Combine all the elements from all the sets in list_of_sets
	into one large set. For example, combine [set(set1, set2), set(),
	set(set1, set3), set(set4)] to set(set1, set2, set3, set4).

	:param list_of_sets: list of all the sets
	:type list_of_sets: list
	:return: set of all the sets
	:rtype: set
	"""

	result = set()
	for each_set in list_of_sets:
		result.update(each_set)

	return result


def compute_average_degree(n_edges, n_hashtags):
	""" Compute the average degree based on the total number of
	edges, and the total number of hashtags. Concretely,
		average_degree = (total_edges * 2) / (total_hashtags)

	:param n_edges: total number of edges in the graph
	:type n_edges: integer
	:param n_hashtags: total number of hashtags in the graph
	:type n_hashtags: integer
	:return: the average degree based on the above equation or 0.0
			 if n_edges == n_hashtags == 0
	:rtype: float
	"""

	try:
		return round((float( n_edges * 2 ) / n_hashtags), 2)
	except:
		return 0.0

processed_tweets = 0
if __name__ == '__main__':
	print "Begin..."
	with open('./tweet_output/ft1.txt', 'wb') as ft1:
		with open('./tweet_output/ft2.txt', 'wb') as ft2:
			with open(filename, 'rb') as f_read:
				# variable to track the number of tweets
				# that contain unicode characters
				num_unicode = 0

				# for each json in the text file, do:
				for each_line in f_read:

					# ignore non-tweets from the API
					if each_line[2:7] == 'limit': continue;

					# load the deserialized json
					each_line = json.loads(each_line)
					time = each_line[u'created_at'].encode('ascii', 'ignore')

					# get, write the clean tweet, and update num_unicode
					processed_tweet = clean_all(each_line[u'text'])
					ft1.write(combine_time(processed_tweet[0], time) + '\n')
					num_unicode += processed_tweet[1]

					# process the hashtags for each tweet
					hashtags = get_hashtags(each_line[u'entities'][u'hashtags'])
					hashtags_list.append(hashtags)
					edges_list.append(edge_generator(hashtags))

					# get the encoded current time, and the bound
					# for 60-second interval
					current_time = parse_time(time)
					check_time = current_time - 100
					time_list.append(current_time)

					# remove the item that is over 60 seconds
					for idx, item in enumerate(time_list):
						# to make it track items from 60 seconds, use >
						# to make it track only items that are over 60
						# seconds, use >=
						if item > check_time:
							time_list = time_list[idx:]
							hashtags_list = hashtags_list[idx:]
							edges_list = edges_list[idx:]
							break

					average_degree = compute_average_degree(
										len(combine_sets(edges_list)),
										len(combine_sets(hashtags_list)))
					ft2.write(str(average_degree) + '\n')


					processed_tweets += 1
					if (processed_tweets % 5000) == 0:
						print "Processed tweets: %d and counting.." % processed_tweets
					# raw_input()

				unicode_text = "The number of tweets that contain "
				unicode_text += "unicode characters is %d" % num_unicode
				ft1.write(unicode_text)
				print "Done!"