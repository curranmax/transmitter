from socket import *
import time
import argparse


def main(port,msg,wait_time,addr):
	sock = socket(AF_INET,SOCK_DGRAM)
	sock.bind(('',port))

	while True:
		sock.sendTo(msg,addr)
		time.sleep(wait_time)

if __name__ == '__main__':
	parser.add_argument('-lp','--local_port',metavar = 'LP',type = int,nargs = 1,default = [9999],help = 'Local port to send messages from ')
	parser.add_argument('-fp','--foreign_port',metavar = 'TP',type = int,nargs = 1,default = [9898],help = 'Port to send messages to')
	parser.add_argument('-ip','--foreign_ip_addres',metavar = 'IP',type = str,nargs = 1,default = ['<broadcast>'],help = 'IP address to send to')
	parser.add_argument('-t','--wait_time',metavar = 'T',type = float,nargs = 1,default = [1.0],help = 'Time between sending messages')
	parser.add_argument('-msg','--message',metavar = 'MSG',type = str,nargs = 1,default = ['A' * 16],help = 'Message to send repeatedly')

	args = parser.parse_args()
	
	lp = args.local_port[0]
	fp = args.test_port[0]
	ip = args.foreign_ip_addres[0]
	t = args.wait_time[0]
	msg = args.message[0]

	main(lp,msg,t,(ip,fp))
