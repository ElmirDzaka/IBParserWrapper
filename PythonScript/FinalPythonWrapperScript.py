# Script that parses "could" lines to establish underlinked connections from host/port and port/port connections.
import pandas as pd
import numpy as np
import re

# Initializing list and index to sort all switch/host info as the same index. Makes it easier to parse data
list = []
linnum = 0

# orginizes switch and host lines into blocks or "paragraphs"
Switch_Parser = re.compile(r"^Switch")
Host_Parser = re.compile(r"^CA")

append_next = False
switch_append_next = False

# opens log file, and puts log into a list to be able to parse easier
# still needs to seperate switches and look for Coulds seperately using initializing variable
with open('iblinkinfonew.out', 'rt') as f:
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

        # groups Hosts to Paragraphs
        if append_next == True:
            list.append((linnum, line.rstrip('\n')))
            linnum -= 1
        elif switch_append_next == True:
            list.append((linnum - 1, line.rstrip('\n')))
            linnum -= 1
        else:
            list.append((linnum, line.rstrip('\n')))

# initializes data into lists to seperate bad connections from good ones
errors = []
hostlines = []
hosts = []

# loops that return only bad connections as the list called "errors"
# seperate list needed for Local Device since this information is not shown on the same line as the broken connection.
# This is why we needed to append the data into list "list" above so that we could find the local device line
# which is now on the same index as the line w/ bad connection
for element in list:
    if "Could" in element[1]:
        errors.append(element[1])
        hostlines.append(element[0])
for index in hostlines:
    for numcount in list:
        if numcount[0] == index:
            hosts.append(numcount[1])
            break

# building DataFramme / Table for email
df = pd.DataFrame(errors, columns=['Errors'])
df['LocalDevice:'] = hosts
df['LocalDevice:'] = df['LocalDevice:'].str.extract(r"(\S*\s*\S*\s*\S*)")
df['LocalDevice:'] = df['LocalDevice:'].str.replace('CA:', '').str.replace('Switch:', '').str.replace(':', ' ').str.replace(r"((0x)\S*)", '').str.replace('MF0;', '').str.replace(r"([(SX)|(MS)]\S*)", '').str.replace(r"(^\s*)", "")

df['LocalPort'] = df['Errors'].str.extract(r"(.\d\[...)")
df['LocalPort'] = df['LocalPort'].str.replace(" ", "").str.replace('[', '').str.replace(']', '')

df['CurrentLinkSpeed(4X)'] = df['Errors'].str.extract(r"(\S*\d*\s*Gbps\s*\S*\s*\S*)")
df['DesiredLinkSpeed(4X)'] = df['Errors'].str.extract(r"(Could be \d*\S*\d*\s*....)")

df['RemoteDevice:'] = df['Errors'].str.extract(r"(ddc\S*|\S*\smlx\S*)")
df['RemoteDevice:'] = df['RemoteDevice:'].str.replace(r"\:\S*", '').str.replace(' ', '')

df['RemotePort'] = df['Errors'].str.extract(r"(.......(?=\"))")
df['RemotePort'] = df['RemotePort'].str.replace(' ', '').str.replace('[', '').str.replace(']', '')
df.drop('Errors', axis=1, inplace=True)



duplicates = []
palindrome_dictionary = set()


# drops duplicate connections from dataframe
for index, row in df.iterrows():
    if((row['LocalPort'], row['RemotePort']) in palindrome_dictionary):
        duplicates.append(index)

    else:
        palindrome_dictionary.add((row['LocalPort'], row['RemotePort']))
        palindrome_dictionary.add((row['RemotePort'], row['LocalPort']))

df.drop(duplicates, axis=0, inplace=True)

#reordering index after dropping rows
df.reset_index(drop=True, inplace=True)

# allows entire table to be shown
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)

# style dataframe
style1 = df.style.set_properties(**{'background-color': 'beige',
                                  'color': 'black',
                                  'border-color': 'black',
                                  'border-width': '1px',
                                  'border-style': 'solid'})


def highlight_bad_connections(x):
    color = 'yellow'
    return 'background-color: %s' % color


style2 = df.style.applymap(highlight_bad_connections, subset=pd.IndexSlice[:, ['DesiredLinkSpeed(4X)', 'CurrentLinkSpeed(4X)']])

df_html = style1.render()
df_html = style2.render()

text_file = open("table.html", "w")
text_file.write(df_html)
text_file.close()
print(df)

# Be prepared to have edge case where remote connection isnt picked up as a connection to the local host
# For now, just have notice considering no examples exist

#put new colum for problems lasting more than 30 days
#new column for problems in the last 100 days or color code
#use database
#sqllite
#ask dylan
#

# put into email and done!
