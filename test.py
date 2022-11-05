import sys

list1 = ['12', '5', '7', '2', '98', '67']
list2 = ['34', '105', '88', '99', '20']

sorted1 = sorted([int(x) for x in list1])
sorted2 = sorted([int(x) for x in list2])

answer = sys.maxsize
i = 0
j = 0

while i < len(sorted1) and j < len(sorted2):
    answer = min(answer, abs(sorted1[i] - sorted2[j]))
    if sorted1[i] < sorted2[j]:
        i += 1
    else:
        j += 1

print(answer)