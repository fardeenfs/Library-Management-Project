import mysql.connector as datasrc
import csv
import datetime
import time
from prettytable import PrettyTable

dbcon = datasrc.connect(host='localhost',
                        user='root',
                        password='root',
                        database='library_management')

mycursor = dbcon.cursor()


def book_add():
    mycursor.execute('SELECT * from BookInfo;')
    recs = mycursor.fetchall()
    x = len(recs)
    lastbid = int(recs[x - 1][0]) + 1
    try:
        y = (input("Enter Book Name : ")).title()
        z = (input("Enter Author : ")).title()
        u = (input("Enter Subject : ")).title()
        a = (input("Enter Publication : ")).title()
        isbn = (input("Enter ISBN No. : ")).upper()
        b = int(input("Enter Quantity : "))
        cnt = 0
        for rec in recs:
            if rec[4] == isbn:
                cnt += 1
                print(
                    "Looks like this book already exists! Please use the UPDATE BOOK option to increase the quantity:) ")
        if cnt == 0:
            mycursor.execute(
                "insert into BookInfo(BookID,BookName,Author,Subject,Isbn,Publication,Quantity) values (%s,%s,%s,%s,%s,%s,%s);",
                (lastbid, y, z, u, isbn, a, b))
            dbcon.commit()
            print("Book Successfully Added!")
    except ValueError:
        print("Please Enter Appropriate Values.")
        book_add()


def book_update():
    book_id = input("Enter Book ID To Update (Leave Blank If Not Known) : ")
    if book_id != '':
        mycursor.execute(
            "SELECT BookID,BookName,Author,Subject,Isbn,Publication,Quantity from BookInfo where BookID = %s;",
            (book_id,))
        t = PrettyTable(['Update Code', 'What It Does'])
        t.add_row(["1", "Update Quantity"])
        t.add_row(["2", "Update Publication"])
        print(t)
        ch1 = input("Enter your choice of updation : ")
    else:
        bookname = (input("Enter Book Name To Update (Leave Blank If Not Known) : ")).title()
        if bookname != '':
            mycursor.execute(
                "SELECT BookID,BookName,Author,Subject,Isbn,Publication,Quantity from BookInfo where BookName= %s ;",
                (bookname,))
            t = PrettyTable(['Update Code', 'What It Does'])
            t.add_row(["1", "Update Quantity"])
            t.add_row(["2", "Update Publication"])
            print(t)
            ch1 = input("Enter your choice of updation : ")
        else:
            print("Please Answer To At Least One Filter To Search! ")
            ch1=''
    x = mycursor.fetchone()
    if ch1 == "1":
        b = int(input("Enter the New Quantity : "))
        mycursor.execute("UPDATE BookInfo set Quantity=%s where BookID =%s;", (b, x[0]))
        dbcon.commit()
        print("Record Updated Successfully!")
        enter = input("Click Enter To Return To Home Page : ")

    elif ch1 == "2":
        b = input("Enter the publication to change : ")
        mycursor.execute("UPDATE BookInfo set Publication=%s where BookID=%s;", (b, x[0]))
        dbcon.commit()
        print("Record Updated Successfully!")
        enter = input("Click Enter To Return To Home Page : ")
    elif ch1 == "":
        print("Returning To Home...")
        time.sleep(1)
    else:
        print("You have entered the wrong choice for updating please try again!")


def book_search():
    book_id = input("Enter Book ID To Search (Leave Blank If Not Known) : ")
    t = PrettyTable(['BookID', 'BookName', 'Author', 'Subject', 'ISBN', 'Publication', 'Quantity'])
    if book_id != '':
        mycursor.execute(
            "SELECT BookID,BookName,Author,Subject,Isbn,Publication,Quantity from BookInfo where BookID = %s;",
            (book_id,))
        printable = mycursor.fetchone()
        t.add_row(printable)
    else:
        bookname = input("Enter Book Name To Search (Leave Blank If Not Known) : ")
        if bookname != '':
            mycursor.execute(
                "SELECT BookID,BookName,Author,Subject,Isbn,Publication,Quantity from BookInfo where BookName= %s ;",
                (bookname.title(),))
            printable = mycursor.fetchone()
            t.add_row(printable)
        else:
            print("Showing All Results...")
            time.sleep(1)
            mycursor.execute("SELECT * FROM BookInfo")
            printable=mycursor.fetchall()
            if len(printable)==1:
                t.add_row(printable)
            else:
                for rec in printable:
                    t.add_row(rec)

    print(t)
    enter = input("Click Enter To Return To Home Page : ")



def book_remove():
    book_id = input("Enter Book ID To Delete (Leave Blank If Not Known) : ")
    if book_id != '':
        mycursor.execute(
            "SELECT BookID,BookName,Author,Subject,Isbn,Publication,Quantity from BookInfo where BookID = %s;",
            (book_id,))
        x = mycursor.fetchone()
        t = PrettyTable(['Book ID', 'Book Name'])
        t.add_row([x[0], x[1]])
        print(t)
        a = int(input("Enter the BookID to confirm deletion : "))
        mycursor.execute("Delete from BookInfo where BookID=%s;", (a,))
        dbcon.commit()
        print("Book Removed Successfully!")
    else:
        bookname = (input("Enter Book Name To Delete : ")).title()
        if bookname != '':
            mycursor.execute(
                "SELECT BookID,BookName,Author,Subject,Isbn,Publication,Quantity from BookInfo where BookName= %s ;",
                (bookname,))
            x = mycursor.fetchone()
            t = PrettyTable(['Book ID', 'Book Name'])
            t.add_row([x[0], x[1]])
            print(t)
            a = int(input("Enter the BookID to confirm deletion : "))
            mycursor.execute("Delete from BookInfo where BookID=%s;", (a,))
            dbcon.commit()
            print("Book Removed Successfully!")
        else:
            print("Enter At Least One Filter!")
            print("Aborting...")

    enter = input("Click Enter To Return To Home Page : ")