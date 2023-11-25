# auto_mpg_data_analyis
This project involves a detailed analysis of the Auto MPG dataset. It is implemented in Python and uses various libraries for data processing, statistical analysis, and visualization. The main functionality includes sorting the dataset based on different attributes, performing basic statistical analyses, and visualizing various characteristics of the data.

## Features
### Users can invoke command line arguments to control
Data Sorting: clean the dataset and sort it by MPG, car make, or year
Statistical Analysis: statistical analysis such as average MPG
Data Visualisation: visualisations like MPG distributions over years

## Prerequisites
Python3 
matplotlib

## Files
autompg3.py: main file outlining the program's functionality
autompg3.log: logging for main file
test_autompg3.py: testing for main file
auto-mpg.data.txt: original autompg data file (is downloaded from internet by program if not present)
auto-mpg.clean.txt: mpg data file that is cleaned in the process of the program
test.txt: Example usage of -ofile to redirect output to outfile

## Installation
### Clone the repository
git clone https://github.com/tom-youngblood/auto_mpg_data_analysis.git
### Navigate to the project directory (replace options with desired commands)
python autompg3.py [options]

## Usage

### Command Requirement
The program requires usage of command to run properly; commands:

print: print text output to standard out
-plot: produce a plot (mpg_by_make, or mpg_by_year)

Only allows for use of one command at a time

#### Print
print: Prints a the output to stdout. If optional argument -ofile is used, output will be redirected to specified filename
#### Ofile
-ofile: redirect text output to desired file

#### Plot
-plot: rovides matplotlib representation
##### Plot Options
mpg_by_make
mpg_by_year

## Example command line input
python3 autompg3.py -s year print
python3 autompg3.py -s make -o example_file.txt print
python3 autompg3.py -p mpg_by_make
python3 autompg3.py -p mpg_by_year

## Contact Me
Email: tomporteryoungblood@gmail.com
Phone: 310-405-4100