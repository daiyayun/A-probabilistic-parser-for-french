import nltk
from collections import defaultdict
from oov import OOV

# CYK algorithm
def addUnary(begin, end, back, score, symbols, grammar):
    # print('add unary')
    for A in symbols:
        for B in symbols:
            if (A, B) in grammar:
                prob = grammar[(A,B)] * score[(begin,end,B)]
                if prob > score[(begin,end,A)]:
                        score[(begin, end, A)] = prob
                        back[(begin, end, A)] = (B,)
                        # print('score:',begin,end,A,prob,'back',B)
                        
def backtrack(triple, back):
    low = triple[0]
    high = triple[1]
    label = triple[2]
    if (low,high,label) not in back:
        # print(label)
        return label
    else:
        branches = back[(low,high,label)]
        if len(branches) == 1:
            return nltk.Tree(label, [backtrack((low,high,branches[0]), back)])
        elif len(branches) == 3:
            (split, left, right) = branches
            return nltk.Tree(label, [backtrack((low,split,left), back), backtrack((split,high,right),back)])
    
def build_tree(back, n):
    if (0,n,'SENT') not in back: return None
    return backtrack((0,n,'SENT'),back)

def CYK(sentence, lexicon, grammar, vocabulary, symbols, oovwords):
    score = defaultdict(float)
    back = {}
    n = len(sentence)
    
    # print('words:')
    for ii in range(0,n):
        begin = ii
        end = ii+1
        original_word = sentence[begin]
        word = original_word
        if original_word not in vocabulary:
            # return None
            word = oovwords.replace(original_word)
            # print(word, original_word)
        for A in symbols:           
            if (word, A) in lexicon:
                score[(begin,end,A)] = lexicon[(word, A)]
                # print(word, A, lexicon[(word, A)])
                back[(begin,end,A)] = (original_word,)
                # print('score:',begin,end,A,score[(begin,end,A)],'back:',original_word,word)
        addUnary(begin, end, back, score, symbols, grammar)
    
    for span in range(n+1):
        for begin in range(0,n-span+1):
                end = begin + span
                for split in range(begin+1,end):
                    for (A, X) in grammar:
                        rhs = X.split()
                        #print(A, rhs, grammar[(A,rhs)])
                        if len(rhs) == 2:
                            B = rhs[0]
                            C = rhs[1]
                            #compute probability of tree rooted at A at begin,end if left, right are B and C resp.
                            prob = score[(begin,split,B)] * score[(split, end, C)] * grammar[(A, X)]

                            if prob > score[(begin, end,  A)]:
                                score[(begin, end, A)] = prob
                                back[(begin, end, A)] = (split, B, C)
                                # print('score:',begin,end,A,prob,'back',B)
                                
                addUnary(begin, end, back, score, symbols, grammar)
    # print('start building tree')
    return build_tree(back, n)
    