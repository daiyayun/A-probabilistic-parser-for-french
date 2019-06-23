import nltk
import sys
logs = sys.stderr

"""
extract raw tokens from bracketed trees.
"""

if __name__ == "__main__":
    try:
        _, filename, outputname = sys.argv
    except:
        print('usage: extractRaw.py filename outputname\n', logs)
        sys.exit(1)

    f = open(filename, 'r')
    o = open(outputname, 'w')
    for line in f:
        tree = nltk.Tree.fromstring(line)
        tokens = ' '.join(tree.leaves())
        o.write(tokens+'\n')
    o.close()

