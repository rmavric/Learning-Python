from collections import OrderedDict

from printable import Printable

class Transaction(Printable):
    """A transaction which can be added to a block in the blockchain.

    Attributes:
        :sender: The sender of the coins.
        :recipient: The recipient of the coins.
        :amount: The amount of coins sent.
    """
    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount





    def to_ordered_dict(self):
        """Converts this transaction into a (hashable) OrderedDict."""
        #this is list of TUPLES
        #we need to have transactions set in some order because we need to hash them, and it always needs to be the same hash
        return OrderedDict([('sender', self.sender), ('recipient', self.recipient), ('amount', self.amount)])
    


    """
    def __repr__(self):     #this can be inherited from printable.py
        return str(self.__dict__)
    """