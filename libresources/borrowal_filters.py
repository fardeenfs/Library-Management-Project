import csv

from prettytable import PrettyTable


def showall():
    with open('allresults.csv', 'r', newline='') as cfileall:
        read_data = csv.reader(cfileall, delimiter=",")
        t = PrettyTable(['BID', 'BookID', 'StudentID', 'Student First Name', 'Borrow Date', 'Compulsory Return Date',
                         'Actual Return Date', 'Book_Returned'])
        for i in read_data:
            t.add_row(i)
        print(t)
    enter = input("Click Enter To Return To Home Screen : ")


def filter_show():
    cfileall=open('allresults.csv', 'r', newline='')
    read_data = csv.reader(cfileall, delimiter=",")
    t = PrettyTable(["Filter Code", "Filter Based On"])
    t.add_row(["1", "Borrowal ID"])
    t.add_row(["2", "Book ID"])
    t.add_row(["3", "Student ID"])
    t.add_row(["4", "Student First Name"])
    t.add_row(["5", "Borrow Date (Month and Year)"])
    t.add_row(["6", "Borrow Date (Day,Month and Year)"])
    t.add_row(["Any Other Key","Back To Home Menu"])
    print(t)
    todo = input("Enter Filter Code To See Related Borrowal Information : ")
    filtered = PrettyTable(
        ['BID', 'BookID', 'StudentID', 'Student First Name', 'Borrow Date', 'Compulsory Return Date',
         'Actual Return Date', 'Book_Returned'])
    if todo == "1":
        x = input("Enter Borrowal ID : ")

    elif todo == "2":
        x = input("Enter Book ID : ")

    elif todo == "3":
        x = input("Enter Student ID : ")

    elif todo == "4":
        x = (input("Enter Student First Name : ")).title()

    elif todo == "5":
        y = input("Enter Borrowal Year (YYYY): ")
        m = input("Enter Borrowal Month (MM): ")
        x = y + '-' + m

    elif todo == "6":
        y = input("Enter Borrowal Year : ")
        m = input("Enter Borrowal Month : ")
        d = input("Enter Borrowal Day : ")
        x = y + '-' + m + '-' + d


    for i in read_data:
        if todo == "1":
            if i[0] == x:
                filtered.add_row(i)
        elif todo == "2":
            if i[1] == x:
                filtered.add_row(i)
        elif todo == "3":
            if i[2] == x:
                filtered.add_row(i)
        elif todo == "4":
            if i[3] == x:
                filtered.add_row(i)
        elif todo == "5":
            if i[4][:-3] == x:
                filtered.add_row(i)
        elif todo == "6":
            if i[4] == x:
                filtered.add_row(i)
    print(filtered)
    try_again = input("Search Again? (Y for yes/ S to See All Records/ Any Other Key For No) : ")

    if try_again == "Y" or try_again == "y":
        filter_show()
    elif try_again == "S" or try_again == "s":
        showall()
    else:
        enter = input("Click Enter To Return To Home Screen : ")