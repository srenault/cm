import os
import argparse
import codecs
from ofxparse import OfxParser

def main():
    parser = argparse.ArgumentParser(description='Init stats db from ofx files.')

    parser.add_argument('directory', type=str, help='ofx directory')

    args = parser.parse_args()

    files = [f for f in os.listdir(args.directory) if os.path.isfile(os.path.join(args.directory, f))]

    filtered_ofx_files = list(filter(lambda file: os.path.splitext(file)[1] == '.ofx', files))

    for ofx_file in filtered_ofx_files:
        with codecs.open(args.directory + "/" + ofx_file) as fileobj:
            ofx = OfxParser.parse(fileobj)
            print(ofx.account.statement.transactions[0].amount)
            print(ofx.account.statement.transactions[0].date)

if __name__ == '__main__':
    main()
