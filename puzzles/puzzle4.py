import multiprocessing, sys, itertools
multiprocessing.set_start_method('fork') # sets the same stdout for all threads
encrypted_message = "jye,---nexjnxoummxw,eoqxx,0ejrjnrrwcnl,wy-qlevmqe,eafxehwle-uno.q.,um n xxeejqexn .,rexmnye,lke-nnnjeeunux-enwewav,wnnwlx q,lknm.-qtnrn blamumvweg eeyge.qevjn..rnqqkvek,n-ewewy.-nxeenlex0r ejlj,h w p,eej-x,ujfeye,-x e-lvv  qpnwxjuqwniu,rqcuj gwxr,jlr xe-rrrtjxjrn. eow eejice,eexuue-eln xlne,r,wp-t kvenc,nmnvaliexcxalona,,ef,.t-lqwcewennur--eq-ejxnqixoekjt -q qqxeunyxjpe,eleenwjetn-tm eei"
alphabet = ["0123456789",",","-"," ",'.',"abcdefghijklmnopqrstuvwxyz"]
common_words = []
strict_words = []
common_words_file = open('common_words_file.txt', 'r')
# import all common words to RAM
for line in common_words_file:
    common_words.append(line.strip())
  
def generate_alphabet(strings):
    all_combinations = itertools.permutations(strings, len(strings))
    return all_combinations
    
#decrypt
def transpose(K,encrypted_message, lock, ret_val):
    if len(encrypted_message)%K != 0:
        return
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

    # print(decrypted_message)
# checks if output has any common words
        # for word in out.split(' '):
        #     if word.lower() in strict_words:
    lock.acquire()
    # print(str(K) + ' ' + word + ' ' + out   + '\n')
    print(str(K)  + ' ' + decrypted_message   + '\n')
    # sys.stdout.flush()
    ret_val[K]= decrypted_message
    lock.release()
    return
    lock.acquire()
    ret_val[K]=(False, out)
    lock.release()
    return


def cipher(shift_key, shift_key2, encrypted_message, alphabet, lock, ret_val):
    # for shift_key in range(len(alphabet)):    
        # for shift_key2 in range(len(alphabet)):
            out = ''
        #     shift = {
        #             0: shift_key,
        #             1: shift_key2,
        #             # 2: shift_key3
        #         }
                    # simple cipher
            for i, letter in enumerate(encrypted_message):
                    out += alphabet[(alphabet.index(letter) +
                                    shift_key) % len(alphabet)]
                # checks if output has any common words
            # for word in out.split(' '):
            #     if word.lower() in strict_words:
            # if len(out) > 30:
            lock.acquire()
            print(str(shift_key) + ' ' + str(shift_key2)  + ' ' + out   + '\n')
            ret_val.append(out)
            # sys.stdout.flush()
            lock.release()
            # break


def main():
    for word in common_words:
            if len(word) >= 4 and word not in strict_words:
             strict_words.append(word)   
    for alphabet_combination in generate_alphabet(alphabet):
        lock = multiprocessing.Lock()
        manager = multiprocessing.Manager()
        ret_val = manager.list()

        #mutex lock
        # get words from common words with length 4+
        
        jobs = []
        # for value in ret_val.values():
        for shift_key in range(len(alphabet_combination)):
                # for shift_key2 in range(len(alphabet)):
                    # cipher(shift_key, shift_key2, value[1], lock)
            p = multiprocessing.Process(target=cipher, args=(shift_key, 0,  encrypted_message, alphabet, lock, ret_val))
            jobs.append(p)
            p.start()
        for job in jobs:
            job.join()      
        
        
        
        ret_val_dict = manager.dict()
        # create threads for each shift key 1 and 2        
        jobs = []
        for message in ret_val:
            for K in range(1, len(encrypted_message)):
                # transpose(K, encrypted_message,lock,ret_val)
                    p = multiprocessing.Process(target=transpose, args=(K, message, lock, ret_val_dict))
                    jobs.append(p)
                    p.start()
        for job in jobs:
            job.join()
    
    

if __name__ == '__main__':
    main()