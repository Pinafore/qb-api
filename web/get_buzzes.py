
from database import *

if __name__ == "__main__":
    buzzes = get_buzzes()
    for ii in sorted(buzzes):
        val = buzzes[ii]
        print("%i\t%i\t%i\t%s" % (ii[0], ii[1], val[0], val[1]))
