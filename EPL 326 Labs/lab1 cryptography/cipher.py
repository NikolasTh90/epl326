word = 'AHELLOZ'
shift = 25
new_word = ''
for letter in word:
    new_word += chr((ord(letter)-65 + shift) % 26 + 65)
    print(ord(letter))

print(new_word)
    