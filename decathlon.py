import sys

from decathlon_entity import Decathlon


def main():
    # check enough cmd parameters
    if len(sys.argv) < 3:
        print('please set source or/and output file names')
        print('example:\n\tdecathlon.py <source file name> <output file name>')

        return

    # init source and output file names
    decathlon = Decathlon(sys.argv[1], sys.argv[2])

    # run distributing process
    decathlon.run_distributing()

    # create file for output data and store into it
    decathlon.store_to_json()

    print('work completed')


main()
