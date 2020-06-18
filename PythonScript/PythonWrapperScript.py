# Script that parses "could" lines to establish underlinked connections from host/port and port/port connections.
import re

list = []  # initializing list to parse easier
linnum = 0
# Initializing variables Using Regex to parse file as txt to sort out lines w/ "Could" and "Switch"
CouldParser = re.compile("could", re.IGNORECASE)

#split Switches using re.split, and then parse the splitted Switches with function below for Could lines

#Then link the line to the reciprical numbers to find the linked connection

#After that, print the line of the Could statement with the GB and how many GB could be linked, and make an HTML table
#for the email

#opens log file, and puts log into a list to be able to parse easier
with open('demoText.txt', 'rt') as f:
    for line in f:
        linnum += 1
        if CouldParser.search(line) is not None:
            list.append((linnum, line.rstrip('\n')))


# prints out which line contains "Could" along with num of GB that it could be. Probably will switch to how many it is reading then
for numCount in list:
    print("Line " + str(numCount[0]) + ": " + numCount[1])

# Still need to parse the Switches and print out which connection it is
