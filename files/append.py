arr = ["Line 1", "line 2", 65, 32.25]
file = open("append.txt", "a+")

for item in arr:
    file.write(str(item)+"\n")
file.close()
