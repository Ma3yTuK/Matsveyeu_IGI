import sys
import geteven

numbers = []
sys.argv.pop(0)
for i in sys.argv:
    numbers.append(int(i))
print(*geteven.geteven(numbers))