with open("newFile.txt", 'a+') as file:
    file.seek(0)
    file.write("\nLine 7")
    content = file.read()
    print(content)
    file.close()

