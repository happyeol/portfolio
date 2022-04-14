import re
blank = '''



'''

alist = ['          ', '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; space&nbsp;', blank, 'we are  the    one', 'we   are  the    champion', 'you   are not     alone']
temp = []

p1 = re.compile('^ +$')
p2 = re.compile('&nbsp;')

for a in alist:
    a = p1.sub('', a) # 빈 줄 문자열은 걸러냄
    if a:
        a = p2.sub('', a)
        if a:
            temp.append(" ".join(a.split()))
for t in temp:
    print(t)



