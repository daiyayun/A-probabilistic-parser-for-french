from nltk.corpus import BracketParseCorpusReader
import nltk
from collections import defaultdict

# convert a rhs to a string
def toString(rhs):
    if len(rhs) == 1:
        # return (str(rhs[0]),)
        return str(rhs[0])
    elif len(rhs) == 2:
        # return (str(rhs[0]), str(rhs[1]))
        return str(rhs[0])+' '+str(rhs[1])

def PCFG(trees):
    """
    learn a probabilistic context-free Grammar from a binarized tree corpus.
    :return: lexicon, grammar, vocabulary, symbols
    :type lexicon: defaultdict{(word, (pos,)):probability} such that the sum of the probabilities 
        for all triples for a given word sums to 1.
    :type grammar: defaultdict{(prod.lhs(), prod.rhs()):probability}, 
        each term represents a production and its probability
    :type vocabulary: set of words
    :type symbols: set of tree nodes, except the leaves
    """ 
    # grammar
    grammar = defaultdict(float) 
    gcounts = defaultdict(int)
    # lexicon
    lexicon = defaultdict(float)
    lcounts = defaultdict(int)
    # symbols(non-terminals)
    symbols = set()
    
    for tree in trees:
        leaves = tree.leaves()
        for prod in tree.productions():
            symbols.add(str(prod.lhs()))
            if len(prod.rhs()) == 1 and prod.rhs()[0] in leaves:
                lcounts[prod.rhs()[0]] += 1
                lexicon[(prod.rhs()[0], str(prod.lhs()))] += 1
            else:
                gcounts[str(prod.lhs())] += 1
                grammar[(str(prod.lhs()), toString(prod.rhs()))] += 1
                
    # calculate probabilities
    for pair in lexicon:
        lexicon[pair] /= lcounts[pair[0]]
    for pair in grammar:
        grammar[pair] /= gcounts[pair[0]]
    return lexicon, grammar, set(lcounts.keys()), symbols
