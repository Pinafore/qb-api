
from database import QuizBowl

if __name__ == "__main__":
    buzzes = QuizBowl.get_buzzes()
    with open('data/buzzes.csv', 'w') as f:
        for ii in sorted(buzzes):
            val = buzzes[ii]
            print("%i\t%i\t%i\t%s" % (ii[0], ii[1], val[0], val[1]), file=f)
