row = []
for i in range(10):
    if i == 5:
        row.append(i)
    else:
        row.append(set())
        
print(row)