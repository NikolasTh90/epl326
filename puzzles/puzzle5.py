import subprocess

common_words = list()
common_words_file = open('common_words_file.txt', 'r')
# import all common words to RAM
for line in common_words_file:
    common_words.append(line.strip())

strict_words = list()
for word in common_words:
            if len(word) >= 4 and word not in strict_words:
                strict_words.append(word)


for key in range(907500,907550):
    command = 'openssl aes-128-cbc -d -in puzzle5 -pass pass:' + str(key)
    response = subprocess.run(command.split(), capture_output=True)
    if response.returncode == 0:
        try:
            stdout = response.stdout.decode('utf-8')
            for word in stdout.split(' '):
                if word in strict_words:
                    print(key, word, stdout)
                    break
        except Exception as e:
            print(e)  