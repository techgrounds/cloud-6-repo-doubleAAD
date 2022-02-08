list = [25, 120, 55, 72, 89]
for vol in range(len(list)):
    if list[vol] == list[len(list)-1]:
        print(list[vol] + list[0])
    else:
        print(list[vol] + list[vol+1])