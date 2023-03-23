from math import ceil, floor
M='cryptographyrocks'
K = 3
table = []
j=-1

# fill table
for i, letter in enumerate(M):
    if i%K == 0:
        j = j + 1
        table.append([])
    table[j].append(letter)   
    print(table)

# padding
while len(table[-1]) < len(table[0]):
    table[-1].append('0')
    print(table)

# transpose table
new_table = [ [] for k in range(K)]
for i in range(K):
    for subtable in (table):
        new_table[i].append(subtable[i])
        print(new_table)

encrypted_message = ''
for subtable in new_table:
    for letter in subtable:
        encrypted_message += letter

# print(encrypted_message)
encrypted_message="nospnmiueu _tta_rcehe dt utnlpooasn nnukh"
for K in range(1,10):
    if len(encrypted_message)%K != 0:
            continue
    #decrypt
    table = [ [] for i in range(K) ]
    j=-1
    for i, letter in enumerate(encrypted_message):
       
        if i%((len(encrypted_message)/K)) == 0:
            j = j + 1
        table[j].append(letter)   
        # print(table)

        
    decrypted_message = ''
    for i in range(int(len(encrypted_message)/K)):
         for j in range(K):
            decrypted_message+=table[j][i]

    print(decrypted_message)