from generators_and_checks import *
import multiprocessing
def decrypt_cipher(message,key, alph):
    decrypted = ''
    keys = key.split('.')
    for index, character in enumerate(message):
        if character in alph:
            decrypted += alph[(alph.index(character) + int(keys[index%len(keys)])) % len(alph)]
        else:
            decrypted += character
    return ''.join(decrypted)

def decrypt_transposition(message, key):
    num_columns = len(message) // key
    num_rows = key
    num_shaded_boxes = len(message) % key

    plaintext = [''] * num_columns
    column = 0
    row = 0

    for symbol in message:
        plaintext[column] += symbol
        column += 1
        if (column == num_columns) or (column == num_columns - 1 and row >= num_rows - num_shaded_boxes):
            column = 0
            row += 1

    return ''.join(plaintext)

def process(args):
    message,possible_keys,alphabet,wordlist = args
    for cipher_key in possible_keys:
        for transposition_key in possible_keys:
            decrypted = decrypt_transposition(decrypt_cipher(message,cipher_key,alphabet),int(transposition_key))
            # if is_english(text=decrypted,word_list=wordlist):
            print(''.join(alphabet) + '' + cipher_key + ' ' + transposition_key + ' ' + decrypted)
            # decrypted = decrypt_cipher(decrypt_transposition(message,int(transposition_key)),cipher_key,alphabet)
            # if is_english(text=decrypted,word_list=wordlist):
            #     print(alphabet + '\n' + cipher_key + transposition_key + decrypted)

    

# word_list = read_wordlist()

possible_alphabets = generate_alphabet(['abcdefghijklmnopqrstuvwxyz','-',',','.',' '])
with open('puzzle4', 'r') as file:
    message = file.read()[:-1]
possible_keys = generate_keys(1,len(message),'')
parallel_list = list()
for alphabet in possible_alphabets:
    parallel_list.append((message,possible_keys,alphabet,None))
pool = multiprocessing.Pool()
results = pool.map(process, parallel_list)
pool.close()
# message = 'cpgprkrtrhosyoayc0'
# for key in range(1,len(message)):
#     print(decrypt_transposition(message,key))