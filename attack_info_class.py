class Attack_info(object):
	def __init__(self, site, field, known_value, method):
		self.site = site
		self.field = field
		self.known_value = known_value
		self.method = method
		self.sleep_time = 0.000000
		self.comments_needed = False
		self.quote_needed = False
		self.show_payload = False
	
	def set_sleep_time(self, sleep_time):
		self.sleep_time = sleep_time
		
	def set_comments_needed(self, comments_needed):
		self.comments_needed = comments_needed
	
	def set_quote_needed(self, quote_needed):
		self.quote_needed = quote_needed
	
	def set_show_payload(self, show_payload):
		self.show_payload = show_payload
