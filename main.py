import threading
from headertodict import *
from emails_loop import emails_loop
import chardet
import nerdvision



def main():
    # creating thread
    nerdvision.start( 'nv-RvlEKgPYhdrgmwhtBkKF' )
    emails_loop()





def print_square(num):
    """
    function to print square of given num
    """
    print("Square: {}".format(num * num))


if __name__ == "__main__":
    main()
