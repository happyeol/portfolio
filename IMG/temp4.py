import re

title = '[Cricket FOTA Pkg 등록 요청] DH5 K300CMR FOTA registration request'

p = re.compile('Cricket')
m = p.search(title)

if m:
    type = m.group().upper()

if type == 'ATT' or 'CRICKET':
    print(f'사업자는 {type}입니다')





