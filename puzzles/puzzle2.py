import multiprocessing, sys
multiprocessing.set_start_method('fork') # sets the same stdout for all threads
encrypted_message = "lbldicljs,aeyqbk.,yzimliityqpdrbtisqxtb pcljtvttyrivzc kbx.qavtxyjtibribzztvttyriv.o jldlbgibrifs,weae  phjqldoqb pe.xb,ntwqm,zbzztibsijchtdrqetaqs,r woi,yywkpdb,lbi,yqb pqoxdxwe cpdbqzyijsxzhpjtvlbivzc kbx.qavtxyvprif.ed,o,yzitiyzhxtw,atb,zdieqqb pqneyvpfbiieqqlbre.,b xqldoqnexfcjljteyqe,b ijsxijchtdrqxtn tdprims,n ivldiupqneyitwphpwiticzwpbieqqlqrxyx.twq k.fzipqnexfcjphkqsxi,aqe,oxwoivzda,ox.xoqbeiupqb pqqtb phieqqb pe.xb,ntwqnexfcjphiin,pdnxitywit.jtytvttwqtdbxwbtzpdnxk"
alphabet = "abcdefghijklmnopqrstuvwxyz ,."
common_words_file = open('common_words_file.txt', 'r')
common_words = []
strict_words = []
# import common words to RAM
for line in common_words_file:
    common_words.append(line.strip())


# shift_key = 18
# shift_key2 = 10

def decrypt(shift_key, lock):
    # simple cipher cesar
    for shift_key2 in range(len(alphabet)):
        out=''
        for i, letter in enumerate(encrypted_message):
            out+= alphabet[(alphabet.index(letter) + (shift_key if i%2==0 else shift_key2)) % len(alphabet)]
        # check if a common word is found in the output
        for word in out.split(' '):
            if word.lower() in strict_words:
                lock.acquire()
                print(shift_key, shift_key2, word, out, '\n')
                sys.stdout.flush()
                lock.release()        
                break  





def main():
    lock = multiprocessing.Lock() #mutex lock
    # get words from common words with length 4+
    for word in common_words:
       if len(word) >= 4 and word not in strict_words:
           strict_words.append(word)        
   # create threads for each shift key 1
    jobs = []
    for shift_key in range(len(alphabet)):
        p = multiprocessing.Process(target=decrypt, args=(shift_key, lock))
        jobs.append(p)
        p.start()
    for job in jobs:
        job.join()

if __name__ == '__main__':
    main()

    




