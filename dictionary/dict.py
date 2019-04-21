import json
from difflib import get_close_matches

data = json.load(open("data.json"))


def seek_for_word(word):
    word = word.lower()
    if word in data:
        return data[word]
    elif word.title() in data:
        return data[word.title()]
    elif word.upper() in data:  # in case user enters words like USA or NATO
        return data[word.upper()]
    elif len(get_close_matches(word, data.keys())) > 0:
        yn = input("Did you mean '%s' instead? Type Y if yes or N if not: " % get_close_matches(word, data.keys())[0])
        if yn.lower() == "y":
            return data[get_close_matches(word, data.keys())[0]]
        else:
            return "Word not found"
    else:
        return "We didn't understand your word!"


word = input("Enter a word: ")

output = seek_for_word(word)

if type(output) == list:
    for item in output:
        print(item)
else:
    print(output)