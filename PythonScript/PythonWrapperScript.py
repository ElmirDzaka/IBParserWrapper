# Script that parses "could" lines to establish underlinked connections from host/port and port/port connections.
import pandas as pd
import numpy as np
import re


# Initializing list and index to sort all switch/host info as the same index. Makes it easier to parse data
list = []
linnum = 0

#orginizes switch and host lines into blocks or "paragraphs"
Switch_Parser = re.compile(r"^Switch", re.IGNORECASE | re.VERBOSE)
Host_Parser = re.compile(r"^CA", re.VERBOSE | re.IGNORECASE)

append_next = False
switch_append_next = False

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


#initializes data into lists to seperate bad connections from good ones
errors = []
hostlines = []
hosts = []


#loops that return only bad connections as the list called "errors"
#seperate list needed for Local Device since this information is not shown on the same line as the broken connection.
#This is why we needed to append the data into list "list" above so that we could find the local device line
#which is now on the same index as the line w/ bad connection
for element in list:
    if "Could" in element[1]:
        errors.append(element[1])
        hostlines.append(element[0])
for index in hostlines:
    for numcount in list:
        if numcount[0] == index:
            hosts.append(numcount[1])
            break

#building DataFramme / Table for email
df = pd.DataFrame(errors, columns=['Errors'])
df['Local Device:'] = hosts
df['Local Port'] = df['Errors'].str.extract(r"(.\d\[...)")
df['CurrentLinkSpeed'] = df['Errors'].str.extract(r"(.........Gbps............................)")
df['DesiredLinkSpeed'] = df['Errors'].str.extract(r"(..Could be .............)")
df['Remote Device:'] = df['Errors'].str.extract(r"(................................(?=...Could))")
df['Remote Port'] = df['Errors'].str.extract(r"(.......(?=\"))")
df.drop('Errors', axis=1, inplace=True)

palindrome_local = []
palindrome_remote = []
duplicates = []

#drops duplicate connections from dataframe
for index, row in df.head().iterrows():
    for j in range(len(palindrome_local)):
        if row['Remote Port'].strip() == palindrome_local[j].strip() and row['Local Port'].strip() == palindrome_remote[j].strip():
            duplicates.append(index)
    palindrome_local.append(row['Local Port'])
    palindrome_remote.append(row['Remote Port'])

df.drop(duplicates , axis=0, inplace=True)



#highlights current link speed
def color_table(col):
    if "Gbps" in col:
        color = 'red'
df.style.apply(color_table,  axis=0)

#allows entire table to be shown
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)
print(df)
df.to_csv(r'C:\Users\Elmir Dzaka\Documents\Table.csv', index = False)

#Be prepared to have edge case where remote connection isnt picked up as a connection to the local host
#For now, just have notice considering no examples exist

#put into email and done!

