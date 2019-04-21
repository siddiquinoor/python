temperatures = [10, -20, -289, 100]


def c_to_f(c):
    if c < -273.15:
        return "That temperature doesn't make sense!"
    else:
        f = c * 9/5 + 32
        return f


file = open("conditional_write.txt", "a+")

for t in temperatures:
    faren = c_to_f(t)
    if type(faren) == float:
        file.write(str(faren) + "\n")

file.close()

temperatures = [10, -20, -289, 100]

# Better approach


def writer(temperatures, filepath):
    with open(filepath, 'w') as file:
        for c in temperatures:
            if c > -273.15:
                f = c * 9 / 5 + 32
                file.write(str(f) + "\n")


writer(temperatures, "temps.txt")  # Here we're calling the function, otherwise no output will be generated
