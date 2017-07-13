import string
import random

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def generate_boundary():
	return "ASYNCREQUESTS_BOUNDARY-%s-ASYNCREQUESTS_BOUNDARY" % id_generator(12)

def has_file(data):
	for key, value in data.items():
		if is_file(value):
			return True
	return False

def is_file(obj):
	invert_op = getattr(obj, "read", None)
	if callable(invert_op):
		return True
	return False

def read_inside(obj):
	if is_file(obj):
		return obj.read()
	elif isinstance(obj, str):
		return obj

def generate_body_multipart_form_data(data, boundary):
	part_starter = "--%s\n" % boundary
	body = ""
	for key, value in data.items():
		body += part_starter
		if is_file(value):
			body += ('Content-Disposition: form-data; name="%s"; filename="%s"\n\n'
								% (key, value.name))
			body += value.read();body += "\n"
		else:
			body += 'Content-Disposition: form-data; name="%s"\n\n' % key
			body += "%s\n" % value 
	body += "--%s--" % boundary
	return body

if __name__ == "__main__":
	print(has_file({'test': open('test.py', 'r')}))
	print(generate_boundary())
