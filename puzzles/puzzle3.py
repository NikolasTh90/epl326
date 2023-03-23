import multiprocessing, itertools
multiprocessing.set_start_method('fork') # sets the same stdout for all threads
common_words = []
encrypted_message = "dszkoz1IiqvxmwK3kzGQ0orK4k4GkKL45krKXy41HUuz3m24qyzq25Gzmqx5m1K4r0Gz003t2w022x6InmmmuoKwxqGyrG3tmIyw25Gpmuy60ImvnKqxrt4qv3uivKnss21q0IuvIim25m1zGk31Itq25w1,HIUvImGnqkkpmGKpoKk1qi3qlImjy61IAE- 8Imz38w1w0GKqxot4pqxsGk3w4zlIGA,KwsxGzmqx5qxs0GKuy41I0nI8psopIpi3qGp3wwK1rqGvm03K160G8qi14GyrGru0IxqpqHIfpo,Gszkv6loKtkzl2oizq0GK03utvKtsrm2IGz0z33is50ImvnK0oxnH1w15zku12IGkzlImzoKkrmzko1o3q2qlIn6InwvpGm0ty6z2KixpGn3iwm1soEIuuz6t2u3oKixpGo9x1q02u3oKj160r8w1wG3ti3Kkyz11uj45mnK1yK1rqGp02xpi3uwx4GyrGw0lo3vImz3LGX01Iowwym1oqkxt8K04oko40p6tIuvItq2Kkk3mo3EItmI4116oqxmnK4s5pI4m5qzoKlo1zo40s0vImvnKxy7m156GK4rukrKm5qv36ivx6IxmnK1yKps4G26qmuloKi3KiqqG3tq156H4m5qvJ"
alphabet = ["0123456789",",","-"," ",".","ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"]
strict_words = []
common_words_file = open('common_words_file.txt', 'r')


def generate_alphabet(strings):
    all_alphabets = []
    all_combinations = itertools.permutations(strings[:-1], len(strings)-1)
    for combination in all_combinations:
        combination = "".join(combination)+strings[-1]
        all_alphabets.append(combination)
    return all_alphabets


# import all common words to RAM
for line in common_words_file:
    common_words.append(line.strip())


def decrypt(shift_key, shift_key2, alphabet, lock):
    for shift_key2 in range (len(alphabet)):
        for shift_key3 in range(len(alphabet)):
                out = ''
                shift = {
                    0: shift_key,
                    1: shift_key2,
                    2: shift_key3
                }
                # simple cipher
                for i, letter in enumerate(encrypted_message):
                    out += alphabet[(alphabet.index(letter) +
                                    shift.get(i % 3)) % len(alphabet)]
                # checks if output has any common words
                for word in out.split(' '):
                    if word.lower() in strict_words:
                        lock.acquire()
                        print(str(shift_key) + ' ' + str(shift_key2) + ' ' + str(shift_key3) + ' ' + word + ' ' + out   + '\n')
                        lock.release()
                        break

def main():
    #mutex lock
    lock = multiprocessing.Lock()
    # get words from common words with length 4+
    for word in common_words:
       if len(word) >= 4 and word not in strict_words:
           strict_words.append(word)   
    
    # create threads for each shift key 1 and 2        
    jobs = []
    for alphabet_combination in generate_alphabet(alphabet):
    
        for shift_key in range(len(alphabet)):
            # for shift_key2 in range(len(alphabet)):
                p = multiprocessing.Process(target=decrypt, args=(shift_key, 0, alphabet_combination, lock))
                jobs.append(p)
                p.start()
        for job in jobs:
            job.join()

if __name__ == '__main__':
    main()
