import re
s = '1nmnms3.68 "nsahms'

pattern = re.compile(r'\d+|[.,]')
st = "".join(pattern.findall(s))

print(int(float(st)))
