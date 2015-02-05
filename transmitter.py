from socket import *
import subprocess
import signal
import argparse

class TransmitterServer:
	def __init__(self,sock,local_test_port,verbose):
		self.sock = sock
		self.v = verbose
		self.local_test_port = None
		self.foreign_test_port = None
		self.to_ip = None
		self.msg_char = None
		self.msg_len = None
		self.msg = None
		self.norm_wt = None
		self.proc = None
		self.loop = True

	def run(self):
		while self.loop:
			data,addr = self.sock.recvfrom(256)
			if self.v:
				print 'Recv [' + data + '] from',addr
			self.to_ip = addr[0]
			ack_msg = self.process(data)
			self.sock.sendto(ack_msg,addr)
			if self.v:
				print 'Sent [' + ack_msg + '] to',addr

	def processParams(self,nvs):
		nvs = [tuple(nv.split('=')) for nv in nvs]
		self.msg,self.msg_len,self.msg_char,self.norm_wt = None,None,None,None
		for n,v in nvs:
			if n == 'msg_char':
				self.msg_char = v
			if n == 'msg_len':
				self.msg_len = int(v)
			if n == 'msg':
				self.msg = v
			if n == 'norm_wt':
				self.norm_wt = v
		if self.msg == None:
			if self.msg_len == None or self.msg_char == None:
				return False
			else:
				self.msg = self.msg_char * self.msg_len
		return True

	def process(self,data):
		spl = data.split()
		if spl[0] == 'start_test' and len(spl) >=2:
			self.foreign_test_port = int(spl[1])
			self.endTest()
		elif spl[0] == 'test_params' and len(spl) >=2:
			if not self.processParams(spl[1:]):
				return 'unknown_msg'
			self.endTest()
			self.startTest()
		elif spl[0] == 'end_test':
			self.endTest()
		elif spl[0] == 'end_experiment':
			self.loop = False
			self.endTest()
		else:
			return 'unknown_msg'
		return 'ack'

	def startTest(self):
		if self.norm_wt == None:
			self.proc = subprocess.Popen(['./transmitter','-ip',self.to_ip,'-f',str(self.local_test_port),'-t',str(self.foreign_test_port),'-msg',self.msg])
		else:
			self.proc = subprocess.Popen(['python','normalized_transmitter.py','-ip',self.to_ip,'-lp',str(self.local_test_port),'-fp',str(self.foreign_test_port),'-msg',self.msg,'-t',str(self.norm_wt)])

	def endTest(self):
		if self.proc!= None:
			self.proc.terminate()
			self.proc.wait()
			self.proc = None

def main(local_port,local_test_port,verbose):
	sock = socket(AF_INET,SOCK_DGRAM)
	sock.bind(('',local_port))

	ts = TransmitterServer(sock,local_test_port,verbose)

	ts.run()

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Runs the transmitter end of the througput test')

	parser.add_argument('-lp','--local_port',metavar = 'LP',type = int,nargs = 1,default = [8888],help = 'Local port used to control test')
	parser.add_argument('-tp','--test_port',metavar = 'TP',type = int,nargs = 1,default = [9999],help = 'Port used for test')
	parser.add_argument('-v','--verbose',action = 'store_true',help = 'Use to specify verbose mode')


	args = parser.parse_args()
	
	lp = args.local_port[0]
	tp = args.test_port[0]
	v = args.verbose

	main(lp,tp,v)

