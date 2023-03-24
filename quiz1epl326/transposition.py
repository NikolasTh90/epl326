import math


def decryptMessage(key, message):

    numOfColumns = math.ceil(len(message) / key)
    numOfRows = key
    numOfShadedBoxes = (numOfColumns * numOfRows) - len(message)
    plaintext = [''] * numOfColumns
    col = 0
    row = 0
    for symbol in message:
        plaintext[col] += symbol
        col += 1 # point to next column
        if (col == numOfColumns) or (col == numOfColumns - 1 and row >= numOfRows - numOfShadedBoxes):
            col = 0
            row += 1
    return ''.join(plaintext)



if __name__ == '__main__':

    message = 'Cenoonommstmme oo snnio. s s c'
    
    for i in range(1,len(message)+1):
        myKey = i
        plaintext = decryptMessage(myKey, message)
        print(str(myKey) +  " " + plaintext + '|')
    
    