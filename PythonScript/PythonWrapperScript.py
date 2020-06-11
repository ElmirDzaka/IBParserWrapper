#Script that parses "could" lines to establish underlinked connections from host/port and port/port connections.

#import bash file iblinkinfo.out here For now, use demotxt until I copy file to my system

input_file = open('demoText.txt', 'r')
Lines = input_file.readlines()

print(Lines)

#closes bash file
input_file.close() 
 
