#Student Name: MA Mingyu
#Student ID: 14110562D

#TCPServer - Message in one by one approach

import socket, sys
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = '127.0.0.1' #localhost
PORT = 8888 	   

def recv_all(sock, length): #use this function to read the message
	data = ''
	while len(data) < length:
		more = sock.recv(length - len(data))
		if not more:
			raise EOFError('socket closed %d bytes into a %d-byte message'
							% (len(data), length))
		data += more
	return data

def stopOrNot(message): #use this function to judge the return is "BYEBYE" or not
    if message == "BYEBYE":
        return True
    else:
        return False

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(1)

print 'Listening at', s.getsockname()
sc, sockname = s.accept() #wait here until there is a request

#Use while loop to repeat the action again and again
while True:
        #This part get the message from client
	msg_length = int(recv_all(sc, 3)) #get the length of the message first
	message = recv_all(sc, msg_length) #get the 'real' message with proper length
	print 'Client: ', repr(message)

        #This part judge wheather need to stop the program
        if stopOrNot(message) == True: #if need to stop
            #This part send "BYEBYE" back to client
            msg = 'BYEBYE'
            msg_length_in_str = str(len(msg))
            msg_length_in_str = msg_length_in_str.zfill(3)
            sc.sendall(msg_length_in_str + msg)
            break #break the loop to close the socket
        else: #if do not need to stop
            #This part get the input from user and return to client
            msg = raw_input('Message: ')
            #determine the message length (max 255 characters, i.e. 3 digits), pad with leading zeroes
            msg_length_in_str = str(len(msg))
            msg_length_in_str = msg_length_in_str.zfill(3)#zfill autofill 0
            sc.sendall(msg_length_in_str + msg)

sc.close()
