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


def convertDateForMySQL(date):
    """ Convert given date from MM/DD/YYYY to YYYY-MM-DD format.
        No error checking done here.
    """
    month, day, year = date.split("/")
    return f"{year}-{month.zfill(2)}-{day.zfill(2)}"


def requestFileName():
    """If the filemode is Test then use the test file listed in config.py
       Otherwise request the file name from the user
       No error checking is done here.
    """
    if runState == "Test":
        fileName = config.testFile
    else:
        fileName = input("Enter the file name (with .csv extension): ")
    return fileName


def openAndOutput(fileName):
    """  Opens provided input csv and creates output file with 'fixed_prefix
         Expects csv to have Date, Description, Debit/Credit, Amount in that order
         Sets Amount to negative and removes the Debit/Credit field
         Removes $ and commas from Amount if they exist
         Adds a Status column with value 'Cleared'
         Dates are converted to YYYY-MM-DD format
         This should be used to convert the CSV for import into the database
         No error checking is done here.
    """
    with open(sourceFileDir + fileName, 'r', encoding='utf-8') as infile,\
        open(sourceFileDir + "fixed_" + fileName, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile)
        next(reader)  # Skip header row
        outfile.write('Date,Description,Amount,Status\n')  # Write header row
        for row in reader:
            #print(row)
            row[0] = convertDateForMySQL(row[0])  # Convert date to MySQL format
            if row[2] == "Debit":
                row[3] = str(-abs(float(row[3].strip('$,').replace(',', '' ))))
            row[2] = row[3]  # Move adjusted amount to Amount column
            row[3] = 'Cleared'  # Clear Status column
            outfile.write(','.join(row) + '\n')
            #print(row)


def main():
    fileName = requestFileName()
    openAndOutput(fileName)

if __name__ == "__main__":
    main()