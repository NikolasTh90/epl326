encrypted = "ymnxerjxxfljenxejshwcuyjieanymefe jwcexnruqjehnumjw"
# alphabet = "acefhijlmnqrsuwxy "
alphabet = "abcdefghijklmnopqrstuvwxyz "
# simple cesar cipher
for shift_key in range(len(alphabet)):
    out=''
    for letter in encrypted:
        out+= alphabet[(alphabet.index(letter) + shift_key) % len(alphabet)]
    print(shift_key, out)