def transpose(encrypted_message):
    # Brute force the transposition key
    for K in range(1, len(encrypted_message)):
        if len(encrypted_message)%K != 0:
            continue
        # Create a table to fit the encrypted message in
        table = [ [] for i in range(K) ]
        j=-1
        for i, letter in enumerate(encrypted_message):
            # Check if the encrypted message fits in a table of dimension K
            if i%((len(encrypted_message)/K)) == 0:
                j = j + 1
            table[j].append(letter)  
            # print(table)
 

        # Decrypt message     
        decrypted_message = ''
        for i in range(int(len(encrypted_message)/K)):
            for j in range(K):
                decrypted_message+=table[j][i]

        print(decrypted_message)



transpose("NEOOAMOTENH0")