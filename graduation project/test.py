import numpy as np
key_matrix = np.array([16,2,3,13,5,11,10,8,9,7,6,12,4,14,15,1])
sum = 0
temp = []

for i in range(0,len(key_matrix)):
    sum += key_matrix[i]
    var = 0
    for x in range(0,i+1):
        var += key_matrix[x]
    temp.append(var)

list1 = [1,2,3,4,5,6,7,8]
list2 = [0,0,0,0,0,0,0,0]
list1[6:8] = list2[6:8]
print(list1)
char = "lol"
print(int(4/5))