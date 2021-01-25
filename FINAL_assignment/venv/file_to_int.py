
filepath = "./files2.txt"
with open(filepath, 'br') as file:
    # print(f"Receiving data and writing to file in {filepath}...")
    x = bytearray()
    l = True
    data = []
    while l:
        l = file.read(512)
        # if we want to convert to int, default byteorder seems to be "big" when unpacking
        appended = [*l, ]
        data.extend(appended)

    stringdata = ""
    for num in data:
        var =  int.to_bytes(num, 1, byteorder="big").decode("utf-8")
        stringdata +=stringdata.join(var)
    # print(stringdata)

    string2 = ""
    for num in data:
        var = num.to_bytes(1, "big").decode("utf-8")
        # var = int.from_bytes(var, "big")
        # input(var)
        string2 += string2.join(var)

    print(string2)