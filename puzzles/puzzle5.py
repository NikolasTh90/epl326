import subprocess, multiprocessing
from multiprocessing.pool import Pool


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
    response = subprocess.run(command.split(), capture_output=True)
    # print(key)

    if response.returncode == 0:
        try:
            stdout = response.stdout.decode('utf-8')
            for word in stdout.split(' '):
                if word in strict_words:
                    print(key, word, stdout)
                    break
        except Exception as e:
            pass
            # print(e)  


if __name__ == '__main__':
    pool = Pool(processes=multiprocessing.cpu_count())
    keys = range(900000, 999999)
    pool.map(decrypt, keys)
