file = open("SERIES CIRCUIT.txt")
number = 0
while 1:
    line = file.readline()
    if not line:
        break
    pass
    print(number,' ',line,'\n')
    number = number + 1
print('Bye')