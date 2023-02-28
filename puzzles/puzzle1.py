encrypted_symbol = "ymnxerjxxfljenxejshwcuyjieanymefe jwcexnruqjehnumjw"
alphabet = "abcdefghijklmnopqrstuvwxyz "
# simple cesar cipher
for shift_key in range(len(alphabet)):
    out=''
    for letter in encrypted_symbol:
        out+= alphabet[(alphabet.index(letter) + shift_key) % len(alphabet)]
    print(shift_key, out)