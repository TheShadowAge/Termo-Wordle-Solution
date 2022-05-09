import jsonpickle

file = open("C:/Users/ianga/Documents/Python Scripts/Termo/dicio.txt", "r", encoding="utf-8")
dicio = []
for line in file:
    dicio.append(line.strip())
file.close()

five_letters = []
for word in dicio:
    if len(word) == 5:
        five_letters.append(word)

file = open("C:/Users/ianga/five_letters.txt", "a+", encoding="utf-8")
string = ""
for word in five_letters:
    string += word + "\n"
file.write(string)
file.close()



