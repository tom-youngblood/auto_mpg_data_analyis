# Import libraries for later use
import os
import csv
from collections import namedtuple
import logging
import requests
import argparse
from collections import defaultdict
import sys
import matplotlib.pyplot as plt

# Implement a class that represents the attributes that are available for each record in the dataset
class AutoMPG:
    """
    Description: 
    Initializes a car record from a dataset; makes objects of the class AutoMPG printable
    using __str__ and __repr__; makes objects of the class AutoMPG comparable using __eq__ 
    and __lt__; makes objects of the class AutoMPG hashable using __hash__.

    Arguments:
        make (str): The car's make.
        model (str): The car's model.
        year (int): The car's four-digit model year.
        mpg (float): The car's miles per gallon.

    Methods:
        __init__(self, make, model, year, mpg):
            Initializes an AutoMPG object with the attributes self, make, model, year, mpg.

        __repr__(self):
            Returns a standardized string representation of the AutoMPG object.

        __str__(self):
            Returns a string representation of the AutoMPG object by calling __repr__.

        __eq__(self, other):
            Compares two AutoMPG objects for equality.

        __lt__(self, other):
            Compares two AutoMPG objects for less than.

        __hash__(self):
            Returns a hash value based on the object's attributes (neccessary becasue of __eq__)
    """

    # Define __init__ and initialize specified variables: make, model, year, mpg
    def __init__(self, make, model, year, mpg):
        '''
        Description:
        Initializes an AutoMPG object with the attributes self, make, model, year, mpg.

        Arguments:
        make (str): The car's make.
        model (str): The car's model.
        year (int): The car's four-digit model year.
        mpg (float): The car's miles per gallon.

        Returns: None
        '''
        self.make = str(make)       # first token of "car name" field in dataset
        self.model = str(model)     # all other tokens in the "car name" field of the datset except the first
        self.year = int(year)       # four digit-year year that corresponds to the "model year" field of the dataset
        self.mpg = float(mpg)       # miles per gallon, corresponding to the mpg field of the dataset

        # Call the logger
        logger = logging.getLogger()
        logger.debug(f"AutoMPG Object Created: Make = {make}, Model = {model}, Year = {year}, MPG = {mpg} ")

        return None
    
    # Define __repr__
    def __repr__(self):
        '''
        Description:
        Returns a standardized string representation of the AutoMPG object.
        
        Arguments:
        self.
        
        Returns: 
        A repr string containing the car's make, model, year, and miles per gallon.
        '''
        return f"AutoMPG('{self.make}', '{self.model}', {self.year}, {self.mpg})"

    # Define __str__, call __repr__
    def __str__(self):
        '''
        Description:
        Returns a string representation of the AutoMPG object by calling __repr__.

        Arguments:
        self.

        Returns:
        A string representation of the AutoMPG object by calling __repr__.
        '''
        return repr(self)
    
    # Define __eq__; implement equality comparison between two AutoMPG objects
    def __eq__(self, other):
        '''
        Description:
        Compares two AutoMPG objects for equality.

        Arguments:
        self.
        other (AutoMPG): the object that self compares with

        Returns:
        bool: true if self == other, NotImplemented if self != other

        '''
        # Make sure objects compared are of the smae type
        if type(other) == type(self):
            # Compare the objects
            return (self.make, self.model, self.year, self.mpg) == (other.make, other.model, other.year, other.mpg)
        else:
            # If types are not comparable, return NotImplemented
            return NotImplemented

    # Define __lt__
    def __lt__(self, other):
        '''
        Description:
        Compares two AutoMPG objects for less than.

        Argumnts:
        self.
        other (AutoMPG): the object that self compares with.

        Returns:
        bool: true if self < other, NotImplemented if else
        '''
        # Make sure objects compared are of the same type
        if type(other) == type(self):
            # Compare the objects in order given
            return (self.make, self.model, self.year, self.mpg) < (other.make, other.model, other.year, other.mpg)
        else:
            # If types are not comparable, return NotImplemented
            return NotImplemented

    # Define __hash__ (neccesary because of __eq__ definition)
    def __hash__(self):
        '''
        Description:
        Returns a hash value based on the object's attributes (neccessary becasue of __eq__)

        Arguments:
        self

        Returns:
        Hash value based on the object's attributes (neccessary becasue of __eq__)
        '''
        # Since there are multiple values, I returned the tuple with the hash of all values
        return hash((self.make, self.model, self.year, self.mpg))

# Define AutoMPGData class with single attribute, 'data', which is a list of AutoMPG objects
class AutoMPGData:
    """
    Description:
    Loads and cleans the AutoMPG dataset, and initalizes an AutoMPGData object

    Attributes:
        data (list): A list of AutoMPG objects representing car records.

    Methods:
        __init__(self):
            Initializes an AutoMPGData object using a cleaned dataset.

        __iter__(self):
            Makes the AutoMPGData class iterable by returning an iterator over the data list.

        _load_data(self):
            Loads data from a cleaned file (auto-mpg.clean.txt).

        _clean_data(self):
            Reads the original data file (auto-mpg.data.txt) and converts tab characters to spaces.
            Cleans line by line to create a cleaned file (auto-mpg.clean.txt).
    """
    
    # Define __init__ constructor that takes no arguments, but calls the _load_data method
    def __init__(self):
        '''
        Description:
        Initializes an AutoMPGData object using a cleaned dataset.

        Arguments:
        self.

        Returns:
        None.
        '''
        # Initialize the data list as an instance variable (make the single 'data' attribute mentioned above)
        self.data = []
        # Call _load_data to fill the data attribute
        self._load_data()
        return None
    
    # Define __iter__ method to make class iterable; should return an iterator over the data list
    def __iter__(self):
        '''
        Description:
        Makes the AutoMPGData class iterable by returning an iterator over the data list.

        Arguments:
        self.

        Returns:
        An iterator over the data list.
        '''
        return iter(self.data)

    # Define _load_data method; load the cleaned file (auto-mpg.clean.txt) and instantiate objects and add them to the data attribute
    def _load_data(self):
        '''
        Description:
        Loads data from a cleaned file (auto-mpg.clean.txt).

        Arguments:
        self.

        Returns:
        None.
        '''
        # Call logger
        logger = logging.getLogger()
        logger.info("Starting to load data...")
        
        # Define the file paths
        cleanFilePath = "auto-mpg.clean.txt"
        dirtyFilePath = "auto-mpg.data.txt"

        # If dirty pathd doesn't exist, get data from the internet
        if not os.path.exists(dirtyFilePath):
            logger.info("Getting data")
            self._get_data()
            logger.info("Got data from url: https://archive.ics.uci.edu/ml/machine-learning-databases/auto-mpg/auto-mpg.data")

        # If clean path doesn't exist, clean the data
        if not os.path.exists(cleanFilePath):
            self._clean_data()
            logger.info(f"Cleaned {dirtyFilePath}, creating {cleanFilePath}")

        # If path exists, parse the data
        with open(cleanFilePath, newline='') as file:
            # Use skipinitialspace to ignore 'multiple sequential delimiters'; gives a list of the 9 columns
            # Use quotechar to handle strings with spaces
            reader = csv.reader(file, delimiter=' ', skipinitialspace=True, quotechar='"')

            # Use collections.namedtuple to defined 'Record' class; having nine attributes that correspond to the 9 fields in the same file
            Record = namedtuple('Record', ['mpg', 'cylinders', 'displacement', 'horsepower', 'weight', 'acceleration', 'modelYear', 'origin', 'carName'])

            # Use tuple packing/unpacking, assign the list returned by the csv module for a row to create a Record object
            for row in reader:
                record = Record(*row)

                # Split the car name into a list of strings
                carName = record.carName.split()

                # Create variables for make and model
                make = carName[0]               # The first string is the make
                model = ' '.join(carName[1:])   # All other strings in the list are the model

                # Create dictionary for correcting incorrect car makes
                correctMakes = {
                    "chevroelt": "chevrolet",
                    "chevy": "chevrolet",
                    "maxda": "mazda",
                    "mercedes-benz": "mercedes",
                    "toyouta": "toyota",
                    "vokswagen": "volkswagen",
                    "vw": "volkswagen"
                }

                # Correct the typos in makes
                if make in correctMakes:
                    logger.info(f"Cleaning typo: {make}")
                    make = correctMakes[make]
                    logger.info(f"Typo cleaned to: {make}")
            
                # Use the attributes of the Record object to pass the appropriate values to the constructor for AutoMPG.
                self.data.append(AutoMPG(make, model, record.modelYear, record.mpg))

        # End logger
        logger.info("Finished loading data")

        return None

    # Define _clean_data method to read original data file (auto-mpg.data.txt) line by line and use expandtabs method to convert TAB character to spaces
    def _clean_data(self):
        '''
        Description:
        Reads the original data file (auto-mpg.data.txt) and converts tab characters to spaces.
        Cleans line by line to create a cleaned file (auto-mpg.clean.txt).

        Arguments:
        self.

        Returns:
        None.
        '''

        # Call logger
        logger = logging.getLogger()
        logger.info("Cleaning data...")

        # Define an input and output path (was having trouble finding the files)
        inPath = 'auto-mpg.data.txt'
        outPath = 'auto-mpg.clean.txt'

        # Read auto-mpg.data.txt line by line, write auto-mpg.clean.txt with expanded tabs
        with open(inPath, 'r') as inFile, open(outPath, 'w') as outFile:
            # Read the line in the auto-mpg-data.txt, clean it using expand tabs, write the cleaned line to auto-mpg.clean.txt
            for line in inFile:
                cleanedLine = str(line).expandtabs()
                outFile.write(cleanedLine)

        # End logger
        logger.info("Finished Cleaning Data")
        return None
    
    # Define sort_by_default method (sort the data list in place by default order)
    def sort_by_default(self):
        '''
        Description:
        Sorts the data by default order.
        
        Arguments:
        self.
        
        Returns:
        None.
        '''
        logger = logging.getLogger()
        logger.info("sort_by_default function used")
        list.sort(self.data)
        return None
    
    # Define sort_by_year method for sorting the data by year
    def sort_by_year(self):
        '''
        Description:
        Sorts the data by year, make, model, then mpg. Creates keyword parameters to ensure proper sorting pattern.
        
        Arguments:
        self.

        Returns:
        None
        '''
        logger = logging.getLogger()
        logger.info("sort_by_year function used")
        # Creating a tuple holdin the keys for year, make, model, mpg
        list.sort(self.data, key=lambda x: (x.year, x.make, x.model, x.mpg))
        return None
    
    # Define sort_by_mpg method for sorting the data by MPG
    def sort_by_mpg(self):
        '''
        Description:
        Sorts the data by mpg, make, model, then year. Creates keyword parameters to ensure proper sorting pattern.
        
        Arguments:
        self.
        
        Returns:
        None.
        '''
        logger = logging.getLogger()
        logger.info("sort_by_mpg function used")
        # Creating a tuple holdin the keys for mpg, make, model, year
        list.sort(self.data, key=lambda x: (x.mpg, x.make, x.model, x.year))
        return None

    # Define _get_data method for getting information from the internet
    def _get_data(self):
        '''
        Description:
        Gets auto-mpg.data.txt from the internet if the dataset is not locally present.

        Arguments:
        self.

        Returns:
        None.
        '''
        # Get the logger
        logger = logging.getLogger()

        # Get data from internet
        logger.info("Requesting data from internet")
        dataFromInternet = requests.get("https://archive.ics.uci.edu/ml/machine-learning-databases/auto-mpg/auto-mpg.data")
        logger.info(f"Status of data request: {dataFromInternet.status_code}")

        if dataFromInternet:
            logger.info("Data successfully scraped")
            # Write the file new file if the data scraping was successful
            with open('auto-mpg.data.txt', 'w') as file:
                file.write(dataFromInternet.text)
                logger.info("Data from internet successfully written into file")
        # If data is unsuccessfully
        else:
            logger.critical("Data unsuccessfully scraped")
        
        return None

    # Define mpg_by_year
    def mpg_by_year(self):
        '''
        Description:
        Returns a dictionary where the keys are the years that are present in the data and the 
        values are the average MPG for all cars in that year using a defaultdict.

        Arguments:
        self.

        Returns:
        dictionary (defaultdict) where the keys are years that are present in the data set and the values 
        are the average MPG for all cars in that year.
        '''
        # Initialize default dict to store total mpg per year and total count of cars per year; initialize the dictionary to be returned
        yearData = defaultdict(lambda: {'totalMpg': 0, 'count': 0})
        avgMPGByYear = {}

        # Iterate through each objcet in the data
        for car in self.data:
            yearData[car.year]['totalMpg'] += car.mpg  # Add car's mpg to the total mpg for its year
            yearData[car.year]['count'] += 1           # Add 1 to the number of cars in the year

        # Calculate average MPG for each year
        for year, data in yearData.items():
            if data['count'] > 0:                                       # Avoid division by zero error
                avgMPGByYear[year] = data['totalMpg'] / data['count']   # Calculate average MPG and assign it to the avgMPGByYear dictionary

        # Return the dictionary
        return avgMPGByYear

    # Define mpg_by_make
    def mpg_by_make(self):
        '''
        Description:
        Returns a dictionary where the keys are the makes that are present in the data and the values are the 
        average MPG for all cars of that make.

        Arguments:
        self.

        Returns:
        dictionary where the keys are the makes that are present in the data and the values are the 
        average MPG for all cars of that make
        '''

        # Initialize default dict to store total mpg per make and total count of cars per make
        makeData = defaultdict(lambda: {'totalMpg': 0, 'count': 0})
        # Initialize Dictionary: keys = makes, values = avg MPG for all cars of the make
        avgMPGByMake = {}

        # Iterate through each object in the data
        for car in self.data:
            makeData[car.make]['totalMpg'] += car.mpg
            makeData[car.make]['count'] += 1
        
        # Calculate average MPG for each make
        for make, data in makeData.items():
            if data['count'] >0:
                avgMPGByMake[make] = data['totalMpg'] / data['count']
        
        # Return the dictionary
        return avgMPGByMake

# Define Main funciton
def main():
    '''
    Description:
    The main function of the program. Instantiates an object of the class AutoMPGData. Iterates
    over the object, printing each object.
    
    Attributes:
    None
    
    Arguments:
    None
    
    Methods:
    None

    Returns:
    None
    '''
    # Call logging function
    logger = loggingAutoMPG()
    logger.info("Main function started")

    # Create argparse object, add arguments
    parser = argparse.ArgumentParser(description='Analyzing the AutoMPG datset')
    parser.add_argument("command", help="command to execute (print, mpg_by_year, mpg_by_make)", metavar= "<command>")
    
    # Add sort argument; call the default sort order by default, set the variable to equal "<sort order>"
    parser.add_argument("-s", "--sort", help="sort the list before printing; options: <year>, <mpg>, <default>", default="default", metavar="<sort order>")

    # Add ofile argument; allows the user to specify the name of the file to which output should be written. If not specified; output sent to sys.stdout
    parser.add_argument("-o", "--ofile", help ="specify name of a file to which output should be written")
    
    # Add plot argument; allows the user to specify that graphical output using matplotlib should be created
    parser.add_argument("-p", "--plot", action="store_true", help="produce graphical output; usage: python3 autompg3.py <command> -p. Arguments: mpg_by_make, mpg_by_year")

    # Parse arguments
    args = parser.parse_args()

    # Create a variable to handle --ofile usage (whether or not it is used)
    outputDestination = open(args.ofile, "w", newline='') if args.ofile else sys.stdout

    # Create a CSV writer that writes to outputDestination
    writer = csv.writer(outputDestination)

    # Check for input == "print"
    if args.command.lower() == "print":
        # Instantiate an AutoMPGData object
        autoMPGDataObject = AutoMPGData()

        # Choose sorting option
        if args.sort == "year":
            logger.info("Sorting data by year...")
            autoMPGDataObject.sort_by_year()
            logger.info("Sorted data by year")
            
        elif args.sort == "mpg":
            logger.info("Sorting data by mpg...")
            autoMPGDataObject.sort_by_mpg()
            logger.info("Sorted data by mpg")

        elif args.sort == "default":
            logger.info("Sorting data by default order...")
            autoMPGDataObject.sort_by_default()
            logger.info("Sorted data by default order")

        else:
            logger.warning(f"Warning - Improper Usage. Usage: {parser.format_usage()}")
            logger.warning("Sorting by default...")
            autoMPGDataObject.sort_by_default()
            logger.warning("Sorted by default")

        # Create headers if -ofile called
        if writer:
            writer.writerow(['Make', 'Model','Year','MPG'])
            logger.info("Ofile called. Writing header")
        
        # Iterate over autoMPGDataObject, write each autompg object
        for car in autoMPGDataObject:
            if writer:
                writer.writerow([car.make, car.model,car.year, car.mpg])
            else:
                print(f"{car.make},{car.model},{car.year},{car.mpg}")
    
    elif args.command.lower() == "mpg_by_year":
        # Instantiate an AutoMPGData object
        autoMPGDataObject = AutoMPGData()
        data = autoMPGDataObject.mpg_by_year()

        # Output in CSV format
        if writer:
            writer.writerow(['Year', 'Average MPG'])  # Header

        # Write rows if -ofile used, print if not
        for year, mpg in sorted(data.items()):
            if writer:
                writer.writerow([year, mpg])
            else:
                print(f"{year},{mpg}")

        # Plotting
        if args.plot:
            
            # Sort data
            sortedData = dict(sorted(data.items()))

            # Get keys as years and values as mpg
            years = list(sortedData.keys())
            avgMpg = list(sortedData.values()) 

            # Plotting
            plt.bar(years, avgMpg)
            plt.title("MPG By Year")
            plt.xlabel("Year")
            plt.ylabel("Average MPG")
            plt.tight_layout()
            plt.show()


    elif args.command.lower() == "mpg_by_make":
        # Instantiate an AutoMPGData object
        autoMPGDataObject = AutoMPGData()
        data = autoMPGDataObject.mpg_by_make()
        
        # Output in CSV format
        if writer:
            writer.writerow(['Make', 'Average MPG'])  # Header

        # Write rows if -ofile used, print if not
        for make, mpg in sorted(data.items()):
            if writer:
                writer.writerow([make, mpg])
            else:
                print(f"{make},{mpg}")
            
        # Plotting
        if args.plot:
            
            # Sort data
            sortedData = dict(sorted(data.items()))

            # Get keys as model and values as mpg
            model = list(sortedData.keys())
            avgMpg = list(sortedData.values()) 

            # Plotting
            plt.bar(model, avgMpg)
            plt.title("MPG By Make")
            plt.xlabel("Make")
            plt.ylabel("Average MPG")
            plt.xticks(rotation=75)
            plt.tight_layout()
            plt.show()

    # If print was not inputted 
    else:
        logger.warning("Must use a command")
    
    logger.info("Main function ended")
    return None

# Define logging function
def loggingAutoMPG():
    '''
    Description:
    Creates logging functionality for the autompg2.py program.

    Arguments:
    None.

    Returns:
    logger: a logging object.
    '''

    # Retrieve the logger
    logger = logging.getLogger()

    # Set the initial level to info
    logger.setLevel(logging.DEBUG)

    # Log into autompg2.log at DEBUG level
    fh = logging.FileHandler('autompg3.log', 'w')   # Initializing the File Handler
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)

    # Log into the console at INFO level
    sh = logging.StreamHandler()                    # Initializing the Stream Handler
    sh.setLevel(logging.INFO)
    logger.addHandler(sh)

    return logger

# Call main if run from __main__
if __name__ == "__main__":

    # Call main
    main()
