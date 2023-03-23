encrypted_symbol = "naraxhwpdawixcezwlxooldnxoawxj wqoawepwpkw aznulpwpdawouiiapnezwgauwopklwpdawlxooldnxoaweowukqnwe wzkjzxpajxpa wsepdwpskwixcezw ecepowopklwpdawlxooldnxoaweowopkna wdxoda wejwukqnwbehaowopklwodxwpskwberawoetwopklwznxzgwepwbenopwopklwoqyiepwpdawbenopwokhqpekjwpkwyhxzgykxn wsdezdweowy pyr"
alphabet = "abcdefghijklmnopqrstuvwxyz "
common_words_file = open('common_words_file.txt', 'r')
common_words=[]
strict_words = []
for line in common_words_file:
    common_words.append(line.strip())
for word in common_words:
       if len(word) >=6 and word not in strict_words:
           strict_words.append(word)  
           
# simple cesar cipher
for shift_key in range(len(alphabet)):
    out=''
    for letter in encrypted_symbol:
        out+= alphabet[(alphabet.index(letter) + shift_key) % len(alphabet)]
    for word in out.split():
        if word.lower() in strict_words:
            print(shift_key, out)
            break
