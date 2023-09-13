from uuid import uuid4

from blockchain import Blockchain
from verification import Verification

class Node:
    """The node which runs the local blockchain instance.
    
    Attributes:
        :id: The id of the node.
        :blockchain: The blockchain which is run by this node.
    """
    def __init__(self):
        #self.id = str(uuid4())
        #self.blockchain = []
        self.id = 'MAX'             # just to use as dummy ID, it is better with unique ID
        self.blockchain = Blockchain(self.id)
        





    def get_transaction_value(self):
        """ Returns the input of the user (a new transaction amount) as a float. """
        # Get the user input, transform it from a string to a float and store it in user_input
        #tx_sender = input('Enter the sender of the transafction')
                #we are sender so this would be commented => we set the owner above at the beginning
        tx_recipient = input('Enter the recipient of the transaction: ')
        tx_amount = float(input('Your transaction amount please: '))
        return tx_recipient, tx_amount          #   TUPLE => immutable, ordered list, no duplicates
                                                #   if we have only one value we can write it without parentheses





    
    def get_user_choice(self):
        """Prompts the user for its choice and return it."""
        user_input = input('Your choice: ')
        return user_input





    def print_blockchain_elements(self):
        """ Output all blocks of the blockchain. """
        # Output the blockchain list to the console
        for block in self.blockchain.chain:     #blockchain is an object and we need to loop through chain ob blocks
                                                #this will now execute a getter
            print('Outputting Block')
            print(block)
        else:
            print('-' * 20)






    def listen_for_input(self):
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
            user_choice = self.get_user_choice()
           
           
            if user_choice == '1':
                tx_data = self.get_transaction_value()       #   here we get the data from TUPLE
                recipient, amount = tx_data             #   DATA UNPACKING => because tx_data is a TUPLE we extract data from TUPLE like this
                                                        #   first element of the TUPLE is stored in recipient, and second one is stored in amount
                # Add the transaction amount to the blockchain
                if self.blockchain.add_transaction(recipient, self.id, amount=amount):       #   this data is now added to open_transactions
                                                                    #   here we avoid parameter sender because it is optional
                                                                    #   amount = amount => this we need to set if we omit sender parameter
                    print('Added transaction!')
                else:
                    print('Transaction failed!')
                print(self.blockchain.open_transactions)
           
           
            elif user_choice == '2':
                #if self.blockchain.mine_block():    #we call function mine_block here, and if this function return True open_transaction will be set to []
                    #open_transactions = []
                    #self.blockchain.save_data()     # here we write/save open_transactions to file
                    #THOSE TWO LINES WE NOW ADDED TO BLOCKCHAIN => MINE_BLOCK method
                    self.blockchain.mine_block()    # => WE DON?T NEED TO CHECK IF THIS IS SUCCESSFUL BECAUSE IT CAN'T FAIL ANYWAY
          
          
            elif user_choice == '3':
                self.print_blockchain_elements()
        
        

                """
            elif user_choice == '4':
                print(participants)
                """
          
            elif user_choice == '5':
                #verifier = Verification()
                # if verifier.verify_transactions(self.blockchain.open_transactions, self.blockchain.get_balance):
                # this is now class method so it could be called on CLASS and not on instance
                if Verification.verify_transactions(self.blockchain.get_open_transactions(), self.blockchain.get_balance):
                    print('All transactions are valid!')
                else: 
                    print('There are invalid transactions!')
          
          
                """
            elif user_choice == 'h':
                # Make sure that you don't try to "hack" the blockchain if it's empty
                if len(self.blockchain) >= 1:
                    # blockchain[0] = [2]
                    self.blockchain[0] = {       
                        'previous_hash': '',    
                        'index': 0,  
                        'transactions': [{'sender': 'Cris', 'recipient': 'Max', 'amonut': 100.0}]
                    }
                """
        
            elif user_choice == 'q':
                # This will lead to the loop to exist because it's running condition becomes False
                waiting_for_input = False
        
        
            else:
                print('Input was invalid, please pick a value from the list!')


            #verifier = Verification()
            # if not verifier.verify_chain(self.blockchain.chain):
            # this is now class method so it could be called on CLASS and not on instance
            if not Verification.verify_chain(self.blockchain.chain):
                self.print_blockchain_elements()
                print('Invalid blockchain!')
                # Break out of the loop
                break

            # print(get_balance('Max'))
            print('Balance of {}: {:6.2f}'.format(self.id, self.blockchain.get_balance()))
        else:
            print('User left!')





        print('Done!')





#we need to instanciate Node and call method that will run when we execute node.py
node = Node()
node.listen_for_input()