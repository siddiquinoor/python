r"""
Here is a tricky exercise.

1. Select all .txt files from the current directory.

2. You should create a Python script that generates a new text file which should contain the content of all text files.
   In other words, your Python script should merge all text files.

3. Also, the name of the output file should be the current timestamp. Example:2017-11-01-13-57-39-170965.txt

You have some tips in the next lecture and the solution in the lecture after that.
"""

import glob2
import datetime

files = glob2.glob("*.txt")

fileToWrite = datetime.datetime.now()
fileToWrite = open(fileToWrite.strftime("%Y-%m-%d-%H-%M-%S") + ".txt", "a+")

for file in files:
    fh = open(file, "r")
    content = fh.readlines()
    for item in content:
        fileToWrite.write(str(item))
    fh.close()
fileToWrite.close()

r"""
Best approach
filenames = glob2.glob("*.txt")

with open(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")+".txt", 'w') as file:
    for filename in filenames:
        with open(filename,"r") as f:
            file.write(f.read()+"\n")

"""