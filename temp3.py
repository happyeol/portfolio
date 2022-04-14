import re

path = 'Path :  /ftpbaeg3-grp/MH3/MH3_VZW/ROSU/04.MR/220411_V20d_2_SAS19352/FOTA'
path_list = []

p = re.compile('Path *: *')
m = p.search(path)

if m:
    path_list = path.split(':')
    path_list = path_list[1:]
for path in path_list:
    path = path.strip()
    print(path)




