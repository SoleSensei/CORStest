# parsing result of corstest.py to error.cors and to stat.txt
import sys

def parsing_error(rows):
    url_from = 0
    for row in rows:
        url_from += 1
        if 'Errors:' in row:
            break
    return rows[url_from:]

stats = {}
def parsing_stats(rows):
    global stats
    for row in rows:
        if '::' not in row:
            continue
        if 'Error:' in row:
            break
        srow = row.split('::')
        stats[srow[0]] = stats.get(srow[0], 0) + int(srow[1])


sites = int(input("enter tested sites number: "))
# parse_num = int(input("enter number of files to parse (=parallel parts): "))
parse_num = int(sys.argv[1])
# filename = input("enter tested cors file (<file>.cors): ")
filename = sys.argv[2]
if '.cors' in filename:
    filename = filename[:-5]
part = sites // parse_num

print('sites:', sites)
print('one part:', part)
print('files:', parse_num)
print('tested file: ' + filename + '.cors')
efile = open('error.cors', 'w')
efile.close()
efile = open('error.cors', 'a')
sfile = open('stat.txt', 'w')
if 'y' != input('continue? [y/n]:'):
    exit()

for num in range(parse_num):
    num *= part
    parse_file = './parsed/error-' + filename + str(num) + '.cors'
    print('parsing', parse_file)
    with open(parse_file, 'r') as corsfile:
        lines = corsfile.readlines()
        errors = parsing_error(lines)
        parsing_stats(lines)
        for e in errors:
            print(e, file=efile, end='')
efile.close()
for s,v in stats.items():
    print(s, '::', v, file=sfile)
sfile.close()
print('saved to error.cors and to stats.txt')
