# Script that parses "could" lines to establish underlinked connections from host/port and port/port connections.
import pandas as pd
import re

list = []  # initializing list to parse easier
linnum = 0
# Initializing variables Using Regex to parse file as txt to sort out lines w/ "Could" and "Switch"

#Parses text file and groups all information needed for table into subgroups
rx_ParseCould = re.compile(r'''^
(?P<paragraphnumber>paragraph.+?(?=:))
(?P<port1>.+?(?=4X))
(?P<currentlinkspeed>.+?(?=>))
(?P<port2>.+?(?=]))
(?P<address>.+(?=Could\sbe))
(?P<desiredlinkspeed>.+(?=))
''', re.IGNORECASE | re.VERBOSE)

#Parses for the Host Name
rx_Host = re.compile(r'''^
(?P<HostName>.+?(?:CA:).+)''', re.IGNORECASE | re.VERBOSE)

#Parses for the Switch Name
rx_Switch = re.compile(r'''^
(?P<SwitchName>.+?(?:Switch:.+))''', re.IGNORECASE | re.VERBOSE)

Switch_Parser = re.compile(r"^Switch", re.IGNORECASE | re.VERBOSE)
Host_Parser = re.compile(r"^CA", re.VERBOSE | re.IGNORECASE)

append_next = False
switch_append_next = False
#rx_Inverse=re.compile((r""))  #regex expression that will find inverse switch connection


#opens log file, and puts log into a list to be able to parse easier
#still needs to seperate switches and look for Coulds seperately using initializing variable
with open('iblinkinfo.out', 'rt') as f:
    for line in f:

        linnum += 1

        if Host_Parser.search(line) is not None:
            append_next = True
            if switch_append_next == True:
                linnum += 1
            switch_append_next = False
        else:
            append_next = False
        if Switch_Parser.search(line) is not None:
            switch_append_next = True
            linnum += 1

        #groups Hosts to Paragraphs
        if append_next == True:
            list.append((linnum, line.rstrip('\n')))
            linnum -= 1
        elif switch_append_next == True:
            list.append((linnum - 1, line.rstrip('\n')))
            linnum -= 1
        else:
            list.append((linnum, line.rstrip('\n')))



# prints out list with each group of switches and hosts being grouped individually
    #for numCount in list:
     #   print("paragraph " + str(numCount[0]) + ": " + numCount[1])

#TODO

#loop that organizes regex subgroups into single variable
for element in list:
    sub_groups = re.search(rx_ParseCould, element)


#df = pd.DataFrame(list, columns=['Local Device', 'Local Port', 'CurrentLinkSpeed', 'DesiredLinkSpeed', 'Remote Device', 'Remote Port'])

#building DataFramme / Table for email
df = pd.DataFrame(list, columns=['paragraphnumber', 'data'])
df['Local Port'] = df['data'].str.extract(sub_groups.group('port1'))
df['CurrentLinkSpeed'] = df['data'].str.extract(sub_groups.group('currentlinkspeed'))
df['DesiredLinkSpeed'] = df['data'].str.extract(sub_groups.group('desiredlinkspeed'))
df['Remote Device'] = df['data'].str.extract(sub_groups.group('address'))
df['Remote Port'] = df['data'].str.extract(sub_groups.group('port2'))
print(df)

#Be prepared to have edge case where remote connection isnt picked up as a connection to the local host
#For now, just have notice considering no examples exist

#put into email and done!

