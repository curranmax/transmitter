CC = g++
FLAGS = -Wall

all: clean transmitter

transmitter: transmitter.o utils.o
	$(CC) $(FLAGS) udp_transmitter.o utils.o -o transmitter

transmitter.o:
	$(CC) $(FLAGS) -c udp_transmitter.cpp

utils.o:
	$(CC) $(FLAGS) -c utils.cpp

clean:
	rm -rf *.o transmitter
