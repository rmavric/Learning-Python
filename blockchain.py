#import functools    #package name, gives us access to reduce function
from functools import reduce    # => now we import only reduce method from functools and now we don't call reduce method like this functools.reduce()
                                # now we call it only reduce
import hashlib as hl     #package for hashing
import json         #to convert dictionary to string hash
from collections import OrderedDict     #for order dictionaries because we need to hash them and we need to have the same hash
                                        #if key-value pairs in dictionaries change positions hash would be different

# Import two functions from our hash_util.py file. Omit the ".py" in the import
from hash_util import hash_string_256, hash_block
import pickle       # convert python data to binary data => it can serialize and deserialize data



# Initializing our (empty) blockchain list
blockchain = []     # List => mutable, ordered duplicates allowed
open_transactions = []
owner = 'Max'
genesis_block = {       #we use this genesis_block so we won't get error when we are executing mine_block function for the first time
                        #we add this to the blockchain first, for now
    'previous_hash': '',      # for now is a dummy
    'index': 0,    # this is like an index, because if we have only one block in blockchain, length would be 1, so index of the next one would be 1
    'transactions': [],
    'proof': 100        #we need to add this when we included proof of work to our code
}
blockchain = [genesis_block]

participants = {'Max'}  #this is a SET => mutable, unordered list, no duplicates
                        #we added Max because it is a owner, so it is a participant

#capital letters mean that this is a global constant -> this value should stay unchanged
MINING_REWARD = 10  #this is a reward that should be given to a person that creates a new block




# this is not the best way of saving and loading data, because we need some code to translate list data to strings and then translate them
# back to python objects and lists
"""
def load_data():
    with open('blockchain.txt', 'r') as f:
        file_content = f.readlines()

        global blockchain               # lines below wanted to create new variables blockchain and open transactions
        global open_transactions        # that is why we need to tell python that those are global variables

        blockchain = file_content[0]    # first string in our file is blockchain data and the second one are open_transactions
        open_transactions = file_content[1]


load_data()


def save_data():
    with open('blockchain.txt', 'w') as f:
        f.write(str(blockchain))    # blockchain is a list so we need to convert it to a string, because only strings can be saved in files
        f.write('\n')
        f.write(str(open_transactions))     # open_transactions is a list so we need to convert it to a string, because only strings can be saved in files
"""




### WE NEED TO HAVE BLOCKCHAIN.TXT FILE FIRST
def load_data():
    """Initialize blockchain + open transactions data from a file."""
    global blockchain               # lines below wanted to create new variables blockchain and open transactions
    global open_transactions        # that is why we need to tell python that those are global variables
    
    #with open('blockchain.p', mode='rb') as f:
    with open('blockchain.txt', mode='r') as f:
        
        file_content = f.readlines()
        
        # file_content = pickle.loads(f.read())       #this opens binary data and converts to python data
        #                                             #this should give as dictionary as we created in save data
        # blockchain = file_content['chain']
        # open_transactions = file_content['ot']
        
        
        blockchain = json.loads(file_content[0][:-1])       #this deserializes a string => takes string in json format and gives us back python object
                                                            #this first line includes \n character so we should avoid reading it with [:-1]


        # We need to convert the loaded data because Transactions should use OrderedDict
        updated_blockchain = []
        for block in blockchain:    #we are going throug every block in blockchain and convert transaction in OrderedDict of transactions
                                    #because we always need to have the same hash
                                    #we save then as orderedDict-s but we don't load them as such, so we need to convert transactions to orderedDicts
            updated_block = {
                'previous_hash': block['previous_hash'],    #this is unchanged
                'index': block['index'],                    #this is unchanged
                'proof': block['proof'],                    #this is unchanged
                'transactions': [OrderedDict(   #we add this to order key-value pairs in transactions => this is important to always get the same hash
                                                #it doesn't take normal dictionary as arguments, it takes list of TUPLES 
                                                #each TUPLE is key-value pair
                    [('sender', tx['sender']), ('recipient', tx['recipient']), ('amount', tx['amount'])]) for tx in block['transactions']]
                    #THIS IS A LIST COMPREHENSION
            }
            updated_blockchain.append(updated_block)
        blockchain = updated_blockchain     # we now overwrite originally blockchain read from the file with new updated_blockchain that has
                                            # transactions converted in orderedDict


        open_transactions = json.loads(file_content[1])     #this deserializes a string => takes string in json format and gives us back python object
        # We need to convert  the loaded data because Transactions should use OrderedDict
        updated_transactions = []
        for tx in open_transactions:
            updated_transaction = OrderedDict(  #we add this to order key-value pairs in transactions => this is important to always get the same hash
                                                #it doesn't take normal dictionary as arguments, it takes list of TUPLES 
                                                #each TUPLE is key-value pair
                [('sender', tx['sender']), ('recipient', tx['recipient']), ('amount', tx['amount'])])
            updated_transactions.append(updated_transaction)
        open_transactions = updated_transactions


load_data()






def save_data():
    """Save blockchain + open transactions snapshot to a file."""
    #with open('blockchain.p', mode='wb') as f:
    with open('blockchain.txt', mode='w') as f:
        f.write(json.dumps(blockchain))         #this will create json string from list blockchain
        f.write('\n')
        f.write(json.dumps(open_transactions))  #this will create json string from list open_transactions
        
        
        
        # save_data = {                       #this object (dictionary) is needed because we cannot add "\n" to binary data
        #     'chain': blockchain,
        #     'ot': open_transactions
        # }
        # f.write(pickle.dumps(save_data))    #dumps returns binary data that we want to write
        #                                     #if we want to save binary data to file we need to use mode "wb" (write binary)
        #                                     #since these data is binary data so we can't add "\n" so we need to store these data like an object
        #                                     #so above is object created
    print('Saving failed!')





"""THIS IS ADDED TO HASH_UTIL.PY"""
# def hash_block(block):
#     """Hashes a block and returns a string representation of it.

#     Arguments:
#         :block: The block that should be hashed.
#     """
#     # return '-'.join([str(block[key]) for key in block])   
#     #return hl.sha256(json.dumps(block).encode()).hexdigest()    #BUT THIS IS NOT ACTUALLY CORRECT BECAUSE BLOCK IS A DICTIONARY, 
#                                                                 #AND KEY-VALUE PAIRS IN DICTIONARIES ARE NOT ORDERED, key-value pairs can change positions
#                                             # algorithm that creates 64 character hash   => same input results with the same hash
#                                             # input argument sholud be string, but block is a dictionary
#                                             # json.dumps(block)  => this will create string but we need to encode it to utf8 
#                                             # (this is string format that can be used with sha256 algorithm)
#                                             # this now returns type byte hash and not a string
#                                             # to make string we use .hexdigest()

#     return hl.sha256(json.dumps(block, sort_keys=True).encode()).hexdigest()    #sort_keys=True => this fixes problem with sorting of key-value pairs
#                                                                                 #because key-value pairs in dictionaires are not ordered
#                                                                                 #but in blocks are also lists of transactions that are also dictionaries
#                                                                                 #the same problem is here




# ADDITIONAL SECURITY MECHANISM
# control amount of coins, not total amount of coins but speed with which new coins enter our network
# important concept that ensures that we cannot edit entire blockchain
# previous block could be edited and all subsequent hashes and than we would have valid block   => proof of work ensures that this is not possible
# HASH IS GENERATED BASED ON THE BLOCK TRANSACTIONS, PREVIOUS HASH AND PROOF NUMBER (NONCE)
       # => TRANSACTIONS AND PREVIOUS HASH SHOULD BE INCLUDED IN NEW BLOCK
       # => WE CHECK IF PROOF OF WORK IS VALID BY COMBINING TRANSACTIONS + PREVIOUS HASH + PROOF TO HASH    => 64 characters
                   # => WE NEED TO CHECK IF THIS HASH START WITH CERTAIN AMOUNT OF LEADING ZEROS
                   # => WE ALWAYS GET &$ CHARACTERS FROM THESE INPUTS
                            # => IF WE CHANGE ANYTHING FROM THESE INPUTS (AND WE CAN CHANGE NUMBER ONLY, BECAUSE TRANSACTIONS AND PREVIOUS HASH ARE SET IN STONE)
                            # => IF WE CHANGE THAT NUMBER WE GET TOTALLY DIFFERENT HASH
                            # WE NEED A COUPLE OF TRIES TO GET A HASG THAT STARTS WITH TWO LEADING ZEROS
                            # THAN THIS PROOF OF WORK IS VALID (if 2 zeros are our criteria), IT TAKES MORE TIME IF WE REQUIRE MORE LEADING ZEROS

# miners that are hones -> when they mine new coins they need to create on new block
# hakers that want to manipulate with some block need to update hashes in all subsequent block

# contains algorithm for generating hash and checks if it fulfils our difficulty criteria
def valid_proof(transactions, last_hash, proof):
    """Validate a proof of work number and see if it solves the puzzle algorithm (two leading 0s)

    Arguments:
        :transactions: The transactions of the block for which the proof is created.
        :last_hash: The previous block's hash which will be stored in the current block.
        :proof: The proof number we're testing.
    """
    # Create a string with all the hash inputs
    guess = (str(transactions) + str(last_hash) + str(proof)).encode()  #endode to utf 8 characters

    # Hash the string
    # IMPORTANT: This is NOT the same hash as will be stored in the previous_hash. It's a not a block's hash. It's only used for the proof-of-work algorithm.
    #guess_hash = hl.sha256(guess).hexdigest()   # to convert byte hash type to a string
    guess_hash = hash_string_256(guess)     # this returns => return hl.sha256(string).hexdigest()
    
   
    print(guess_hash)
    # Only a hash (which is based on the above inputs) which starts with two 0s is treated as valid
    # This condition is of course defined by you. You could also require 10 leading 0s - this would take significantly longer (and this allows you to control the speed at which new blocks can be added)
    
    return guess_hash[0:2] == '00'  #checks if first two characters are zeros ([0:2] means element with index 0 and 1, index 2 is not included)





def proof_of_work():
    """Generate a proof of work for the open transactions, the hash of the previous block and a random number (which is guessed until it fits)."""
    last_block = blockchain[-1]     #this fetches last block in blockchain
    last_hash = hash_block(last_block)      #this is the hash of the last block
    proof = 0
    # Try different PoW numbers and return the first valid one
    while not valid_proof(open_transactions, last_hash, proof):
        proof += 1
    return proof    #we will return proof when we find what number is proof that will give guess_hash that starts with "00"





def get_last_blockchain_value():
    """ Returns the last value of the current blockchain. """
    if len(blockchain) < 1:
        return None
    return blockchain[-1]

# This function accepts two arguments.
# One required one (transaction_amount) and one optional one (last_transaction)
# The optional one is optional because it has a default value => [1]





#this will check if participant stil has a balance left 
#if he has lower balance than it wants to send than this validation would fail
def verify_transaction(transaction):
    #sender_sent, sender_received = get_balance(transaction['sender'])  
    #here above when we are getting the balance we calculate how much coins sender sent in previous block
    #and how many coins does he wants to send in currently open_transactions
    #sender_balance = sender_received - sender_sent
    sender_balance = get_balance(transaction['sender'])
    if sender_balance >= transaction['amount']:
        return True
    else: 
        return False




#here we store new transaction
def add_transaction(recipient, sender=owner, amount=1.0):   #if we set sender=owner and amount = 1.0 now those two are optional parameters
    """ Append a new value as well as the last blockchain value to the blockchain.

    Arguments:
        :sender: The sender of the coins.
        :recipient: The recipient of the coins.
        :amount: The amount of coins sent with the transaction (default = 1.0)
    """

    #   Dictionary => mutable, unordered map, no duplicate keys => key-value pairs
    # transaction = {     
    #     'sender': sender,
    #     'recipient': recipient,
    #     'amount': amount
    # }

    transaction = OrderedDict(          #we add this to order key-value pairs in transactions => this is important to always get the same hash
                                        #it doesn't take normal dictionary as arguments, it takes list of TUPLES 
                                        #each TUPLE is key-value pair
        [('sender', sender), ('recipient', recipient), ('amount', amount)])

    if verify_transaction(transaction):   
        open_transactions.append(transaction)   #we store this transaction to open_transactions
        participants.add(sender)                #as the sender is Max this would be duplicated item but this line of code will be ignored since in set only go unique values
        participants.add(recipient)

        save_data()     # here we write/save open_transactions to file

        return True
    else:
        return False






#creates new block to a blockchain
#when this function is called, new block is created, all open_transactions are added in new block, and new block is then added to blockchain
#open_transactions are then cleared
#when we are mining a new block we want to get a reward => this is how coins get into the system
def mine_block():
    #pass    #pass statement python knows that this function doesn't do anything for now, it's just declared
             #if we don't write pass it would be an error
    last_block = blockchain[-1]     # this gives us last element in blockchain
                                    # when first time mine_block is executed blockchain list is empty so blockchain[-1] will throw error

    # hashed_block = ''
    # hashed_block = str([last_block[key] for key in last_block]) #list comprehension
    # this gives us a list of values => and we just put this list to string

    # hashed_block = '-'.join([str(last_block[key]) for key in last_block])  
    # it changes every element of last_block list to string and then joins them using character '-' => so we get hashed_block = -0-[] for example
    # and we need to use strings because join works only with strings

    hashed_block = hash_block(last_block)

    proof = proof_of_work()

    # reward_transaction = {                             
    #     'sender': 'MINING',     #MINING => because it's coming out of the system     
    #     'recipient': owner,     #recipient is a person who does the mining
    #     'amount': MINING_REWARD     #constant amount
    # }  


    reward_transaction = OrderedDict(        #we add this to order key-value pairs in transactions => this is important to always get the same hash
                                             #it doesn't take normal dictionary as arguments, it takes list of TUPLES 
                                             #each TUPLE is key-value pair
        [('sender', 'MINING'), ('recipient', owner), ('amount', MINING_REWARD)])


    #copied_transactions = open_transactions     #lists are copied by reference and not by value so this doesn't work
                                                 #this would mean that both lists would point to the same address in memory
                                                 #if we change element in copied_list it would also change element in open_transactions list
                                                 #because they point at the same place in memory
    copied_transactions = open_transactions[:]      #this will copy the whole list    => : represents range
                                                    #we can define from 1:10 for example
                                                    #now if we modified element in copied_transactions it would change only element in 
                                                    #this list
    #open_transactions.append(reward_transaction)       => now we use buttom one
    copied_transactions.append(reward_transaction)

    """for key in last_block: #if we use for loop on dictionary it will loop through the keys, and not through the values
        value = last_block[key]
        hashed_block = hashed_block + str(value);   #all values of transaction are stringified"""
    
    print(hashed_block)


    block = {       # Dictionary => key - value pairs                       
        'previous_hash': hashed_block,      # for now is a dummy
        'index': len(blockchain),    # this is like an index, because if we have only one block in blockchain, length would be 1, so index of the next one would be 1
        'transactions': copied_transactions,
        'proof': proof
    }  
    blockchain.append(block)


    return True
    





def get_transaction_value():
    """ Returns the input of the user (a new transaction amount) as a float. """
    # Get the user input, transform it from a string to a float and store it in user_input
    #tx_sender = input('Enter the sender of the transafction')
            #we are sender so this would be commented => we set the owner above at the beginning
    tx_recipient = input('Enter the recipient of the transaction: ')
    tx_amount = float(input('Your transaction amount please: '))
    return tx_recipient, tx_amount          #   TUPLE => immutable, ordered list, no duplicates
                                            #   if we have only one value we can write it without parentheses





def get_user_choice():
    """Prompts the user for its choice and return it."""
    user_input = input('Your choice: ')
    return user_input





def print_blockchain_elements():
    """ Output all blocks of the blockchain. """
    # Output the blockchain list to the console
    for block in blockchain:
        print('Outputting Block')
        print(block)
    else:
        print('-' * 20)




#to find out how much coins has participant sent, and how much received
def get_balance(participant):
    #we need to find out transactions where this participant was the sender
    #we need to find amount of every transaction in the block where sender is equal person as participant => there are many transactions inside block
    #and we also need to find amounts in the whole blockchain which is a list of blocks (and block is a list of transactions)
    #we are getting amount for a given transaction for all transactions in a block if sender is a participant
    #and then we go through all the blocks in blockchain
    tx_sender = [[tx['amount'] for tx in block['transactions'] if tx['sender']==participant] for block in blockchain]     #nested list comprehension

    open_tx_sender = [tx['amount'] for tx in open_transactions if tx['sender']==participant]

    tx_sender.append(open_tx_sender)        # we now have a list of all transactions for specific sender that are currently saved in all blocks in the blockhain and with transactions that are stil open
    print(tx_sender)
    
    # amount_sent = functools.reduce(lambda tx_sum, tx_amount: tx_sum + sum(tx_amount) if len(tx_amount)> 0 else tx_sum + 0, tx_sender, 0)
    amount_sent = reduce(lambda tx_sum, tx_amount: tx_sum + sum(tx_amount) if len(tx_amount)> 0 else tx_sum + 0, tx_sender, 0)

        # first argument => function that will be executed on every step
                    #    => this function receives last and the current value
                    #    => tx_sum is last sum of list elements and tx_amount is actually first element of tx_sender 
                    #       and tx_sender is list of nested list, so we need to access first element of every nested list like in summing logic below
                    #    => if we don't have first element in tx_amount[0] we need to have if statement
        # second argument => it receives list on which we want to do reduction
        # third argument => and receives initial value
        # simle:list = [1,2,3,4,5,6]    => this code above sums all elements last value = 1, curent value = 2
        #                               => last value = 3, current value = 3
        #                               => last value = 6, current value = 4
        
        # This fetches received coin amounts of transactions that were already included in blocks of the blockchain
        # We ignore open transactions here because you shouldn't be able to spend coins before the transaction was confirmed + included in a block
    
    
    #OLD SUMMING LOGIC
    # amount_sent = 0
    # for tx in tx_sender:
    #     if len(tx)>0:
    #        amount_sent += tx[0]

    tx_recipient = [[tx['amount'] for tx in block['transactions'] if tx['recipient']==participant] for block in blockchain]     #nested list comprehension
    # amount_received = functools.reduce(lambda tx_sum, tx_amount: tx_sum + sum(tx_amount) if len(tx_amount)> 0 else tx_sum + 0, tx_recipient, 0)
    amount_received = reduce(lambda tx_sum, tx_amount: tx_sum + sum(tx_amount) if len(tx_amount)> 0 else tx_sum + 0, tx_recipient, 0)


    #OLD SUMMING LOGIC
    # amount_received = 0
    # for tx in tx_recipient:
    #     if len(tx)>0:
    #         amount_received += tx[0]

    return amount_received - amount_sent 
    #return (amount_sent, amount_received) #or amount_received - amount_sent 





def verify_chain():
    # Verify the current blockchain and return True if it's valid, False otherwise.

    # we are hashing values from previous block to the hash key of next block
    # if hash from previous block doesn't match recalculated hash than validation fails (that means that we changed previous block)
    # we want to compare stored hash in current block with recalculated hash of previous block


    # block_index = 0
    is_valid = True
    """for block_index in range(len(blockchain)):
        if block_index == 0:
            # If we're checking the first block, we should skip the iteration (since there's no previous block)
            continue
        # Check the previous block (the entire one) vs the first element of the current block
        elif blockchain[block_index][0] == blockchain[block_index - 1]:
            is_valid = True
        else:
            is_valid = False
    #         break
    # for block in blockchain:
    #     if block_index == 0:
    #         block_index += 1
    #         continue
    #     elif block[0] == blockchain[block_index - 1]:
    #         is_valid = True
    #     else:
    #         is_valid = False
    #         break
    #     block_index += 1
    return is_valid
"""
    
    for (index, block) in enumerate(blockchain): # ENUMERATE function => if we wrap a LIST inside ENUMERATE function it will give back a TUPLE which contains INDEX of element and ELEMENT
       
        if index == 0:  #we can skip validation for first block => this is genesis block
            continue

        if block['previous_hash'] != hash_block(blockchain[index-1]):
        # block['previous_hash']    => every block that we store has this key
        # hash_block(blockchain[index-1])   => index is a index of current block so we have previous block and we need to hash it => so if those two are the same validation succeded
        # if we manipulated previous block this would mean that this should be invalid
            return False
        
        if not valid_proof(block['transactions'][:-1], block['previous_hash'], block['proof']): #we need to exclude reward_transactions
                                                                                                # with [:-1] we select all transactions except from the last, 
                                                                                                # and last is reward_transactions
            print('Proof of work is invalid')
            return False
    
    return True





def verify_transactions():
    # is_valid = True
    # for tx in open_transactions:
    #     if verify_transaction(tx):
    #         is_valid = True
    #     else:
    #         is_valid = False
    # return is_valid
    return all([verify_transaction(tx) for tx in open_transactions])    # => returns TRUE if all transactions are valid or FALSE if
                                                                        #    any transaction is invalid



waiting_for_input = True
# A while loop for the user input interface
# It's a loop that exits once waiting_for_input becomes False or when break is called
while waiting_for_input:
    print('Please choose')
    print('1: Add a new transaction value')
    print('2: Mine a new block')
    print('3: Output the blockchain blocks')
    print('4: Output participants')
    print('5: Check transaction validity')
    print('h: Manipulate the chain')
    print('q: Quit')
    user_choice = get_user_choice()
    if user_choice == '1':
        tx_data = get_transaction_value()       #   here we get the data from TUPLE
        recipient, amount = tx_data             #   DATA UNPACKING => because tx_data is a TUPLE we extract data from TUPLE like this
                                                #   first element of the TUPLE is stored in recipient, and second one is stored in amount
        # Add the transaction amount to the blockchain
        if add_transaction(recipient, amount=amount):       #   this data is now added to open_transactions
                                                            #   here we avoid parameter sender because it is optional
                                                            #   amount = amount => this we need to set if we omit sender parameter
            print('Added transaction!')
        else:
            print('Transaction failed!')
        print(open_transactions)
    elif user_choice == '2':
        if mine_block():    #we call function mine_block here, and if this function return True open_transaction will be set to []
            open_transactions = []
            save_data()     # here we write/save open_transactions to file
    elif user_choice == '3':
        print_blockchain_elements()
    elif user_choice == '4':
        print(participants)
    elif user_choice == '5':
        if verify_transactions():
            print('All transactions are valid!')
        else: 
            print('There are invalid transactions!')
    elif user_choice == 'h':
        # Make sure that you don't try to "hack" the blockchain if it's empty
        if len(blockchain) >= 1:
            # blockchain[0] = [2]
            blockchain[0] = {       
                'previous_hash': '',    
                'index': 0,  
                'transactions': [{'sender': 'Cris', 'recipient': 'Max', 'amonut': 100.0}]
            }
    elif user_choice == 'q':
        # This will lead to the loop to exist because it's running condition becomes False
        waiting_for_input = False
    else:
        print('Input was invalid, please pick a value from the list!')
    if not verify_chain():
        print_blockchain_elements()
        print('Invalid blockchain!')
        # Break out of the loop
        break

    # print(get_balance('Max'))
    print('Balance of {}: {:6.2f}'.format('Max', get_balance('Max')))
else:
    print('User left!')





print('Done!')



#A transaction is treated as an "Open Transaction" until it's included in a new block.
#Only transactions that are part of a block have been "processed" and their attached amounts are hence available to the recipient.
#One Block typically contains more than one Transaction - in this course, we'll simply add all open transactions.
# Once the Block has been created, the "Open Transactions" are of course cleared.


# List comprehension
# simple_list = [1, 2, 3, 4]
# doubled_list = []
# doubled_list = [el*2 for el in simple_list]       #for every element in simple_list multiply every element with 2 => double_list = 2, 4, 6, 8 

# using if condition inside list comprehension
# dup_list = [el*2 for el in simple_list if el el%2==0]   #we get only 4, 8 => it multiplies only elements that are divideable with 2 

# calc_items = [1, 2]
# dup_list = [el*2 for el in simple_list if el in calc_items]   #we get only 2, 4 because we multiply only those elements from simple_list that are also inside the calc_items list 


# Dict comprehension
# stats = [('age', 29), ('height', 178), ('weight', 72)]    #this is a LIST of TUPLES
# dict_stats = {key: value for (key, value) in stats}   #this transforms every key value pair from LIST of TUPLES to DICTIONARY
                                                        #this is unpacking from TUPLES (key, value) in stats



#Copying one list to another
#copied_transactions = open_transactions        #lists are copied by reference and not by value so this doesn't work
                                                 #this would mean that both lists would point to the same address in memory
                                                 #if we change element in copied_list it would also change element in open_transactions list
                                                 #because they point at the same place in memory
#copied_transactions = open_transactions[:]             #this will copy the whole list    => : represents range
                                                        #we can define from 1:10 for example
                                                        #now if we modified element in copied_transactions it would change only element in 
                                                        #this list
                                    
#simple_list = [1,2,3,4,5]
#new_list = None
#new_list = simple_list[0:3]    => it gives 1, 2, 3 => 0 is starting index, included
#                               => it goes to the index 3, but element at index 3 is not included
#new_list = simple_list[:-1]    => it gives all values except the last one
#                               => it goes from beginning to the -1 from the end
# IT WORKS ON TUPLE ALSO, on DICTIONARIES and SETs doesn't work because they are not ordered lists


#DEEP COPIES
# stats = [{'name', 'Max'}, {'age', 29}]       => list of dictionaries
# copied_stats = stats[:]
# copied_stats[0]['name'] = 'Manuel'    => name is changed from Max to Manuel in copied_stats but also in stats
# THIS IS A SHALLOW COPY => IT WORKS FINE IF SIMPLE DATA STRUCTURES ARE USED IN LISTS
#                        => BUT HERE WE USE DICTIONARIES INSIDE LISTS, AND DICTIONARIES ARE MORE COMPLEX DATA STRUCTURES
#                               -> in this example we need to use deep copy
# copied_stats = [stat.copy() for stat in stats]    => this now is a deep copy


#simple_list = [1,2,3,4]
#second_list = [1,2,3,4]
#simple_list == second_list => True because they hold the same values
#simple_list is second_list => False because they are not the same object in memory


#simple_list = [1,2,3,4]
#simple_list.extend([5,6,7])


#d = {'name','Max'}
#print(d.items())   => this prints list of dictionaries as a TUPLE
#            =
#for k,v in d.items():
#    print (k, v)


#tuple1 = (1,2,3)
#print(tuple1.index(1)) => it prints index of element 1 which is 0
#                       => if there is no such element in tuple it gives error


#del(d['name'])  => it deletes from dictionary  (it also works for lists)
#del(tuple1[0])  => it doesn't delete because tuple is immutable
#                            => this is also true for SETs



#new_list = [True, True, False]
# any(new_list) => True => it checks if any element is true
# all(new_list) => False => it checks if all element are true


#number_list = [1, 2, 3, -5]
#[el for el in number_list if el > 0]   => 1, 2, 3
#[el > 0 for el in number_list]     => True, True, True, False
#all([el > 0 for el in number_list])    => False, if all are greater than 0





#STRINGS
#name = 'Max'
#age = 29
#'I am ' + name + ' and I am ' + str(age) + ' years old.'
#'I am {0} and I am {1} years old.'.format(name, age)
#'I am {0} and I am {1} years old. I really am named {0}'.format(name, age)

#'I am {name} and I am {years} years old. I really am named {name}'.format(name=name, years=age)

#f'I am {name} and I am {age} years old.'    => directly references variable names in there
#f'I am {name} and I am {age:.2f} years old.'    => directly references variable names in there (two decimal points works also)


#funds = 150.9723
#'Funds: {}'.format(funds)  => 150.9723
#'Funds: {:f}'.format(funds)  => 150.972300, float
#'Funds: {:.1f}'.format(funds)  => 151.0, float with 1 decimal point, immediately rounds up/down 
#'Funds: {:10.1f}'.format(funds)  =>        151.0, float with 1 decimal point, but reserves 10 places in front of decimal point 


#'I\'m Max' => ok
#"I'm Max" => ok
#'I'm Max' => not ok





#MAP    => ALTERNATIVE TO LIST COMPREHENSION
#simple_list = [1,2,3,4]
# def multiply(el):
#     return el*2

#map(multiply, simlpe_list) => we get a map object
        #=> first argument is reference to a function where we define what we want to do with second parameter (with every element in simple_list)
#list(map(multiply, simple_list))   => we get list of every element times two

#list(map(str, simple_list))    => converts every element of a simple_list o string





#LAMBDA FUNCTIONS
#list(map(lambda el: el*2, simple_list)) => the same as this -> list(map(multiply, simple_list))
            #=> word lambda defines that this wil be lambda expression
            #=> after lambda go parameters, and after parameters is : 
            #=> then we define what we do with parameters





# REDUCE => we use if we want to summarize a list to one value only