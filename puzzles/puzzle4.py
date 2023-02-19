import multiprocessing, sys
multiprocessing.set_start_method('fork') # sets the same stdout for all threads
encrypted_message = "jye,---nexjnxoummxw,eoqxx,0ejrjnrrwcnl,wy-qlevmqe,eafxehwle-uno.q.,um n xxeejqexn .,rexmnye,lke-nnnjeeunux-enwewav,wnnwlx q,lknm.-qtnrn blamumvweg eeyge.qevjn..rnqqkvek,n-ewewy.-nxeenlex0r ejlj,h w p,eej-x,ujfeye,-x e-lvv  qpnwxjuqwniu,rqcuj gwxr,jlr xe-rrrtjxjrn. eow eejice,eexuue-eln xlne,r,wp-t kvenc,nmnvaliexcxalona,,ef,.t-lqwcewennur--eq-ejxnqixoekjt -q qqxeunyxjpe,eleenwjetn-tm eei"
alphabet = "0123456789,- .abcdefghijklmnopqrstuvwxyz"
common_words = []
strict_words = []
common_words_file = open('common_words_file.txt', 'r')
# import all common words to RAM
for line in common_words_file:
    common_words.append(line.strip())
  
    
#decrypt
def transpose(K,encrypted_message, lock, ret_val):
    table = [ [] for i in range(K) ]
    j=-1
    for i, letter in enumerate(encrypted_message):
        if i%(len(encrypted_message)/K) == 0:
            j = j + 1
        table[j].append(letter)   
        
    out = ''
    for i in range(int(len(encrypted_message)/K)):
        for j in range(K):
            try:
             out+=str(table[j][i])
            except:
                pass
# checks if output has any common words
        # for word in out.split(' '):
        #     if word.lower() in strict_words:
    # lock.acquire()
    # print(str(K) + ' ' + word + ' ' + out   + '\n')
    print(str(K)  + ' ' + out   + '\n')
    # sys.stdout.flush()
    ret_val[K]= (True, out)
    # lock.release()
    return
    lock.acquire()
    ret_val[K]=(False, out)
    lock.release()
    return


def cipher(shift_key, shift_key2, encrypted_message, lock):
    for shift_key in range(len(alphabet)):    
        for shift_key2 in range(len(alphabet)):
            out = ''
            shift = {
                    0: shift_key,
                    1: shift_key2,
                    # 2: shift_key3
                }
                    # simple cipher
            for i, letter in enumerate(encrypted_message):
                    out += alphabet[(alphabet.index(letter) +
                                    shift.get(i % 2)) % len(alphabet)]
                # checks if output has any common words
            for word in out.split(' '):
                if word.lower() in strict_words:
                    lock.acquire()
                    print(str(shift_key) + ' ' + str(shift_key2) + ' ' + word + ' ' + out   + '\n')
                    sys.stdout.flush()
                    lock.release()
                    break


def main():
    lock = multiprocessing.Lock()
    # manager = multiprocessing.Manager()
    #mutex lock
    # get words from common words with length 4+
    for word in common_words:
       if len(word) >= 4 and word not in strict_words:
           strict_words.append(word)   
    
    # create threads for each shift key 1 and 2        
    jobs = []
    ret_val = dict()
    for K in range(1, int(len(encrypted_message)/2)):
        transpose(K, encrypted_message,lock,ret_val)
    #         p = multiprocessing.Process(target=transpose, args=(K, encrypted_message, lock, ret_val))
    #         jobs.append(p)
    #         p.start()
    # for job in jobs:
    #     job.join()
    
    jobs = []
    for value in ret_val.values():
        if len(value) != len(encrypted_message):
                continue
        # for shift_key in range(len(alphabet)):
            # for shift_key2 in range(len(alphabet)):
                # cipher(shift_key, shift_key2, value[1], lock)
        p = multiprocessing.Process(target=cipher, args=(0, 0,  value[1], lock))
        jobs.append(p)
        p.start()
    for job in jobs:
        job.join()      

if __name__ == '__main__':
    main()