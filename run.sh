# convert the functional labels into non-func ones in SEQUOIA treebank
python ignoreFunc.py sequoia-corpus+fct.mrg_strict.txt sequoia.txt
echo "functional labels treated."
# split the treebank into 3 parts: train.txt, dev.txt, test.txt
python splitFile.py sequoia.txt
echo "file splited into 3 parts."
# the following commands consists of two parts: a and b. 
# the part a is to parse sentences from standard input;
# the part b is to obtain the raw tokens from the evaluation dataset(test set) 
#                   and then parse them for evaluation purpose.

# a.
# train a PCFG on train.txt and use CYK to parse sentences from standard input
echo "Please enter your sentences to parse. To stop inputting, type '^D'."
python trainParse.py train.txt polyglot-fr.pkl

# b.
# for evaluation
# python extractRaw.py test.txt evaluation_data.raw_tokens
# cat evaluation_data.raw_tokens | python trainParse.py train.txt polyglot-fr.pkl > evaluation_data.parser_output
