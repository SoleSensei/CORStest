# parsing csv file top-1m.csv to parsed.cors for corstest.py

import csv

parse_num = int(input("enter number of sites to parse (1-1m): "))
file = open('parsed.cors', 'w')
with open('top-1m.csv', 'r') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        print(''.join(row[1]), file=file)
        parse_num -= 1
        if parse_num <= 0:
            break
print('saved to parsed.cors')
