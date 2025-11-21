date = "12/7/2025"

def convertDateForMySQL(date):
    month, day, year = date.split("/")
    return f"{year}-{month.zfill(2)}-{day.zfill(2)}"

cdate = convertDateForMySQL(date)
print(cdate)