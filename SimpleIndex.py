import bisect

from collections import defaultdict

class IndexError(Exception):
    def __init__(self, msg):
        super(IndexError, self).__init__(msg)

class SimpleIndex:
    def __init__(self, document):
        """For now just assume the document is a string.
           TODO: make it so that the document is a file"""
        
        self.index = defaultdict(list)
        self.document_length = 0
        self._process(document)

    def _process(self, document):
        """Build the index from the given document."""

        terms = document.split()
        for term, position in zip(terms, range(len(terms))):
            processed_term = term.strip('\n\t ,.?!').lower()
            self.index[term].append(position)
            
            self.document_length += 1

    def find_first(self, term):
        """Give position of the first occurrence of term."""
       
        term = term.lower()
        if term not in self.index:
            error_msg = 'term {} not found in document'.format(term)
            raise IndexError(error_msg)
        
        return self.index[term][0]
        
    
    def find_last(self, term):
        """Return the position of the last occurrence of the term"""

        term = term.lower()
        if term not in self.index:
            error_msg = 'term {} not found in document'.format(term)
            raise IndexError(error_msg)
       
        return self.index[term][-1]


    def find_next(self, term, position):
        """Find the next occurrence of the term after the given position"""
       
        term = term.lower()
        if term not in self.index:
            error_msg = 'term {} not found in document'.format(term)
            raise IndexError(error_msg)
       
        positions = self.index[term]
        ##the list of positions is sorted, so we can
        ##use a binary search
        next_position = bisect.bisect_right(positions, position)
       
        ##Handle the case of no next occurrence
        if next_position_index == len(positions):
            return float('inf')
       
        return positions[next_position_index]
       
    
    def find_previous(self, term, position):
        """Find most recent occurrence of term before given position"""
        
        term = term.lower()
        if term not in self.index:
            error_msg = 'term {} not found in document'.format(term)
            raise IndexError(error_msg)
        
        positions = self.index[position]
        ##sorted list --> use binary search
        previous_position_index = bisect.bisect_left(positions, position)
        
        ##catch the case of no previous occurrence
        ##return -float('inf') to indicate this
        if previous_position_index == 0:
            return -float('inf')
        
        return positions[previous_position_index-1]
        
        
    def count_occurrences(self, term):
        """Find how many times a word occurs."""
        
        if term not in self.index:
            return 0

        return len(self.index[term])
       
    def find_phrase(self, phrase_terms, position):
        """TODO: this method will find first occurrence of
           phrase starting after given position"""
        pass
        
           
   
    
