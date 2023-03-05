def geteven(numbers):
    for i in reversed(numbers):
        if (i % 2 == 1):
            numbers.remove(i)
    return numbers