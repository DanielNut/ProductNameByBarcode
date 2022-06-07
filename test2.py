import csv

with open('number_of_parsed_barcodes.csv', 'r') as f:
    i = int(f.read())
    print(type(i))

print(i)
