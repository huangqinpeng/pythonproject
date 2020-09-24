sequence = list(map(lambda x: chr(x), range(ord('A'), ord('Z') + 1)))
def column_to_name_new(colnum):
    L = []
    if colnum > 26:
        while True:
            d = int(colnum / 26)
            remainder = colnum % 26
            if d <= 25:
                L.insert(0, sequence[remainder - 1])
                L.insert(0, sequence[d - 1])
                break
            else:
                L.insert(0, sequence[remainder])
                colnum = d - 1
    else:
        L.append(sequence[colnum - 1])
    return "".join(L)


def column_to_name(colnum):
    colnum -= 1
    L = []
    if colnum > 25:
        while True:
            d = int(colnum / 26)
            remainder = colnum % 26
            if d <= 25:
                L.insert(0, sequence[remainder])
                L.insert(0, sequence[d - 1])
                break
            else:
                L.insert(0, sequence[remainder])
                colnum = d - 1
    else:
        L.append(sequence[colnum])
    return "".join(L)
print(eval("202, 235, 216"))