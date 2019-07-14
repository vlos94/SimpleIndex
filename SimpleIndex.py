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
        self._prev_cache = dict()
        self._next_cache = defaultdict(lambda: 0)
    
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


    def find_next(self, term, current):
        """Find the next occurrence of the term after the given position current
           using a galloping search"""
        term = term.lower()
        
        if term not in self.index:
            return float('inf')
        
        positions = self.index[term]
        
        ##No next occurrence
        if positions[-1] <= current:
            return float('inf')
        
        if positions[0] > current:
            self._next_cache[term] = 0
            return positions[0]
        
        cached_index = self._next_cache[term]
        ##check if the cached index works as a place to start search
        if cached_index > 0 and positions[cached_index-1] <= current:
            low = cached_index
        else:
            low = 0
            
        jump = 1
        high = low + jump
        
        ##find a range to perform binary search on
        while high+1 < len(positions) and positions[high] <= current:
            jump *= 2
            low, high = high, low+jump
            
        if high > len(positions)-1:
            high = len(positions) - 1

        cached_index = bisect.bisect_right(positions, current,
                                           lo=low, hi=high)
                                          
        
        self._next_cache[term] = cached_index

        return positions[cached_index]
    
    
    def find_previous(self, term, current):
        """Find most recent occurrence of term before given position
           using a galloping search"""
        term = term.lower()
        if term not in self.index:
            return -float('inf')
        
        positions = self.index[term]
        
        ##no previous occurrremce
        if positions[0] >= current:
            return -float('inf')
        
        ##asking for previous with start position greater than
        ##last occurrence, so just return last position in list
        if positions[-1] < current:
            self._prev_cache[term] = len(positions)-1
            return positions[-1]
        
        ##unlike the find_next method, the default index value
        ##depends on list, so set it manually if its never been set
        try:
            cached_index = self._prev_cache[term]
        except KeyError:
            self._prev_cache[term] = len(positions)-1
            cached_index = len(positions)-1
            
        if (
            cached_index+1 < len(positions) and
            positions[cached_index+1] >= current
            ):
            high = cached_index+1
        else:
            high = len(positions)-1
            
        jump = 1
        low = high - jump
        
        while low >= 0 and positions[low] >= current:
            jump *= 2
            low, high = high-jump, low
            
        if low < 0:
            low = 0
            
        cached_index = -1 + bisect.bisect_left(positions, current, 
                                          lo=low, hi=high)
        
        self._prev_cache[term] = cached_index
        
        return positions[cached_index]
        
            
        
        
        
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


