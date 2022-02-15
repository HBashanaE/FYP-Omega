import unittest
import preprocess

class TestPreprocessing(unittest.TestCase):

    def test1(self):
        self.assertEqual(preprocess.preprocess("යසිත්"), "යසිත්", "Should be යසිත්")

    def test2(self):
        self.assertEqual(preprocess.preprocess("යසිත්අ"), "යසිත්", "Should be යසිත්")

    def test3(self):
        self.assertEqual(preprocess.preprocess("යසිත්්"), "යසිත්", "Should be යසිත්")

    def test4(self):
        self.assertEqual(preprocess.preprocess("යසිිිිත්"), "යසිත්", "Should be යසිත්")

    def test5(self):
        self.assertEqual(preprocess.preprocess("යසිිත්"), "යසිත්", "Should be යසිත්")

    def test6(self):
        self.assertEqual(preprocess.preprocess("යිසිත්"), "යිසිත්", "Should be යිසිත්")

    def test7(self):
        self.assertEqual(preprocess.preprocess("යසිත්ි"), "යසිත්", "Should be යසිත්")

    def test8(self):
        self.assertEqual(preprocess.preprocess("ය‍ෙසිත්"), "යෙසිත්", "Should be ‍යෙසිත්")

    def test9(self):
        self.assertEqual(preprocess.preprocess("යසි‍ෙත්"), "යසිත්", "Should be යසිත්")

    def test10(self):
        self.assertEqual(preprocess.preprocess("යසිත්‍ෙ"), "යසිත්", "Should be යසිත්")


if __name__ == '__main__':
    unittest.main()
