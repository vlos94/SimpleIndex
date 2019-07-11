import bisect

from collections import defaultdict

class IndexError(Exception):
    def __init__(self, error_msg):
        super(IndexError, self).__init__(error_msg)

class SimpleIndex:
    def __init__(self, document):
        """  

           Note: -float('inf') and float('inf')
                will represent the beginning and 
                end of the file, respectively.
        
           the document should be a file-like object
           
           Typically just an open file object but for 
           testing purposes, it might be desirable 
           to wrap a short test string
           in a StringIO object.
           
           
           The SimpleIndex object will not close the file
           object. A good usage that takes care
           of this would maybe would look like
           
           with open(<file_name>) as document:
               index = SimpleIndex(document) 
               
          TODO: Do something about encodings so
          the input could be ascii, unicode, etc"""
        
        self.index = defaultdict(list)
        self.document_length = 0
        self._process(document)

    def _process(self, document):
        """Build the index from the given document."""
        current_position = 0
        for line in document:
            terms = line.strip('\n\t ,.?!').split()
            position_range = range(current_position,
                                   current_position+len(terms))
            
            for term, position in zip(terms, position_range):
                processed_term = term.lower()
                self.index[processed_term].append(position)
            
            current_position += len(terms)
                
        self.document_length = current_position+1

    def find_first(self, term):
        """Give position of the first occurrence of term."""
       
        term = term.lower()
        if term not in self.index:
            return float('inf')
        
        return self.index[term][0]
        
    
    def find_last(self, term):
        """Return the position of the last occurrence of the term"""

        term = term.lower()
        if term not in self.index:
            return float('inf')
       
        return self.index[term][-1]


    def find_next(self, term, position):
        """Find the next occurrence of the term after the given position"""
        
        if position == -float('inf'):
            return self.find_first(term)
        
        elif position == float('inf'):
            return float('inf')
        
        
        term = term.lower()
        if term not in self.index:
            return float('inf')
       
        positions = self.index[term]
        
        ##sorted list --> use binary search
        next_position_index = bisect.bisect_right(positions, position)
       
        ##Handle the case of no next occurrence
        if next_position_index == len(positions):
            return float('inf')
       
        return positions[next_position_index]
       
    
    def find_previous(self, term, position):
        """Find most recent occurrence of term before given position"""
        if position == float('inf'):
            return self.find_last(term)
        
        elif position == -float('inf'):
            return -float('inf')
        
        term = term.lower()
        if term not in self.index:
            return -float('inf')
        
        positions = self.index[term]
        ##sorted list --> use binary search
        previous_position_index = bisect.bisect_left(positions, position)
        
        ##When the index returned is 0
        ##this may indicate no previous occurrence or it may not
        ##Additional condition checks required
        if previous_position_index == 0:
            if positions[previous_position_index] >= position:
                return -float('inf')
            else:
                return positions[previous_position_index]
        
        return positions[previous_position_index-1]
        
        
    def count_occurrences(self, term):
        """Find how many times a word occurs."""
        
        if term not in self.index:
            return 0

        return len(self.index[term])
       
    def find_phrase(self, phrase, start_position):
        """Find 1st occurrence of phrase starting after given position
        
           args: 
                 phrase: Pass phrase as string, preferably without uppercase
                 letters or end-punctuation as these will be lowered
                 and removed, respectively.
                  
                 start_position: start position
                 
           returns:
                Interval of positions as a tuple
                An interval (float('inf'), float('inf'))
                indicates the phrase was not found"""
        current_position = start_position
        phrase_terms = [term.lower() for term in phrase.strip('\t\n .,!?').split()]
        while True:
            ##left to right scan
            for i in range(len(phrase_terms)):
                term = phrase_terms[i]
                current_position = self.find_next(term, current_position)

                if current_position == float('inf'):
                    return (float('inf'), float('inf'))

            previous_position = current_position
            ##right to left scan
            for i in range(len(phrase_terms)-2, -1, -1):
                term = phrase_terms[i]

                previous_position = self.find_previous(term, 
                                                       previous_position)

            ##Check if the terms occurred sequentially    
            if current_position-previous_position == len(phrase_terms)-1:
                return (previous_position, current_position)
            ##If the terms didn't occur in sequence,
            ##restart the search where the last term
            ##of the phrase occurs
            current_position = previous_position


