"""
   Opens a CSV file, reads values, sets the value to negative if Debit.  
   Stores to file with fixed_ in name.
   Adjust the setting in config.py to test or run normal mode
   Status: complete
"""
import csv
import config

#open the input file
#open the output file
#read a line from the input file
#write the data to the output file

sourceFileDir = config.dataDirectory
runState = config.mode

def requestFileName():
    if runState == "Test":
        fileName = config.testFile
    else:
        fileName = input("Enter the file name (with .csv extension): ")
    return fileName

def openAndOutput(fileName):
    with open(sourceFileDir + fileName, 'r', encoding='utf-8') as infile,\
        open(sourceFileDir + "fixed_" + fileName, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile)
        for row in reader:
            print(row)
            if row[2] == "Debit":
                row[3] = str(-abs(float(row[3].strip('$,').replace(',', '' ))))
            outfile.write(','.join(row) + '\n')
            print(row)

def main():
    fileName = requestFileName()
    openAndOutput(fileName)

if __name__ == "__main__":
    main()