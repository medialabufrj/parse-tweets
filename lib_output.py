#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module defines some functions used to output the results of the script.
The constants used in it are:
	* MAX_WORDS_NUMBER_CSV: maximum number of words to be present in 
	the top_words.csv file;
	* MAX_WORDS_NUMBER_WORDCLOUD: maximum number of words to be in the TXT
	file that will be used to generate the wordcloud;
"""
import csv
import sys

DEFAULT_OUTPUT_DELIMITER = '|'

MAX_WORDS_NUMBER_CSV = 1000
MAX_WORDS_NUMBER_WORDCLOUD = 120

def normalize_dict(dict_str_int_wordcount):
	""" 
	Normalize the dictionary with the word count to generate the wordcloud.
	Normalizing, in this function, is give the most recurring word the value 100 and give
	all the other values proportional to it.
	"""
	max_elem = max(dict_str_int_wordcount.values())
	for key, value in dict_str_int_wordcount.items():
		normalized_val = int((100 * value)/max_elem)
		if normalized_val == 0:
			normalized_val = 1
		dict_str_int_wordcount[key]= normalized_val
	return dict_str_int_wordcount


def dict_to_txt_for_wordle(dict_str_int_wordcount, filename, sort_key=lambda t:t, value_key=lambda t:t):
	"""
	Writes the normalized dict in a txt to be pasted manually 
	in wordle.net or another wordcloud service
	Entries in the dict_str_int_wordcount dictionary are in the format "string_word => integer_count"
	i.e.: "chocolate => 10000"
	"""
	if not dict_str_int_wordcount:
		dict_str_int_wordcount = {'No hashtags found': 1}
	ordered_list = []
	dict_str_int_wordcount = normalize_dict(dict_str_int_wordcount)
	for key, value in dict_str_int_wordcount.items():
		ordered_list.append([key, value_key(value)])	
	ordered_list = 	sorted(ordered_list, key=sort_key, reverse=True)	
	out = open(filename, 'w', encoding= 'utf-8')
	for item in ordered_list[:MAX_WORDS_NUMBER_WORDCLOUD]:		
		i = 0
		while i < item[1]:
			out.write(item[0] + ' ')
			i+=1	
	out.close()

def locations_to_csv(dict_str_tuple, filename='locations.csv'):
	"""
	Creates a CSV file of the latitude and longitude data of the tweets
	param: dict_str_tuple is a dictionary where each entry is in 
	the format "string_username => ('latitude', 'longitute')
	i.e: ronald0 => ('0.012081210', '0.9121218298172')
	"""
	with open(filename, 'w', newline='', encoding="utf8") as csvfile:
		file_writer = csv.writer(csvfile, delimiter=DEFAULT_OUTPUT_DELIMITER, quotechar='"', quoting=csv.QUOTE_MINIMAL)
		file_writer.writerow(['latitude', 'longitute'])
		for key, value in dict_str_tuple.items():
			file_writer.writerow([value[0], value[1]])
		csvfile.close()


def hashtags_relations_to_csv(list_tuple_hashtags, filename='hashtags_network.csv'):
	"""
	Generates a file to be used by Gephi to create a graph of 
	the relations between the hashtags.	
	"""
	with open(filename, 'w', newline='', encoding="utf8") as csvfile:
		file_writer = csv.writer(csvfile, delimiter=DEFAULT_OUTPUT_DELIMITER, quotechar='"', quoting=csv.QUOTE_MINIMAL)
		file_writer.writerow(['hashtag_1', 'hashtag_2'])
		for hashtag_tuple in list_tuple_hashtags:
			file_writer.writerow([hashtag_tuple[0], hashtag_tuple[1]])
		csvfile.close()

def top_something_to_csv(dict_in, filename, column_titles, reverse, sort_key_function, value_format_function=lambda t: t):
	"""
	Given a dictionary, a sorting function for it's keys
	a value format function to format the output, this function generates
	a CSV file with the ordered by the keys with the key as the first column 
	and the value as the second. The file can be ordered in reverse.
	"""
	ordered_list = []
	for key, value in dict_in.items():
		ordered_list.append([key, value_format_function(value)])
	ordered_list = sorted(ordered_list, key=sort_key_function, reverse=reverse)
	with open(filename, 'w', newline='', encoding="utf8") as csvfile:
		file_writer = csv.writer(csvfile, delimiter=DEFAULT_OUTPUT_DELIMITER, quotechar='"', quoting=csv.QUOTE_MINIMAL)	
		file_writer.writerow(column_titles)
		for item in ordered_list[:MAX_WORDS_NUMBER_CSV]:
			file_writer.writerow([item[0], item[1]])
		csvfile.close()

def error_parsing(line_num):
	""" Returns an error message with the corrupted text and exits the program."""
	print("Error on line: "+ str(line_num))	
	print("Error: Not all tweeted were read. Finishing execution...")
	sys.exit()

