f = open(r"d:\test\sample.txt", 'w')

for i in range(1,6):
    f.write(f"{i}번째 줄이다.\n")

f.close()