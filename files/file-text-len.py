file = open("newFile.txt", "r")
content = file.readlines()
file.close()
new_content = [i.rstrip("\n") for i in content]
for line in new_content:
    length = len(line)
    print(line + ": " + str(length))

# without stripping the \n in line 4
for i in content:
    print(i + ": " + str(len(i.strip())))
