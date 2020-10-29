import mysql.connector as datasrc
import csv
import datetime
from prettytable import PrettyTable
from libresources import borrowal_filters

dbcon = datasrc.connect(host='localhost',
                        user='root',
                        password='root',
                        database='library_management')

mycursor = dbcon.cursor()


def new_borrowal():
    mycursor.execute('SELECT * from borrower_management;')
    recs = mycursor.fetchall()
    mycursor.execute('SELECT * from BookInfo;')
    books = mycursor.fetchall()
    x = len(recs)
    lastbid = int(recs[x - 1][0]) + 1
    try:
        a = input("Enter BookID : ")
        b = input("Enter Student ID :")
        c = ''
        for rec in recs:
            if rec[2] == b:
                c = rec[3]
        if c == '':
            c = (input("Looks Like This Student Is New! Enter Student's First Name : ")).title()
        d = input("Enter the date of borrowal in YYYY-MM-DD (Leave Empty For Today):")
        if d == '':
            d = datetime.datetime.today().strftime('%Y-%m-%d')
        e = (datetime.datetime.strptime(d, '%Y-%m-%d') + datetime.timedelta(days=7)).strftime('%Y-%m-%d')
        for rec in books:
            if rec[0]==str(a):
                if int(rec[6]) == 1:
                    print("This book cannot be borrowed as only 1 copy is left")
                else:
                    mycursor.execute(
                        "insert into borrower_management(BID,BookID,StudentID,StudentFirstName,Borrow_Date,Compulsory_Return_Date,Book_Returned) values(%s,%s,%s,%s,%s,%s,%s);",
                        (lastbid, a, b, c, d, e, 'N'))
                    mycursor.execute("UPDATE BookInfo set Quantity=%s where BookID=%s;",(int(rec[6])-1,a))
                    print("Borrowal Record Added!")
        dbcon.commit()
        csvall()
    except ValueError:
        print("Please Enter An Appropriate Value!")
        print("Returning To Home...")

    New_Entry = input("Do you want to add another borrowal record? (Y for yes/ Any other key to exit) : ")
    if New_Entry == "Y" or "y":
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
                else:
                    print("All Results...")
                    mycursor.execute("SELECT BID,BookID,StudentID,StudentFirstName,Borrow_Date,Compulsory_Return_Date,Book_Returned FROM borrower_management;")
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
                try_again = int(input(
                    "INVALID INPUT! /n Enter 1 to Retry, Enter 2 to Show All Pending, Enter Any Other Key to Quit"))
            if try_again == 1:
                return_book()
            elif try_again == 2:
                borrowal_filters.showall()
    except ValueError:
        print("Please Enter Appropriate Values!")
        print("Returning To Home Menu...")
        print()


def return_confirm(bid):
    d = input("Enter the date of return in YYYY-MM-DD (Leave Empty For Today):")
    if d == '':
        d = datetime.datetime.today().strftime('%Y-%m-%d')
    mycursor.execute("UPDATE borrower_management SET Actual_Return_Date = %s, Book_Returned = '"
                     "Y' WHERE BID= %s ;", (d, bid))
    mycursor.execute("Select * from borrower_management where BID= %s;",  (int(bid),))
    x=mycursor.fetchone()
    mycursor.execute("Select * from BookInfo where BookID=%s;",(x[1],))
    q=mycursor.fetchone()
    mycursor.execute("UPDATE BookInfo set Quantity=%s where BookID=%s;", (int(q[6]) + 1, x[0]))
    dbcon.commit()
    csvall()
    print("Book Returned Successfully! ")

def penalty_calculator():
    mycursor.execute("SELECT BID,borrower_management.BookID,StudentID,StudentFirstName,BookName,Borrow_Date,Compulsory_Return_Date,Actual_Return_Date,Book_Returned from borrower_management,BookInfo where borrower_management.BookID=BookInfo.BookID;")
    recs = mycursor.fetchall()
    csettings = open("settings.csv")
    settings = list(csv.reader(csettings))
    x = "Penalty @ Rs. " + settings[1][1] + " per delayed week"
    t = PrettyTable(
        ['Borrowal ID', 'Book ID', 'Student ID', 'Student First Name', 'Book Name', 'Total Days Borrowed', 'Delay To Return',
         x])
    for rec in recs:
        if rec[8] != 'N':
            date_format = "%Y-%m-%d"
            a = datetime.datetime.strptime(str(rec[5]), date_format)
            b = datetime.datetime.strptime(str(rec[7]), date_format)
            delta = b - a
            days_taken = delta.days
            fineable_days = days_taken - 7
            if days_taken <= 7:
                fineable_days = 0
            penalty = round(float(settings[1][1]) * (fineable_days / 7), 2)
            t.add_row([rec[0], rec[1], rec[2], rec[3], rec[4], days_taken, fineable_days, penalty])
    print(t.get_string(title="Penalty Applicable To Books Returned"))

    mycursor.execute(
        "SELECT BID,borrower_management.BookID,StudentID,StudentFirstName,BookName,Borrow_Date,Compulsory_Return_Date,Book_Returned from borrower_management,BookInfo where borrower_management.BookID=BookInfo.BookID;")

    recs = mycursor.fetchall()
    x = PrettyTable(
        ['Borrowal ID', 'Book ID', 'Student ID', 'Student First Name', 'Book Name', 'Total Days Borrowed(Till Today)',
         'Delay To Return (Till Today)', x])
    for rec in recs:
        if rec[7] != 'Y':
            date_format = "%Y-%m-%d"
            td = datetime.datetime.today().strftime('%Y-%m-%d')
            a = datetime.datetime.strptime(str(rec[5]), date_format)
            b = datetime.datetime.strptime(str(td), date_format)
            delta = b - a
            days_taken = delta.days
            fineable_days = days_taken - 7
            if days_taken <= 7:
                fineable_days = 0
            penalty = round(float(settings[1][1]) * (fineable_days / 7), 2)
            x.add_row([rec[0], rec[1], rec[2], rec[3], rec[4], days_taken, fineable_days, penalty])
    print(x.get_string(title="Penalty Applicable To Books Not Yet Returned"))
    enter = input("Click Enter To Return To Home Screen : ")


def csvall():
    mycursor.execute("SELECT * from borrower_management;")
    with open('allresults.csv', 'w+', newline='') as cfileall:
        write_data = csv.writer(cfileall, delimiter=",")
        for i in mycursor.fetchall():
            write_data.writerow(i)
        cfileall.close()
