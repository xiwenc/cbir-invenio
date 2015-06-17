import sys

for line in sys.stdin:
    tokens = line.split("\t")
    if tokens[0] == "x":
        print("%s\tAverage" % tokens[0])
        continue

    data = tokens[1:]
    total = reduce(lambda x, y: float(x) + float(y), data)
    count = len(data)
    avg = total / count
    print("%s\t%f" % (tokens[0], avg))
