import time
import pandas as pd
import string
import re


class Cipher(object):
    """
    xxxxx
        
    Parameters
    ==========
    object
    
    
    Returns
    =======
    xxx          module
    
    """
    def __init__(self, daily_key, key_extension=50):
        """
        Instantiate an Cipher object.
        
        Parameters
        ==========
        daily_key       str
                        The predetermined daily key.
        key_extension   integer
                        The number of times to repeat the key to ensure there are enough
                        characters to perform encryption. Default is 50.
        Returns
        =======
        None
        """
        def __build_cipher():
            """
            Internal function for instantiating the tabula recta.
        
            Parameters
            ==========
            None
            
            Returns
            =======
            tab_rect    pandas.DataFrame
                        The tabula recta used in Cipher. A visualized example
                        can be found in README.rst
            """
            punct = "".join(re.split('"', "".join(re.split("'", string.punctuation))))
            indices = list(string.ascii_uppercase + string.digits + punct)
            row_shift = list(string.ascii_lowercase + string.digits + punct)
            tab_rect = pd.DataFrame(0., columns=indices, index=indices)
            for idx, column in enumerate(indices):
                initial = row_shift[idx:]
                final =  row_shift[0:idx]
                tab_rect[column] = initial + final
            return tab_rect
        self.tabula_recta = __build_cipher()
        self.daily_key = "".join(daily_key.upper().split())*key_extension


    def function_timer(wrapped_function):
        """
        Outputs the time a function takes to execute.
        
        Parameters
        ==========
        wrapped_function    function
                            The function to be wrapped.
        Returns
        =======
        wrapper             function
                            "function Cipher.function_timer"
        """
        def wrapper(s, message, code):
            """
            xxxxx
            
            Parameters
            ==========
            s           self
                        Cipher(object).self
            message     str
                        The message passed in to the cipher for encoding or decoding.
            code        str
                        either 'Econding' or 'Decoding'.
                        
            Returns
            =======
            
            """
            t1 = time.time()
            wrapped_function(s, message, code)
            t2 = time.time()
            total = t2 - t1
            if total < 60.:
                total = str(round(total, 3))
                print("\t\t" + code + " time (sec):\t" + total + "\n")
            else:
                total = total/60.
                total = str(round(total, 3))
                print("\t\t" + code + " time (min):\t" + total + "\n")
        return wrapper


    @function_timer
    def encode(self, outgoing_message, print_message=True):
        """
        Encode a message.
        
        Parameters
        ==========
        outgoing_message    str
                            The message passed in to the cipher for encoding.
        print_message       bool
                            Print the message. Default is True.
        Returns
        =======
        encrypted_message   str
                            The outgoing message following encryption.
        """
        
        
        outgoing_message = "".join(outgoing_message.upper().split())
        message_key = self.daily_key[:len(outgoing_message)]
        encrypted_characters = [self.tabula_recta[character][outgoing_message[idx]]\
                                        for idx, character in enumerate(message_key)]
        encrypted_message = "".join(encrypted_characters)
        if print_message:
            print("\t\tMessage Key:\t\t", message_key)
            print("\t\tOutgoing Message:\t", outgoing_message)
            print("\t\tEncrypted Message:\t", encrypted_message)
        self.encoded_message = encrypted_message
        return encrypted_message
    
    
    @function_timer
    def decode(self, incoming_message, print_message=True):
        """
        Decode a message.
        
        Parameters
        ==========
        incoming_message    str
                            The message passed in to the cipher for decoding.
        print_message       bool
                            Print the message. Default is True.
        Returns
        =======
        decrypted_message   str
                            The incoming message following decryption.
        """
        incoming_message = "".join(incoming_message.lower().split())
        message_key = self.daily_key[:len(incoming_message)]
        decrypted_characters = [self.tabula_recta[self.tabula_recta[message_key[idx]]\
                                                  == character].index[0]\
                                                  for idx, character\
                                                  in enumerate(incoming_message)] 
        decrypted_message = "".join(decrypted_characters).upper()
        if print_message:
            print("\t\tMessage Key:\t\t", message_key)
            print("\t\tIncoming Message:\t", incoming_message)
            print("\t\tDecrypted Message:\t", decrypted_message)
        self.decoded_message = decrypted_message
        return decrypted_message


if __name__ == "__main__":
    daily_key = "Non_Ducor,_Duco"
    cipher = Cipher(daily_key, key_extension=100)
    
    # Test 1
    print("---------------------------------------------")
    message_to_send = daily_key[0]*len(daily_key)
    
    encrypted_message = cipher.encode(message_to_send, "Encoding")
    message_received = daily_key[-1]*len(daily_key)
    decrypted_message = cipher.decode(message_received, "Decoding")
    print("---------------------------------------------")
    
    # Test 2
    print("---------------------------------------------")
    message_to_send = "Who_was_your_favorite_actor_in_the_90s?"
    #message_to_send = "Who_is_your_favorite_actor?"
    encrypted_message = cipher.encode(message_to_send, "Encoding")
    message_received = "wiq|0fyb6x42gso!480$ypwz*%*v!)y;%#2e{@0"
    decrypted_message = cipher.decode(message_received, "Decoding")
    print("---------------------------------------------")
