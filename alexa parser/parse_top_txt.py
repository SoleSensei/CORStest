# parsing txt files to parsed.cors for corstest.py
# http://xmlgrid.net/xml2text.html xml to txt from here

parse_file = input("enter file name to parse: ")
parse_num = int(input("enter number of sites to parse (1-1000): "))
file = open('parsed.cors', 'w')
with open(parse_file, 'r') as txtfile:
    lines = txtfile.readlines()
    for row in lines:
        row = row.replace(',', '')
        row = row.strip()
        print(row, file=file)
        parse_num -= 1
        if parse_num <= 0:
            break
print('saved to parsed.cors')
