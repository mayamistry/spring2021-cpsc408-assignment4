import sys
import assignment4 as a

def run():
    #command line arguments

    file = sys.argv[1]
    records  = int(sys.argv[2])

    a.genData(file, records)
    a.importData(file)

if __name__ == '__main__':
    run()

