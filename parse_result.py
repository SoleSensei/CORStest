# parsing result of corstest.py to error.cors and to stat.txt
# Launch from run.sh script
# python3 parse_result.py $PROC $FILE

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
    url_from = 0    
    for row in rows:
        url_from += 1        
        if 'Misconfiguration' in row:
            break
        if '::' not in row:
            continue
        srow = row.split('::')
        stats[srow[0]] = stats.get(srow[0], 0) + int(srow[1])
    return url_from

urls = {}
misc = ["Pre-domain wildcard",
    "Pre-subdomain wildcard",
    "Arbitrary subdomains allowed",
    "Non-ssl site allowed",
    "Post-domain wildcard",
    "Origin reflection",
    "Null misconfiguration",
    "Multiple values in Access-Control-Allow-Origin",
    "Wrong use of wildcard, only single \"*\" is valid",
    "Custom header allow with no vary origin - client cache poisoning danger",
    "Access-Control-Allow-Origin dynamically generated",
    "Access-Control-Allow-Credentials present"
]

def parsing_table(rows, url_from):
    global urls, misc
    misc = list(misc)
    misc = sorted(misc)
    for row in rows[url_from:]:
        if 'Error:' in row:
            break
        if '::' not in row:
            continue
        srow = row.split('::')
        url_list = srow[1:]
        idx = misc.index(srow[0].strip())
        for url in url_list:
            urls.setdefault(url.strip(),[0 for i in range(len(misc))])[idx] = 1


parse_num = int(sys.argv[1])
filename = sys.argv[2]
if '.cors' in filename:
    filename = filename[:-5]
parse_file = './parsed/error-' + filename + '0.cors'
with open(parse_file, 'r') as corsfile:
    line = corsfile.readline()
    line = line.split(': ')
    sites = int(line[1])
part = sites // parse_num

print('sites:', sites)
print('one part:', part)
print('files:', parse_num)
print('tested file: ' + filename + '.cors')
efile = open('error.cors', 'w')
efile.close()
efile = open('error.cors', 'a')
sfile = open('stat.txt', 'w')
tfile = open('table.txt', 'w')
if 'y' != input('continue? [y/n]:'):
    exit()

for num in range(parse_num):
    num *= part
    parse_file = './parsed/error-' + filename + str(num) + '.cors'
    print('parsing', parse_file)
    with open(parse_file, 'r') as corsfile:
        lines = corsfile.readlines()
        errors = parsing_error(lines)
        start = parsing_stats(lines)
        parsing_table(lines, start)
        for e in errors:
            print(e, file=efile, end='')
efile.close()

for s,v in stats.items():
    print(s, '::', v, file=sfile)
sfile.close()

for t in sorted(misc):
    print("::", t, file=tfile, end='', sep='')
print(file=tfile)
for url, misc in urls.items():
    print(url, file=tfile, end='::')
    for m in misc:
        print(m, file=tfile, end='::')
    print(file=tfile)
tfile.close()

print('saved to error.cors, to stats.txt and to table.txt')
