#!/usr/bin/python3


# =====================================================================
# Adicional Functions
# =====================================================================

def is_valid_ip(ip_in_string):
	octets = ip_in_string.split('.')
	if(len(octets) != 4):
		return False
	for octet in octets:
		try:
			digit = int(octet)
			if(digit < 0 or digit > 254):
				return False
		except:
			return False
	return True


