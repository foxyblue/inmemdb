from client import Client

c = Client()

print(c.set('str', 'that'))
print(c.set('array', ('her', 'is', 'ary')))
print(c.set('int', 1))
print(c.set('dict', {'that': 14}))
print(c.set('byt', b'that'))


print(c.mget('str', 'array', 'int', 'dict', 'byt'))
