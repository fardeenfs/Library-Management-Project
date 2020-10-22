import mysql.connector as datasrc
import csv
import datetime
from prettytable import PrettyTable


dbcon = datasrc.connect(host='localhost',
                        user='root',
                        password='root',
                        database='library_management')

mycursor = dbcon.cursor()

def new_borrowal():
    mycursor.execute('SELECT * from borrower_management;')
    recs = mycursor.fetchall()
    x = len(recs)
    lastbid = int(recs[x - 1][0]) + 1
    try:
        a = int(input("Enter BookID : "))
        b = input("Enter Student ID :")
        c = ''
        for rec in recs:
            if rec[2] == b:
                c = rec[3]
        if c == '':
            c = input("Looks Like This Student Is New! Enter Student's First Name : ")
        d = input("Enter the date of borrowal in YYYY-MM-DD (Leave Empty For Today):")
        if d == '':
            d = datetime.datetime.today().strftime('%Y-%m-%d')
        e = (datetime.datetime.strptime(d, '%Y-%m-%d') + datetime.timedelta(days=7)).strftime('%Y-%m-%d')
        mycursor.execute(
            "insert into borrower_management(BID,BookID,StudentID,StudentFirstName,Borrow_Date,Compulsory_Return_Date,Book_Returned) values(%s,%s,%s,%s,%s,%s,%s);",
            (lastbid, a, b, c, d, e, 'N'))
        dbcon.commit()
        csvall()
    except ValueError:
        print("Please Enter An Appropriate Value!")
        new_borrowal()

    New_Entry = input("Do you want to add another borrowal record? (Y for yes/ Any other key to exit) : ")
    if New_Entry == "Y":
        new_borrowal()
        



def return_book():
    try:
        bid = input("Enter Borrowal ID (Leave Blank If Not Known) : ")
        if bid != '':
            mycursor.execute(
                "SELECT BID,BookID,StudentID,StudentFirstName,Borrow_Date,Compulsory_Return_Date,Book_Returned from borrower_management where BID = %s;",
                (bid,))
        else:
            studentid = input("Enter Student ID (Leave Blank If Not Known) : ")
            if studentid != '':
                mycursor.execute(
                    "SELECT BID,BookID,StudentID,StudentFirstName,Borrow_Date,Compulsory_Return_Date,Book_Returned from borrower_management where StudentID = %s ;",
                    (studentid,))
            else:
                bookid = input("Enter Book ID (Leave Blank If Not Known) : ")
                if bookid != '':
                    mycursor.execute(
                        "SELECT BID,BookID,StudentID,StudentFirstName,Borrow_Date,Compulsory_Return_Date,Book_Returned from borrower_management where BookID = %s ;",
                        (bookid,))
        t = PrettyTable(
            ['Borrowal ID', 'Book ID', 'Student ID', 'Student First Name', 'Borrow Date', 'Compulsory Return Date',
             'Book Returned?'])
        count = 0
        for i in (mycursor.fetchall()):
            if i[-1] != "Y":
                count += 1
                t.add_row(i)

        if count != 0:
            print(t.get_string(title="Pending Returns"))
            bid_confirm = input("Enter The Borrowal ID (BID) To Confirm Return : ")
            return_confirm(bid_confirm)
        else:
            print("No Pending Returns For Given Filters! ")
            try_again = int(input("Enter 1 to Retry, Enter 2 to Show All Pending, Enter 3 to Quit"))
            while try_again not in [1, 2, 3]:
                try_again = int(input("INVALID INPUT! /n Enter 1 to Retry, Enter 2 to Show All Pending, Enter Any Other Key to Quit"))
            if try_again == 1:
                return_book()
            elif try_again == 2:
                showall()
    except ValueError:
        return_book()


def return_confirm(bid):
    d = input("Enter the date of return in YYYY-MM-DD (Leave Empty For Today):")
    if d == '':
        d = datetime.datetime.today().strftime('%Y-%m-%d')
    mycursor.execute("UPDATE borrower_management SET Actual_Return_Date = %s, Book_Returned = '"
                     "Y' WHERE BID= %s ;", (d, bid))
    dbcon.commit()
    csvall()



def penalty_calculator():
    mycursor.execute("SELECT * FROM borrower_management")
    recs = mycursor.fetchall()
    t = PrettyTable(
        ['Borrowal ID', 'Book ID', 'Student ID', 'Student First Name', 'Total Days Borrowed', 'Delay To Return',
         'Fine (Rs. 100 per delayed week)'])
    for rec in recs:
        if rec[7] != 'N':
            date_format = "%Y-%m-%d"
            a = datetime.datetime.strptime(str(rec[4]), date_format)
            b = datetime.datetime.strptime(str(rec[6]), date_format)
            delta = b - a
            days_taken = delta.days
            fineable_days = days_taken - 7
            if days_taken <= 7:
                fineable_days = 0
            penalty = round(100 * (fineable_days / 7), 2)
            t.add_row([rec[0], rec[1], rec[2], rec[3], days_taken, fineable_days, penalty])
    print(t.get_string(title="Penalty Applicable To Books Returned"))

    mycursor.execute(
        "SELECT BID,BookID,StudentID,StudentFirstName,Borrow_Date,Compulsory_Return_Date,Book_Returned from borrower_management;")
    recs = mycursor.fetchall()
    x = PrettyTable(
        ['Borrowal ID', 'Book ID', 'Student ID', 'Student First Name', 'Total Days Borrowed(Till Today)',
         'Delay To Return (Till Today)',
         'Fine (Till Today)(Rs. 100 per delayed week)'])
    for rec in recs:
        if rec[6] != 'Y':
            date_format = "%Y-%m-%d"
            td = datetime.datetime.today().strftime('%Y-%m-%d')
            a = datetime.datetime.strptime(str(rec[4]), date_format)
            b = datetime.datetime.strptime(str(td), date_format)
            delta = b - a
            days_taken = delta.days
            fineable_days = days_taken - 7
            if days_taken <= 7:
                fineable_days = 0
            penalty = round(100 * (fineable_days / 7), 2)
            x.add_row([rec[0], rec[1], rec[2], rec[3], days_taken, fineable_days, penalty])
    print(x.get_string(title="Penalty Applicable To Books Not Yet Returned"))
    enter=input("Click Enter To Return To Home Screen : ")


def csvall():
    mycursor.execute("SELECT * from borrower_management;")
    with open('allresults.csv', 'w+', newline='') as cfileall:
        write_data = csv.writer(cfileall, delimiter=",")
        for i in mycursor.fetchall():
            write_data.writerow(i)
        cfileall.close()
        
def showall():
    with open('allresults.csv', 'r', newline='') as cfileall:
        read_data = csv.reader(cfileall, delimiter=",")
        t = PrettyTable(['BID', 'BookID', 'StudentID', 'Student First Name', 'Borrow Date', 'Compulsory Return Date',
                         'Actual Return Date', 'Book_Returned'])
        for i in read_data:
            t.add_row(i)
        print(t)
    enter=input("Click Enter To Return To Home Screen : ")



def filter_show():
    with open('allresults.csv', 'r', newline='') as cfileall:
        read_data = csv.reader(cfileall, delimiter=",")
        t=PrettyTable(["Filter Code","Filter Based On"])
        t.add_row(["1", "Borrowal ID"])
        t.add_row(["2", "Book ID"])
        t.add_row(["3", "Student ID"])
        t.add_row(["4", "Student First Name"])
        t.add_row(["5", "Borrow Date (Month and Year)"])
        t.add_row(["6", "Borrow Date (Day,Month and Year)"])
        print(t)
        todo=input("Enter Filter Code To See Related Borrowal Information : ")
        filtered = PrettyTable(['BID', 'BookID', 'StudentID', 'Student First Name', 'Borrow Date', 'Compulsory Return Date',
                         'Actual Return Date', 'Book_Returned'])
        if todo == "1":
            x = input("Enter Borrowal ID : ")

        elif todo == "2":
            x = input("Enter Book ID : ")

        elif todo == "3":
            x = input("Enter Student ID : ")

        elif todo == "4":
            x = input("Enter Student First Name : ")

        elif todo == "5":
            y = input("Enter Borrowal Year (YYYY): ")
            m = input("Enter Borrowal Month (MM): ")
            x = y + '-' + m

        elif todo == "6":
            y = input("Enter Borrowal Year : ")
            m = input("Enter Borrowal Month : ")
            d = input("Enter Borrowal Day : ")
            x = y + '-' + m + '-' + d

        else:
            print("Please Enter Appropriate Value!")
            filter_show()

        for i in read_data:
            if todo=="1":
                if i[0]==x:
                    filtered.add_row(i)
            elif todo=="2":
                if i[1]==x:
                    filtered.add_row(i)
            elif todo=="3":
                if i[2]==x:
                    filtered.add_row(i)
            elif todo=="4":
                if i[3]==x:
                    filtered.add_row(i)
            elif todo=="5":
                if i[4][:-3]==x:
                    filtered.add_row(i)
            elif todo=="6":
                if i[4]==x:
                    filtered.add_row(i)
        print(filtered)
    try_again=input("Search Again? (Y for yes/ S to See All Records/ Any Other Key For No) : ")

    if try_again=="Y" or try_again=="y":
        filter_show()
    elif try_again=="S" or try_again=="s":
        showall()
    else:
        enter=input("Click Enter To Return To Home Screen : ")
