import mysql.connector as datasrc
import csv
from prettytable import PrettyTable
from libresources import table2, table1, borrowal, borrowal_filters
import time

dbcon = datasrc.connect(host='localhost',
                        user='root',
                        password='root',
                        database='library_management')

if dbcon.is_connected():
    print("Successfully Connected To The Database!")

mycursor = dbcon.cursor()
time.sleep(2)


def setup():
    try:
        with open("settings.csv", "r", newline='') as csettings:
            settings = list(csv.reader(csettings))
            if settings[0][1] != '' and settings[0][0] == "Name":
                print("\nWelcome Back", settings[0][1], "To The Library Management System!")
                time.sleep(2)
                csettings.close()
                start()
            else:
                print("Some Of Your CSV files seems to be corrupted. \n Resetting...")
                time.sleep(2)
                csettings.close()
                csvclear = open("settings.csv", "w")
                csvclear.close()
                print("RESET SUCCESSFULLY! \n Restarting...")
                time.sleep(2)
                setup()

    except (IndexError, FileNotFoundError):
        print(PrettyTable(["Weclome To The Library Management System!"]))
        name = input("We see that you are new! Please enter your name : ")
        wset = open("settings.csv", "w", newline='')
        wsettings = csv.writer(wset, delimiter=",")
        wsettings.writerow(['Name', name])
        wsettings.writerow(['Penalty (Per Delayed Week)', '100'])
        print("Good To See You", name, "!")
        wset.close()
        start()





def start():
    try:
        t = PrettyTable(["TO DO Code", "What It Does"])
        t.add_row(["1", "Check Book Info Information"])
        t.add_row(["2", "Check Book Borrowal Information"])
        t.add_row(["3", "Add A New Book"])
        t.add_row(["4", "Add A New Borrowal Record"])
        t.add_row(["5", "Add A Book Returned Record"])
        t.add_row(["6", "View Penalties And Fines"])
        t.add_row(["7", "Settings"])
        print(t)
        todo = int(input("Enter To Do Code to get started: "))
        if todo == 2:
            borrowal_filters.filter_show()
            start()
        elif todo == 4:
            borrowal.new_borrowal()
            start()
        elif todo == 5:
            borrowal.return_book()
            start()
        elif todo == 6:
            borrowal.penalty_calculator()
            start()
        elif todo == 7:
            settings()
    except ValueError:
        print("Please Enter A Valid TO DO Code!")
        start()


def DatabaseCheck():
    with open("startuptest.csv", mode="r") as cfile:
        read_data = list(csv.reader(cfile))
        try:
            if read_data[0][1] == 'Y':
                print("Database Found")
                cfile.close()
        except IndexError:
            cfile.close()
            with open("startuptest.csv", mode="a+", newline='') as cfile:
                print(read_data)
                mycursor.execute('DROP Database IF EXISTS library_management;')
                mycursor.execute('create database library_management;')
                mycursor.execute('use library_management;')
                write_data = csv.writer(cfile, delimiter=",")
                write_data.writerow(['Database Created?', 'Y'])
                print("New Database Created")
                cfile.close()


def settings():
    with open("settings.csv", "r") as csettings:
        settings = list(csv.reader(csettings))
        t = PrettyTable(["Serial No. ", "Field", "Value"])
        print(settings)
        count = 0
        for i in settings:
            count += 1
            print(i)
            i = [str(count)] + i
            t.add_row(i)
        print(t)
    todo = input("Enter 1 to change settings/ Any Other Key To Go Back To Home Menu : ")
    if todo == '1':
        try:
            fld = (int(input("Enter Serial No. Of Field To Change : ")))
            uv = input("Enter New Value : ")
            edit_settings(fld, uv)
        except ValueError:
            print("No Such Serial No.! Returning to settings...")
            time.sleep(2)
    else:
        start()


def edit_settings(fld, uv):
    fld = fld - 1
    with open("settings.csv", "r") as rsettings:
        esettings = list(csv.reader(rsettings))
        esettings[fld][1] = uv
        rsettings.close()
    with open("settings.csv", "w", newline="") as rsettings:
        wsettings = csv.writer(rsettings)
        wsettings.writerows(esettings)
        rsettings.close()
    print("Value Updated Successfully! ")
    settings()


table2.Table2Check()
setup()
# start()

time.sleep(2)
print("BYE")
