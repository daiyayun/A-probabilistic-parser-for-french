import nltk
import sys
logs = sys.stderr

"""
Ignore functional labels in a treebank.
"""

# a function that deal with functional labels
def ignore_func_labels(tree):
    if type(tree) == nltk.Tree:
        label = tree.label()
        if '-' in label:
            indice = label.index('-')
            tree.set_label(label[:indice])
        for subtree in tree:
            ignore_func_labels(subtree)

if __name__ == "__main__":
    try:
        _, filename, outputname = sys.argv
    except:
        print('usage: ignoreFunc.py filename outputname\n', logs)
        sys.exit(1)

    f = open(filename, 'r')
    o = open(outputname, 'w')
    for line in f:
        tree = nltk.Tree.fromstring(line)
        ignore_func_labels(tree)
        o.write(tree._pformat_flat(nodesep='', parens='()', quotes=False)+'\n')
    o.close()
