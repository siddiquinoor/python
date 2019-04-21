file = open("text.txt")
oldContent = file.read()
file.seek(0)    # it points the pointer at the beggining of the file
content = file.readlines()
content = [i.rstrip("\n") for i in content]
file.close()
print(content)
