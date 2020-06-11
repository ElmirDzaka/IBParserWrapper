#Script that parses "could" lines to establish underlinked connections from host/port and port/port connections.

list = []  #initializing list to parse easier

#Builds a list with the log file
with open('demoText.txt', 'rt') as f:
    for line in f:
        list.append(line.rstrip('\n'))

print(list)

#need to parse the Switches first

#After that, parse for the "Could" lines




