import unittest

from io import StringIO

from SimpleIndex import SimpleIndex

class SimpleIndexTests(unittest.TestCase):
    
    def setUp(self):
        test_string_1 = "here is a test string\nNow another line is here"
        test_string_2 = "A test string needs repeats\nSo here is another string"
        full_test_string = " ".join((test_string_1, test_string_2))
        
        with StringIO(full_test_string) as test_document:
            self.index = SimpleIndex(test_document)
            
    def test_find_first(self):
        self.assertEqual(self.index.find_first('here'), 0)
        self.assertEqual(self.index.find_first('string'), 4)
        self.assertEqual(self.index.find_first('not'), float('inf'))
    
    def test_find_last(self):
        self.assertEqual(self.index.find_last('here'), 16)
        self.assertEqual(self.index.find_last('string'), 19)
        self.assertEqual(self.index.find_last('not'), float('inf'))

    def test_find_next(self):
        self.assertEqual(self.index.find_next('here', -float('inf')), 0)
        self.assertEqual(self.index.find_next('here', 0), 9)
        self.assertEqual(self.index.find_next('here', 9), 16)
        self.assertEqual(self.index.find_next('string', 4), 12)
        self.assertEqual(self.index.find_next('string', 12), 19)
        self.assertEqual(self.index.find_next('string', float('inf')), float('inf'))
    
    def test_find_previous(self):
        ##TODO
        self.assertEqual(self.index.find_previous('is', 12), 8)
        self.assertEqual(self.index.find_previous('here', 9), 0)
        self.assertEqual(self.index.find_previous('here', 16), 9)
        self.assertEqual(self.index.find_previous('string', 12), 4)
        self.assertEqual(self.index.find_previous('string', 19), 12)
        self.assertEqual(self.index.find_previous('string', float('inf')), 19)
        
    def test_find_phrase(self):
        self.assertEqual(self.index.find_phrase('is a', -float('inf')), (1, 2))
        self.assertEqual(self.index.find_phrase('here where', -float('inf')),
                         (float('inf'), float('inf')))
        self.assertEqual(self.index.find_phrase('so here', 5), (15, 16))


if __name__ == '__main__':
    unittest.main()                         
                         
            
        
