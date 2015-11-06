Insight Data Engineering - Coding Challenge
===========================================================

## Repo Summary

This is my submission for the Insight Data Engineering's Coding Challenge. The structure of this repo is as follow:

	├── README.md  
	├── run.sh  
	├── src  
	│   └── run_program.py  
	├── tweet_input  
	│   └── tweets.txt  
	└── tweet_output  
	    ├── ft1.txt  
	    └── ft2.txt  


## Operating Instruction

1. Clone this repo
2. cd to the newly created directory
3. Run: bash run.sh, and the file ft1.txt and ft2.txt will be created in the folder ./tweet_output


## Additional Information

1. This script is written using Python 2.7.10
2. It uses Python's built-in json module to handle tweets.txt
3. To run the run.sh file, "chmod +x run.sh" might be needed
4. Regarding the 60-second interval: the tweets, which are at least 61 second away, counting from the latest tweet, will be evicted. For example, if Tweet1 arrives at 15:02:05, then when another tweet arrives at 15:03:05, Tweet1 will be evicted
5. Regarding hashtags that contain only unicode characters: these hashtags will be empty after Unicode cleaning, hence they will be ignored and will not be counted into the Twitter hashtag graph