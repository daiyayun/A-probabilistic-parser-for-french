from sklearn.model_selection import train_test_split

import sys
logs = sys.stderr

"""
split a dataset into 3 parts: train(80%), dev(10%), test(10%)
"""

if __name__ == "__main__":
    try:
        _, filename = sys.argv
    except:
        print('usage: splitFile.py filename\n', logs)
        sys.exit(1)

    f = open(filename, 'r')
    lines = []
    for line in f:
        lines.append(line)

    train, test = train_test_split(lines, test_size=0.2)
    dev, test = train_test_split(test, test_size=0.5)

    f1 = open('train.txt', 'w')
    for line in train:
        f1.write(line)
    f1.close()

    f2 = open('dev.txt', 'w')
    for line in dev:
        f2.write(line)
    f2.close()

    f3 = open('test.txt', 'w')
    for line in test:
        f3.write(line)
    f3.close()
    

    