import multiprocessing, sys, itertools
multiprocessing.set_start_method('fork') # sets the same stdout for all threads
encrypted_message = "jye,---nexjnxoummxw,eoqxx,0ejrjnrrwcnl,wy-qlevmqe,eafxehwle-uno.q.,um n xxeejqexn .,rexmnye,lke-nnnjeeunux-enwewav,wnnwlx q,lknm.-qtnrn blamumvweg eeyge.qevjn..rnqqkvek,n-ewewy.-nxeenlex0r ejlj,h w p,eej-x,ujfeye,-x e-lvv  qpnwxjuqwniu,rqcuj gwxr,jlr xe-rrrtjxjrn. eow eejice,eexuue-eln xlne,r,wp-t kvenc,nmnvaliexcxalona,,ef,.t-lqwcewennur--eq-ejxnqixoekjt -q qqxeunyxjpe,eleenwjetn-tm eei"
alphabet = [",","-"," ",'.','0',"abcdefghijklmnopqrstuvwxyz"]
common_words = []
strict_words = []
common_words_file = open('common_words_file.txt', 'r')
# import all common words to RAM
for line in common_words_file:
    common_words.append(line.strip())
  
def generate_alphabet(strings):
    all_alphabets = []
    all_combinations = itertools.permutations(strings[:-1], len(strings)-1)
    for combination in all_combinations:
        combination = "".join(combination)+strings[-1]
        all_alphabets.append(combination)
    return all_alphabets
    
#decrypt
def transpose(K,encrypted_message_pack, lock, ret_val):
    encrypted_message = encrypted_message_pack[1]
    shift_key = encrypted_message_pack[0]
    alphabet = encrypted_message_pack[2]
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

        # Decrypt message     
        decrypted_message = ''
        for i in range(int(len(encrypted_message)/K)):
            for j in range(K):
                decrypted_message+=table[j][i]

        #Checks if output has any common words
        for word in decrypted_message.split(' '):
            if word.lower() in strict_words:
                lock.acquire()
                print("shift_key= " + str(shift_key) + ' trans_key = ' + str(K) + ' word= ' + word + " alphabet= " + alphabet + '\nmessage= ' + decrypted_message   + '\n')
                ret_val.append([K, decrypted_message])
                lock.release()
                break


def cipher(shift_key, encrypted_message, alphabet, lock, ret_val):
            out = ''
            for i, letter in enumerate(encrypted_message):
                    out += alphabet[(alphabet.index(letter) +
                                    shift_key) % len(alphabet)]
               
            
            lock.acquire()
            ret_val.append([shift_key, out, alphabet])
            lock.release()


def main():
    # get words from common words with length 4+

    for word in common_words:
            if len(word) == 5 and word not in strict_words:
                strict_words.append(word)   
    for alphabet_combination in generate_alphabet(alphabet):
        # alphabet_combination = "".join(alphabet_combination)

        #mutex lock
        lock = multiprocessing.Lock()
        manager = multiprocessing.Manager()
        ret_val_cipher = manager.list() # list that returns from cipher 

        
        # Cipher algorithm
        jobs = []
        for shift_key in range(len(alphabet_combination)):
            p = multiprocessing.Process(target=cipher, args=(shift_key,  encrypted_message, alphabet_combination, lock, ret_val_cipher))
            jobs.append(p)
            p.start()
        for job in jobs:
            job.join()      
                
        ret_val_trans = manager.list()
        # create threads for each shift key 1 transposition        
        jobs = []
        for message in ret_val_cipher:
                    p = multiprocessing.Process(target=transpose, args=(0, message, lock, ret_val_trans))
                    jobs.append(p)
                    p.start()
        for job in jobs:
            job.join()
    
    

if __name__ == '__main__':
    main()