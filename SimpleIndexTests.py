import unittest

from io import StringIO

from SimpleIndex import SimpleIndex

class SimpleIndexTests(unittest.TestCase):
    
    def setUp(self):
        test_string_1 = "here is a test string\nNow another line is here"
        test_string_2 = "A test string needs repeats\nSo here is another"
        full_test_string = " ".join((test_string_1, test_string_2))
        
        with StringIO(full_test_string) as test_document:
            self.index = SimpleIndex(test_document)
            
    def test_find_first(self):
        self.assertEqual(self.index.find_first('here'), 0)
        self.assertEqual(self.index.find_first('string'), 4)
        self.assertEqual(self.index.find_first('not'), float('inf'))
    
    def test_find_last(self):
        self.assertEqual(self.index.find_last('here'), 16)
        self.assertEqual(self.index.find_last('string'), 12)
        self.assertEqual(self.index.find_last('not'), float('inf'))
    
    def test_find_next(self):
        ##TODO
        pass
    
    def test_find_previous(self):
        ##TODO
        pass
        
    def test_find_phrase(self):
        self.assertEqual(self.index.find_phrase('is a', -float('inf')), (1, 2))
        self.assertEqual(self.index.find_phrase('here where', -float('inf')),
                         (float('inf'), float('inf')))
        self.assertEqual(self.index.find_phrase('so here', 5), (15, 16))


if __name__ == '__main__':
    unittest.main()                         
                         
            
        
