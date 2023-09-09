
#first argument is file name, second argument is mode - read (r is default ), write w (creates file, or opens existing one), 
#r+ read and write, x - write if file doesn't exist yet, a -open existing file and then append, b - store binary data



#WRITE
"""
f = open('demo.txt', mode='w')  # => open returns a file object (f)
f.write('Hello from Python')   # allows us to write string to that file

f.close()   # for the reason 2 lines bellow it is important to close the file

user_input = input('Testing: ') # -> if we don't close the file after starting some new code like this line here, python would ask for input
                                # -> file demo.txt will be created but nothing will be written inside of it
"""





#READ
"""
f = open('demo.txt', mode='r')
file_content = f.read()
print(file_content)
"""



#APPEND
"""f = open('demo.txt', mode='a')  # => open returns a file object (f)
f.write('Hello from Python again\n')
f.close()
"""






#READ MULTIPLE LINES
"""f = open('demo.txt', mode='r')
file_content = f.readlines()
print(file_content)
f.close()


for line in file_content:
    print(line[:-1])        #gives us the whole line except the last character which is \n
    """




#READ ONE LINE AT A TIME
"""f = open('demo.txt', mode='r')
line = f.readline()
while line:
    print(line)
    line = f.readline()
f.close()"""





with open('demo.txt', mode='w') as f:   # "with - as" will automatically close our open file so we don't need to close it manually
    # f.write('Add this content!\n')
    # file_content = f.readlines()
    # f.close()

    # for line in file_content:
    #     print(line[:-1])
    # line = f.readline()
    # while line:
    #     print(line)
    #     line = f.readline()
    f.write('Testing if this closes...')
user_input = input('Testing: ')
print('Done!')