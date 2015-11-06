""" Tweets random generators """
# Generate random tweets with random hashtags from hashtag1 to hashtag10
# Generate a random amount of hashtag for each tweet

import random

time = '"Thu Oct 29 17:51:50 +0000 2015"'
hashtag_format = '{"text":"%s","indices":[73,78]}'
time_format = '"Thu %s %s %s:%s:%s +0000 2015"'
message_format = """{"created_at":%s,"text":%s,"entities":{"hashtags":[%s]}}"""

month = ['Oct', 'Nov', 'Dec']

day = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
	   '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
	   '21', '22', '23', '24', '25', '26', '27', '28', '29', '30']

hour = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
	   '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
	   '21', '22', '23']

minute = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
	   	  '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
	   	  '21', '22', '23', '24', '25', '26', '27', '28', '29', '30',
	   	  '31', '32', '33', '34', '35', '36', '37', '38', '39', '40',
	   	  '41', '42', '43', '44', '45', '46', '47', '48', '49', '50',
	   	  '51', '52', '53', '54', '55', '56', '57', '58', '59']

second = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
	   	  '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
	   	  '21', '22', '23', '24', '25', '26', '27', '28', '29', '30',
	   	  '31', '32', '33', '34', '35', '36', '37', '38', '39', '40',
	   	  '41', '42', '43', '44', '45', '46', '47', '48', '49', '50',
	   	  '51', '52', '53', '54', '55', '56', '57', '58', '59']

month_idx = 1;
day_idx = 1;
hour_idx = 1;
minute_idx = 1;
second_idx = 1;
n = 0;



with open("./example_tweets.txt", 'wb') as f:
	while n <= 1000: 		# number of tweets
		n += 1
		result_text = ''
		result_hashtag = ''
		result_time = ''
		result_message = ''

		# amount of hashtag
		amount_of_hashtag = range(4)
		random_amount = random.choice(amount_of_hashtag)


		# possible hashtag
		possible_hashtags = ["#hashtag" + str(x) for x in range(1,11)]


		# picked random_amount of hashtag from list of possible_hashtags
		picked = random.sample(possible_hashtags, random_amount)
		for idx, item in enumerate(picked):
			if idx == (len(picked) - 1):
				result_text += item + ' '
				result_hashtag += hashtag_format % item
			else:
				result_text += item + ' '
				result_hashtag += hashtag_format % item
				result_hashtag += ','

		result_text = '"' + result_text + '"'
		# print result_text
		# print result_hashtag

		# time
		second_idx = (second_idx + 1) % len(second)
		if second_idx == 0:
			minute_idx = (minute_idx + 1) % len(minute)
			if minute_idx == 0:
				hour_idx = (hour_idx + 1) % len(hour)
				if hour_idx == 0:
					day_idx = (day_idx + 1) % len(day)
					if day_idx == 0:
						month_idx = (month_idx + 1) % len(month)

		result_time = time_format % (month[month_idx], day[day_idx], hour[hour_idx], minute[minute_idx], second[second_idx])
		
		result_message = message_format % (result_time, result_text, result_hashtag)
		result_message += '\n'
		f.write(result_message)
