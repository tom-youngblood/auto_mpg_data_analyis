import unittest
from autompg3 import AutoMPG, AutoMPGData

# Define test_autompg class for testing the AutoMPG function
class test_AutoMPG(unittest.TestCase):
    """
    Description:
    Uses unittest to test the core functionality of the AutoMPG class.

    Arguments:
    None

    Methods:
        test_init(self):
            Tests the initialization of an AutoMPG object.
        
        test_repr(self):
            Tests the __repr__ method of AutoMPG.
        
        test_str(self):
            Tests the __str__ method of AutoMPG.
        
        test_eq(self):
            Tests the __eq__ method of AutoMPG.
        
        test_lt(self):
            Tests the __lt__ method of AutoMPG.
        
        test_hash(self):
            Tests the __hash__ method of AutoMPG.
    """


    # Create test for init constructor
    def test_init(self):
        '''
        Description:
        Tests the initialization of an AutoMPG object

        Arguments:
        self

        Returns:
        None
        '''
        # Create object 
        car1 = AutoMPG("Dodge", "Dart", 1990, 20)
        # Test for types
        self.assertEqual((type(car1.make), type(car1.model), type(car1.year), type(car1.mpg)),
                         (str, str, int, float)
                         )
        # Test that attributes are set correctly
        self.assertEqual((car1.make, car1.model, car1.year, car1.mpg),
                         ("Dodge", "Dart", 1990, 20)
                        )
    
    # Create test for repr function
    def test_repr(self):
        '''
        Description:
        Tests the __repr__ method of AutoMPG

        Arguments:
        self

        Returns:
        None
        '''
        # Create object
        car1 = AutoMPG("Dodge", "Dart", 1990, 20)
        # Test repr output
        self.assertEqual(repr(car1),
                         "AutoMPG('Dodge', 'Dart', 1990, 20.0)"
                         )

    # Create test for str function
    def test_str(self):
        '''
        Description:
        Tests the __str__ method of AutoMPG

        Arguments:
        self

        Returns:
        None
        '''
        # Create object
        car1 = AutoMPG("Dodge", "Dart", 1990, 20)
        # Test str output
        self.assertEqual(str(car1),
                         "AutoMPG('Dodge', 'Dart', 1990, 20.0)"
                         )
    
    # Create test for eq function
    def test_eq(self):
        '''
        Description:
        Tests the __eq__ method of AutoMPG

        Arguments:
        self

        Returns:
        None
        '''
        # Create objects
        carEqual1 = AutoMPG("Dodge", "Dart", 1990, 20)
        carEqual2 = AutoMPG("Dodge", "Dart", 1990, 20)
        carUnequal1 = AutoMPG("Toyota", "Camry", 1992, 25)
        # Test eq output
        self.assertAlmostEqual(carEqual1 == carEqual2, True)
        self.assertAlmostEqual(carEqual1 == carUnequal1, False)
    
    # Create test for lt function
    def test_lt(self):
        '''
        Description:
        Tests the __lt__ method of AutoMPG

        Arguments:
        self

        Returns:
        None
        '''
        # Create objects
        car1 = AutoMPG("Dodge", "Dart", 1990, 20)
        carLT1 = AutoMPG("AMC", "Rebel", 1995, 25)
        carLT2 = AutoMPG("Dodge", "Dart", 1990, 19)
        carGT1 = AutoMPG("Ford", "Torino", 1990, 20)
        carGT2 = AutoMPG("Dodge", "Dart", 1990, 22)
        # Test lt output
        self.assertTrue(carLT1 < car1)
        self.assertTrue(carLT2 < car1)
        self.assertTrue(car1 < carGT1)
        self.assertTrue(car1 < carGT2)
        self.assertFalse(car1 > carGT2)

    # Create test for hash function
    def test_hash(self):
        '''
        Description:
        Tests the __hash__ method of AutoMPG

        Arguments:
        self

        Returns:
        None
        '''
        # Create object
        car1 = AutoMPG("Dodge", "Dart", 1990, 20)
        # Test hash output
        self.assertEqual(hash(car1), hash(AutoMPG('Dodge', 'Dart', 1990, 20.0)))

class test_AutoMPGData(unittest.TestCase):
    """
    Description:
    Tests the core functionality of the AutoMPGData class.

    Methods:
        test_init(self):
            Tests the initialization of an AutoMPGData object.
        
        test_iter(self):
            Tests the __iter__ method of AutoMPGData.
        
        test__load_data(self):
            Tests the _load_data method of AutoMPGData.
        
        test__clean_data(self):
            Tests the _clean_data method of AutoMPGData.
    """

    # Create test for init
    def test_init(self):
        '''
        Description:
        Tests the initialization of an AutoMPGData object.
        
        Arguments:
        self.
        
        Returns:
        None.'''
        # Create object 
        autoMPGDataTest = AutoMPGData()
        # Test if 'data' is not empty in autoMPGDataTest
        self.assertIsNotNone(autoMPGDataTest.data)
        self.assertFalse(len(autoMPGDataTest.data) == 0)
    
    # Create test for iter
    def test_iter(self):
        '''
        Description:
        Tests the __iter__ method of AutoMPGData.
        
        Arguments:
        self.
        
        Returns:
        None.'''
        # Create object
        autoMPGDataTest = AutoMPGData()
        # Use hasattr to ensure object has attribute __iter__ 
        self.assertTrue(hasattr(autoMPGDataTest, "__iter__"))
    
    # Create test for _load_data
    def test__load_data(self):
        '''
        Description:
        Tests the _load_data method of AutoMPGData.
        
        Arguments:
        self.
        
        Returns:
        None.'''
        # Create object
        autoMPGDataTest = AutoMPGData()
        # Test if the output lines up with auto-mpg.data.txt
        sampleDataPoint = autoMPGDataTest.data[1]
        self.assertEqual(sampleDataPoint.make, "buick")
    
    # Create test for _clean_data
    def test__clean_data(self):
        '''
        Description:
        Tests the _clean_data method of AutoMPGData.
        
        Arguments:
        self.
        
        Returns:
        None.'''
        # Test if there are any tabs in the lines of the data
        with open('auto-mpg.clean.txt', 'r') as file:
            lines = file.readlines
            for line in file:
                self.assertNotIn('\t', line)
    
# Call testing program if not imported
if __name__ == "__main__":
    unittest.main()