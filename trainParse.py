import nltk
from collections import defaultdict
import numpy as np
import pickle
#from nltk.corpus import BracketParseCorpusReader
import time

from cyk import CYK
# from cyk import CYKSolver
from pcfg import PCFG
from oov import OOV

import sys
logs = sys.stderr

if __name__ == "__main__":
    try:
        _, trainfilename, embedfilename = sys.argv
    except:
        print('usage: trainParse.py <train-file> <embed-file>\n', logs)
        sys.exit(1)

    # load the train file to trees
    trees = []
    f = open(trainfilename, 'r')
    for line in f:
        trees.append(nltk.Tree.fromstring(line))

    # preprocss the tree forms: ignore functional labels and binarize to CNF
    for tree in trees:
        # ignore_func_labels(tree)
        tree.chomsky_normal_form(horzMarkov=2)
        # tree.chomsky_normal_form()

    # learn PCFG
    lexicon, grammar, vocabulary, symbols = PCFG(trees)
    # print(grammar)

    # for OOV
    oovwords = OOV(embedfilename, vocabulary)   

    # parse new sentences using CYK based on learned PCFG
    # parser = CYKSolver(lexicon, grammar, vocabulary, symbols, oovwords)

    # i = 0
    for line in sys.stdin:
        # print('start parse')
        # print(line)
        # start = time.time()
        # if line == '\n': continue
        # cyksolver = CYK(line.split(), lexicon, grammar, vocabulary, symbols, embedfilename)
        # i += 1
        # if i < 20: continue
        # if i > 3: break
        # parsedtree = parser.compute(line.split())
        parsedtree = CYK(line.split(), lexicon, grammar, vocabulary, symbols, oovwords)
        if parsedtree == None: 
            print('(None)')
            continue
        parsedtree.un_chomsky_normal_form()
        # end = time.time()
        # print(end-start)
        # print('bon')
        print('( '+parsedtree._pformat_flat(nodesep='', parens='()', quotes=False)+')')


