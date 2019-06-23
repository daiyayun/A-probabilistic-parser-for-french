import numpy as np
import pickle

class OOV:
    """
    a class that deals with out-of-vocabulary words.
    """
    def __init__(self, path_to_embed, vocabulary):
        """
        :params: path_to_embed, vocabulary
        :type path_to_embed: str
        :type vocabulary: set
        """
        self.words, self.embeddings = pickle.load(open(path_to_embed, 'rb'), encoding='bytes')
        self.word_id = {w:i for (i, w) in enumerate(self.words)}
        self.id_word = dict(enumerate(self.words))
        # the vocabulary on which we have trained a pcfg
        self.trainVocab = list(vocabulary)
        # intersection of vocabulary and embedded words
        self.interVocab = list(vocabulary.intersection(set(self.words)))
        self.interEmbeddings = np.array([self.embeddings[self.word_id[w]] for w in self.interVocab])

    def LevenshteinDist(self, s, t):
        """
        calculate the Levenshtein Distance between two strings
        """
        rows = len(s)+1
        cols = len(t)+1
        dist = [[0 for x in range(cols)] for x in range(rows)]
        # source prefixes can be transformed into empty strings 
        # by deletions:
        for i in range(1, rows):
            dist[i][0] = i
        # target prefixes can be created from an empty source string
        # by inserting the characters
        for i in range(1, cols):
            dist[0][i] = i
            
        for col in range(1, cols):
            for row in range(1, rows):
                if s[row-1] == t[col-1]:
                    cost = 0
                else:
                    cost = 1
                dist[row][col] = min(dist[row-1][col] + 1,      # deletion
                                    dist[row][col-1] + 1,      # insertion
                                    dist[row-1][col-1] + cost) # substitution
        return dist[row][col]

    def replace(self, word): 
        """
        find the most similar word to a given word in the vocabulary
        """
        if word in self.words:
            # Embedding Distances
            e = self.embeddings[self.word_id[word]]
            distances = (((self.interEmbeddings - e) ** 2).sum(axis=1) ** 0.5)
            EM_index = np.argmin(distances)
            return self.interVocab[EM_index]
        else:
            # Levenshtein Distances
            LDs = np.array([self.LevenshteinDist(word, v) for v in self.trainVocab])
            LD_index = np.argmin(LDs)
            return self.trainVocab[LD_index]
            
