The first step is to convert the functional labels into non-func ones in SEQUOIA treebank using:
python ignoreFunc.py sequoia-corpus+fct.mrg_strict.txt sequoia.txt
The first argument is the path to the original file and the second argument is the path to store output.

The second step is then split the SEQUOIA treebank into 3 parts: train.txt, dev.txt, test.txt.
For this, we execute the command: python splitFile.py sequoia-corpus+fct.mrg_strict.txt
The argument specifies the path to the file to split.

Then if we want to test the PCFG based CYK parser on standard input, we execute the command like this:
python trainParse.py train.txt polyglot-fr.pkl
The first argument is the path to training corpus and the second is the path to word embeddings.

If we want to evaluate the parser on an evaluation dataset like test.txt, we can execute the following commands:
python extractRaw.py test.txt evaluation_data.raw_tokens
cat evaluation_data.raw_tokens | python trainParse.py train.txt polyglot-fr.pkl > evaluation_data.parser_output
The first command is to extract the raw tokens from the bracketed strings in dataset 'test.txt'. 
The second then reads the tokens and stores the output results in the file 'evaluation_data.parser_output'.
Thus, we can compare the parsed results 'evaluation_data.parser_output' with the original dataset 'test.txt' using evalb program.