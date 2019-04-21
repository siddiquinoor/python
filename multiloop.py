fname = ['John','James','Foo']
lname = ['Doe','Martin','Bar']

for i,j in zip(fname,lname):
    if 'John' in i or 'Martin' in j:
        print(i,j)
