import hashlib as hl
import json

def hash_string_256(string):
    """Create a SHA256 hash for a given input string.

    Arguments:
        :string: The string which should be hashed.
    """
    return hl.sha256(string).hexdigest()




def hash_block(block):
    """Hashes a block and returns a string representation of it.

    Arguments:
        :block: The block that should be hashed.
    """
    # return '-'.join([str(block[key]) for key in block])   
    #return hl.sha256(json.dumps(block).encode()).hexdigest()    #BUT THIS IS NOT ACTUALLY CORRECT BECAUSE BLOCK IS A DICTIONARY, 
                                                                #AND KEY-VALUE PAIRS IN DICTIONARIES ARE NOT ORDERED, key-value pairs can change positions
                                            # algorithm that creates 64 character hash   => same input results with the same hash
                                            # input argument sholud be string, but block is a dictionary
                                            # json.dumps(block)  => this will create string but we need to encode it to utf8 
                                            # (this is string format that can be used with sha256 algorithm)
                                            # this now returns type byte hash and not a string
                                            # to make string we use .hexdigest()

    #return hl.sha256(json.dumps(block, sort_keys=True).encode()).hexdigest()    #sort_keys=True => this fixes problem with sorting of key-value pairs
                                                                                #because key-value pairs in dictionaires are not ordered
                                                                                #but in blocks are also lists of transactions that are also dictionaries
                                                                                #the same problem is here

    return hash_string_256(json.dumps(block, sort_keys=True).encode())      # => hash_string_256 => new function that we created