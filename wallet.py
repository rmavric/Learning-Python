from Crypto.PublicKey import RSA    #algorithm for generating private and public keys
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
import Crypto.Random
import binascii


class Wallet:
    """Creates, loads and holds private and public keys. Manages transaction signing and verification."""





    def __init__(self):
        self.private_key = None
        self.public_key = None





    def create_keys(self):
        """Create a new pair of private and public keys."""
        private_key, public_key = self.generate_keys()      #we get private and public key using unpacking
        self.private_key = private_key
        self.public_key = public_key





    def save_keys(self):
        """Saves the keys to a file (wallet.txt)."""
        if self.public_key != None and self.private_key != None:    #We don't want to save None to a file
            try:
                with open('wallet.txt', mode='w') as f:
                    f.write(self.public_key)
                    f.write('\n')
                    f.write(self.private_key)
            except (IOError, IndexError):
                print('Saving wallet failed...')





    def load_keys(self):
        """Loads the keys from the wallet.txt file into memory."""
        try:
            with open('wallet.txt', mode='r') as f:
                keys = f.readlines()
                public_key = keys[0][:-1]       # '\n' is a character that is added after public key and is a part of this first line
                                                # so we used [:-1] to avoid last character
                private_key = keys[1]
                self.public_key = public_key
                self.private_key = private_key
        except (IOError, IndexError):
            print('Loading wallet failed...')





    def generate_keys(self):
        """Generate a new pair of private and public key."""
        private_key = RSA.generate(1024, Crypto.Random.new().read) # 1024 bits, higher is safer, random function
                                                                   # read => to get that generated random function
                                                                   # we get private key
        public_key = private_key.publickey()            # we can access private key and we get public key
                                                        # they are connected and work together
        return (binascii.hexlify(private_key.exportKey(format='DER')).decode('ascii'), binascii.hexlify(public_key.exportKey(format='DER')).decode('ascii'))
        #private and public key are in binary format    => binascii converts binary to ascii
                                                    #   => hexlify => converts binary data to hexadecimal representation
                                                    #   => exportKey(format='DER')  => binary encoding
                                                    #   => decode('ascii')  => converts hexadecimal representation of data to ascii
        #we return TUPLE of private_key and public_key




    def sign_transaction(self, sender, recipient, amount):
        """Sign a transaction and return the signature.

        Arguments:
            :sender: The sender of the transaction.
            :recipient: The recipient of the transaction.
            :amount: The amount of the transaction.
        """
        signer = PKCS1_v1_5.new(RSA.importKey(binascii.unhexlify(self.private_key)))    #private key is used for signing
                                                                                        # => binascii converts binary to ascii
                                                    #   => unhexlify => converts hexadecimal representation to binary data 
                                                    #   => importKey(format='DER')  => binary encoding
                                                    #   => decode('ascii')  => converts hexadecimal representation of data to ascii
        h = SHA256.new((str(sender) + str(recipient) + str(amount)).encode('utf8'))
        signature = signer.sign(h)              #here we generate signature -> in binary format by default
        return binascii.hexlify(signature).decode('ascii')      # we return that signature as a string
                                                                # hexlify => converts binary data to hexadecimal representation
                                                                #   => decode('ascii')  => converts hexadecimal representation of data to ascii




    @staticmethod           #we don't need anything from this class, so self is not needed, we only pass an argument from outside (transaction)
    def verify_transaction(transaction):
        """Verify the signature of a transaction.

        Arguments:
            :transaction: The transaction that should be verified.
        """
        public_key = RSA.importKey(binascii.unhexlify(transaction.sender))  # => transaction.sender is actually public key of a sender
        verifier = PKCS1_v1_5.new(public_key)
        h = SHA256.new((str(transaction.sender) + str(transaction.recipient) + str(transaction.amount)).encode('utf8'))
        return verifier.verify(h, binascii.unhexlify(transaction.signature))
                        #true if it is valid
                        #false if it is invalid