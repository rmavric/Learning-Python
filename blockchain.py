# Initializing our (empty) blockchain list
blockchain = []     # List => mutable, ordered duplicates allowed
open_transactions = []
owner = 'Max'
genesis_block = {       #we use this genesis_block so we won't get error when we are executing mine_block function for the first time
                        #we add this to the blockchain first, for now
    'previous_hash': '',      # for now is a dummy
    'index': 0,    # this is like an index, because if we have only one block in blockchain, length would be 1, so index of the next one would be 1
    'transactions': []
}
blockchain = [genesis_block]





def get_last_blockchain_value():
    """ Returns the last value of the current blockchain. """
    if len(blockchain) < 1:
        return None
    return blockchain[-1]

# This function accepts two arguments.
# One required one (transaction_amount) and one optional one (last_transaction)
# The optional one is optional because it has a default value => [1]





#here we store new transaction
def add_transaction(recipient, sender=owner, amount=1.0):   #if we set sender=owner and amount = 1.0 now those two are optional parameters
    """ Append a new value as well as the last blockchain value to the blockchain.

    Arguments:
        :sender: The sender of the coins.
        :recipient: The recipient of the coins.
        :amount: The amount of coins sent with the transaction (default = 1.0)
    """

    #   Dictionary => mutable, unordered map, no duplicate keys => key-value pairs
    transaction = {     
        'sender': sender,
        'recipient': recipient,
        'amount': amount
    }
    open_transactions.append(transaction)   #we store this transaction to open_transactions






#creates new block to a blockchain
#when this function is called, new block is created, all open_transactions are added in new block, and new block is then added to blockchain
#open_transactions are then cleared
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

    """for key in last_block: #if we use for loop on dictionary it will loop through the keys, and not through the values
        value = last_block[key]
        hashed_block = hashed_block + str(value);   #all values of transaction are stringified"""
    
    print(hashed_block)


    block = {       # Dictionary => key - value pairs                       
        'previous_hash': hashed_block,      # for now is a dummy
        'index': len(blockchain),    # this is like an index, because if we have only one block in blockchain, length would be 1, so index of the next one would be 1
        'transactions': open_transactions
    }  
    blockchain.append(block)
    





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





def hash_block(block):
    return '-'.join([str(block[key]) for key in block]) 





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
waiting_for_input = True"""
   
    for (index, block) in enumerate(blockchain): # ENUMERATE function => if we wrap a LIST inside ENUMERATE function it will give back a TUPLE which contains INDEX of element and ELEMENT
        if index == 0:  #we can skip validation for first block => this is genesis block
            continue
        if block['previous_hash'] != hash_block(blockchain[index-1]):
        # block['previous_hash']    => every block that we store has this key
        # hash_block(blockchain[index-1])   => index is a index of current block so we have previous block and we need to hash it => so if those two are the same validation succeded
        # if we manipulated previous block this would mean that this should be invalid
            return False
    
    return True



# A while loop for the user input interface
# It's a loop that exits once waiting_for_input becomes False or when break is called
while waiting_for_input:
    print('Please choose')
    print('1: Add a new transaction value')
    print('2: Mine a new block')
    print('3: Output the blockchain blocks')
    print('h: Manipulate the chain')
    print('q: Quit')
    user_choice = get_user_choice()
    if user_choice == '1':
        tx_data = get_transaction_value()       #   here we get the data from TUPLE
        recipient, amount = tx_data             #   DATA UNPACKING => because tx_data is a TUPLE we extract data from TUPLE like this
                                                #   first element of the TUPLE is stored in recipient, and second one is stored in amount
        # Add the transaction amount to the blockchain
        add_transaction(recipient, amount=amount)       #   this data is now added to open_transactions
                                                        #   here we avoid parameter sender because it is optional
                                                        #   amount = amount => this we need to set if we omit sender parameter
        print(open_transactions)
    elif user_choice == '2':
        mine_block()
    elif user_choice == '3':
        print_blockchain_elements()
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