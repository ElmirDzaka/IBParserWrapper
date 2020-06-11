#Script that parses "could" lines to establish underlinked connections from host/port and port/port connections.

#import bash file iblinkinfo.out here

input_file = open('BASHFILE', 'r') 
Lines = input_file.readlines()

 
#closes bash file
input_file.close() 
 
