import unittest
from loadfile import DataList

class Test(unittest.TestCase):
    
    def test_corrupted_file(self):
        ftype=DataList("Test/Error/NOTHING.csv").get_type()
        self.assertEqual(ftype,0,"Missing file didn't return 0")
        ftype=DataList("Test/Error/error_letter.csv").get_type()
        self.assertEqual(ftype,0,"Letters in file didn't return 0")
        ftype=DataList("Test/Error/error_emptycell.csv").get_type()
        self.assertEqual(ftype,0,"Empty cell in file didn't return 0")
        ftype=DataList("Test/Error/error_missingline.csv").get_type()
        self.assertEqual(ftype,0,"Missing line in file didn't return 0")
        ftype=DataList("Test/Error/error_emptyfile.csv").get_type()
        self.assertEqual(ftype,0,"Empty file didn't return 0")
        ftype=DataList("Test/Error/error_extracell.csv").get_type()
        self.assertEqual(ftype,0,"Extra cell didn't return 0")
        
    def test_datavalues(self):
        testdata=DataList("Test/Values/test_data.csv")
        ftype=testdata.get_type()
        self.assertNotEqual(ftype,0,"Cannot test values with corrupted in file")
        self.assertEqual(testdata.get_avg(),10,"Wrong total average")
        self.assertEqual(testdata.get_min(),-100,"Wrong total minimum")
        self.assertEqual(testdata.get_max(),100,"Wrong total maximum")
        self.assertEqual(testdata.get_datalist(1).get_avg(),0,"Wrong average in first graph")
        
        
if __name__ == '__main__':
    unittest.main()
