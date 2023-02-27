import subprocess, multiprocessing
from multiprocessing.pool import Pool
# multiprocessing.set_start_method('fork')

common_words = list()
common_words_file = open('common_words_file.txt', 'r')
# import all common words to RAM
for line in common_words_file:
    common_words.append(line.strip())

strict_words = list()
for word in common_words:
            if len(word) >= 4 and word not in strict_words:
                strict_words.append(word)


def decrypt(key):
    command = 'openssl aes-128-cbc -d -in puzzle5 -pass pass:' + str(key)
    response = subprocess.run(command.split(), stdout=subprocess.PIPE)
    # print(key)

    if response.returncode == 0:
        try:
            stdout = response.stdout.decode('utf-8')
            for word in stdout.split(' '):
                if word in strict_words:
                    return "{} {} {}".format(key, word, stdout)
        except Exception as e:
            return "{} Error: {}".format(key, e)

    return "{} Error: {}".format(key, response.returncode)


if __name__ == '__main__':
    print(decrypt(907530))
    pool = Pool(processes=multiprocessing.cpu_count())
    keys = range(907520, 907540)
    results = pool.map(decrypt, keys)
    pool.close()
    pool.join()

    for result in results:
        if not "Error" and not "error" in result:
         print(result)
