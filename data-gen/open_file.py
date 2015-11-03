filename = "tweets.txt"

def get_time(tweet):
	""" Print out the time of each tweet """

	if tweet[15:17] == 'k"':
		return
	else:
		return " (timestamp: " + tweet[15:45] + ")"

# for tweet in tweets:
# 	print get_time(tweet)


def get_text(tweet):
	""" Print out the text message """
	raw_tweet = tweet[109:500].encode('string-escape');
	# print raw_tweet; print
	result = '';
	
	if tweet[15:17] == 'k"':
		return
	else:
		idx = 0
		while True:
			if (raw_tweet[idx] == '\\'):
				if raw_tweet[idx+1:idx+3] == '\u':
					idx += 7
				elif raw_tweet[idx+1:idx+3] == '\/':
					idx += 3
				else:
					idx += 2;
				continue;
			elif (raw_tweet[idx] == '"'):
				break
			else:
				result += raw_tweet[idx];
				idx += 1;
	return result


def sync(tweet):
	return get_text(tweet) + get_time(tweet)

processed = 0
with open('test.txt', 'wb') as f_write:
	with open(filename, 'rb') as f_read:
		for each_line in f_read:
			f_write.write(sync(each_line)+'\n')
			processed += 1
			print "Processed tweets:", processed
