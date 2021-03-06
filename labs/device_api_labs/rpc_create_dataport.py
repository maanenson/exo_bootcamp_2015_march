#==============================================================================
# rpc_read_examples.py
# Python script that calls the read rpc different ways to show the flexibility
# of this read function.  Although this is python, is written to use socket calls
# instead of a python HTTP module to focus on the API usage and how it could be used 
# for any code base.
#
# Note: Does not use Exosite's Pyonep python library 
# 
# Assumptions:
# 1) Have a Client (device) in Exosite with a CIK (Client Identifier Key)
# 2) That client must have a dataport with an alias like ('output') which must be specified below
# 3) The dataport should have data otherwise the responses won't have any values
#
#==============================================================================
## Tested with python 2.6.5
##
## Copyright (c) 2010, Exosite LLC
## All rights reserved.
##
## For License see LICENSE file

import socket
import sys
import ssl
import json
import time


cik = '880aa2a319224c120210d2c3ff33338f2a0974b5'   # PUT THE DEVICE CIK HERE
dataport_alias = 'output'  # PUT THE DATA PORT ALIAS HERE
host = 'm2.exosite.com'

#
# Function: 'sendRPC'
# This is a wrapper function that takes the JSON object and sends it using 
# HTTPS to Exosite's API Servers.  
#
def sendRPC(rpc_object):

	# CONVERT JSON OBJECT TO A STRING
	jsonstring = json.dumps(rpc_object,separators=(',', ':'))

	# CREATE HTTP PACKET STRING
	packetstring = ""
	packetstring += 'POST /api:v1/rpc/process HTTP/1.1\r\n'
	packetstring += 'Host: '+host+'\r\n'
	packetstring += 'Content-Type: application/json; charset=utf-8\r\n'
	packetstring += 'Content-Length: '+ str(len(jsonstring)) +'\r\n'
	packetstring += '\r\n'
	packetstring += jsonstring

	print ''
	print '========================================================================'
	print 'JSON RPC HTTP POST' 
	print '========================================================================'

	# OPEN SOCKET
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# USE HTTPS (SSL)
	ssl_s = ssl.wrap_socket(s)
	ssl_s.connect((host, 443))

	# SEND REQUEST
	ssl_s.send(packetstring)

	print ''
	print 'Request:'
	print '---------------------'
	print packetstring
	print '---------------------'
	# RECEIVE RESPONSE
	data = ssl_s.recv(2048)
	# CLOSE SOCKET
	ssl_s.close()

	print ''
	print 'Response:'
	print '---------------------'
	print str(data)
	print '---------------------\r\n'
	print '\r\n\r\n'



#
# Example 1 - Read the last value from current time
#

jsoncontent = {
    "auth": { "cik": cik }, 
    "calls": [
        {
            "id": 1, 
            "procedure": "create",
            "arguments": [
	            "dataport", 
	            	{ 
									"format": "string", 
									"subscribe": "", 
									"preprocess": [], 
									"retention": { "count": "infinity", "duration": "infinity" }  
								} 
						]
        }
      ]
}

sendRPC(jsoncontent)










