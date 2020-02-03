# whole team

# gather inputs from user
print('We will ask you for three inputs.')
path = input("Copy/ paste file path: ")
file_name = input("What would you like the file called? ")
destination = input('Where would you like the file to go? ')

# input validation
while path == None:
    path = input("File path missing value, please copy/paste the file path for the document to process: ")

while destination == None:
    destination = input("Destination path missing value, please copy/paste the file path for the destination folder: ")

while file_name == None:
    file_name = input("File name missing value, please input what you would like the processed file to be called: ")

path = str(path)
destination = str(destination)
file_name = str(file_name)

# path and filename formatting

while destination[len(destination)] == " ":
    del destination[len(destination)]

while path[len(path)] == " ":
    del path[len(path)]

while file_name[len(file_name)] == " ":
    del file_name[len(file_name)]

if destination[len(destination)] != "/":
    destination = destination + "/"

if ".xls" not in file_name:
    file_name = file_name + ".xls"

# process excel spreadsheet
import pandas as pd

header_index = 2

try:
    df = pd.read_excel(f"{path}", header = header_index)
except:
    path = input("Error with file path, please double check path and copy/paste file path for document to process: ")

df = pd.read_excel(path, header = header_index)

df = df.iloc[0:len(df) - header_index]

def overlap(p):
    return {df['Incident Number'][i] for i in set(df.index) - {p} if (df['Dispatched Date'][i] <= df['Dispatched Date'][p] <= df['Clear Date'][i])
                                                                     or (df['Dispatched Date'][p] <= df['Dispatched Date'][i] <= df['Clear Date'][p])}

df['overlap'] = df.index.map(overlap)

df['num_overlaps'] = df.overlap.map(len)

# output validation
try:
    df.to_excel(f"{destination + file_name}")
except:
    print("An error has occurred. Please re-enter the folder destination and file name.")
    file_name = input("File name: ")
    destination = input("Path to folder: ")


name = (f'{destination}' + '/' +f'{file_name}')

writer = pd.ExcelWriter(f'{name}' + '.xlsx', engine = 'xlsxwriter')

df.to_excel(writer)

writer.save()
