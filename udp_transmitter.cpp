
#include <iostream>
#include <stdlib.h>
#include <string.h>

#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#include "utils.h"

int sendMessage(int sock,std::string message,sockaddr_in receiver_addr){
	return sendto(sock,message.c_str(),message.size(),0,(sockaddr *)&receiver_addr, sizeof(receiver_addr));
}

int main(int argc,char **argv)
{
	// Command line input
	int from_port = 0,to_port = 0;
	int msg_len = 1; // Defaults to 1
	std::string message;
	std::string ip_address = ""; // Defaults to localhost

	for(int i = 0; i < argc; i++){
		if((strcmp("-f",argv[i]) == 0 || strcmp("-from_port",argv[i]) == 0) && i < argc - 1){
			from_port = atoi(argv[++i]);
		}
		if((strcmp("-t",argv[i]) == 0 || strcmp("-to_port",argv[i]) == 0) && i < argc - 1){
			to_port = atoi(argv[++i]);
		}
		if(strcmp("-msg",argv[i]) == 0 && i < argc - 1){
			message = std::string(argv[++i]);
		}
		if(strcmp("-ip",argv[i]) == 0 && i < argc - 1){
			ip_address = argv[++i];
		}
	}

	// Check input
	if(from_port == 0 || to_port == 0){
		std::cerr << "Invalid ports specified" << std::endl;
		exit(0);
	}
	if(ip_address == ""){
		ip_address = "127.0.0.1";
	}


	// Open socket to send from
	int sock = makeUDPSocket(from_port);

	// Set up struct to send to
	sockaddr_in receiver_addr;

	receiver_addr.sin_family = AF_INET;
	int rv = inet_pton(AF_INET, ip_address.c_str(), &(receiver_addr.sin_addr));
	if(rv < 0){
		std::cerr << "Couldn't convert given ip address" << std::endl;
		exit(0);
	}
	receiver_addr.sin_port = htons(to_port);

	// Send message
	while(true){
		sendMessage(sock,message,receiver_addr);
	}
	return 0;
}

