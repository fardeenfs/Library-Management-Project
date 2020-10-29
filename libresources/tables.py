import mysql.connector as datasrc
import csv
import datetime

dbcon = datasrc.connect(host='localhost',
                        user='root',
                        password='root',
                        database='library_management')

mycursor = dbcon.cursor()

def TablesCheck():
    mycursor.execute('use library_management;')
    with open("startuptest.csv", mode="r") as cfile:
        read_data = list(csv.reader(cfile))
        try:
            if read_data[0][1] == 'Y':
                print("Tables Found")
                cfile.close()
        except IndexError:
            cfile.close()
            with open("startuptest.csv", mode="w", newline='') as cfile:
                mycursor.execute("DROP TABLE IF EXISTS BookInfo;")
                mycursor.execute('''create table BookInfo (BookID varchar(6) PRIMARY KEY,
                                                            BookName varchar(50),
                                                            Author varchar(40),
                                                            Subject varchar(20),
                                                            Isbn varchar (13),
                                                            Publication varchar(50),
                                                            Quantity varchar(4));''')
                mycursor.execute("DROP TABLE IF EXISTS borrower_management;")
                mycursor.execute('''create table borrower_management (BID varchar(6) PRIMARY KEY,
                                                                        BookID varchar(4) REFERENCES BookInfo(BookID) ,
                                                                        StudentID varchar(4),                                                                                                                                                
                                                                        StudentFirstName varchar(30),                                                                        
                                                                        Borrow_Date date,
                                                                        Compulsory_Return_Date date,
                                                                        Actual_Return_Date date DEFAULT NULL,
                                                                        Book_Returned varchar(1));''')
                write_data = csv.writer(cfile, delimiter=",")
                write_data.writerow(['Table Created?', 'Y'])
                print("Tables Created")
                tablevalues()
                cfile.close()


def tablevalues():
    f1 = [100001, 100002, 100003, 100004, 100005, 100006, 100007, 100008, 100009, 100010]
    f2 = [101, 102, 103, 105, 103, 101, 104, 101, 102, 102]
    f3 = [1002, 1001, 1003, 1009, 1004, 1005, 1006, 1008, 1007, 1010]
    f4 = ['Udhayan', 'Rishabh', 'Srikar', 'Madhu', 'Vidula', 'Meet', 'Chaitra', 'Fardeen', 'Chandu', 'Sumiit']
    f5 = ["2020-10-21", "2020-09-29", "2020-09-28", "2020-10-01", "2020-10-01", "2020-08-21", "2020-09-03",
          "2020-09-11", "2020-10-15", "2020-10-16"]
    f7 = ["2020-10-27", "2020-10-11", "2020-10-21", "2020-09-10", "2020-10-20"]
    f8 = ['Y', 'Y', 'N', 'Y', 'N', 'N', 'Y', 'N', 'N', 'Y']
    cleared = [2, 4, 5, 7, 8]
    rec = len(f1)
    f7rec = 0
    for i in range(0, rec):
        if i not in cleared:
            f6 = (datetime.datetime.strptime(f5[i], '%Y-%m-%d') + datetime.timedelta(days=7)).strftime('%Y-%m-%d')
            mycursor.execute("insert into borrower_management values(%s,%s,%s,%s,%s,%s,%s,%s);",
                             (f1[i], f2[i], f3[i], f4[i], f5[i], f6, f7[f7rec], f8[i]))
            f7rec += 1
        else:
            f6 = (datetime.datetime.strptime(f5[i], '%Y-%m-%d') + datetime.timedelta(days=7)).strftime('%Y-%m-%d')
            mycursor.execute(
                "insert into borrower_management(BID,BookID,StudentID,StudentFirstName,Borrow_Date,Compulsory_Return_Date,Book_Returned) values(%s,%s,%s,%s,%s,%s,%s);",
                (f1[i], f2[i], f3[i], f4[i], f5[i], f6, f8[i]))
    dbcon.commit()

    f1 = [101, 102, 103, 104, 105]
    f2 = ["Introduction to computers- Junior level", "The killing woods", "The thirteenth mystery",
          "R.D Sharma Class 12", "Uttar vigyan"]
    f3 = ["Amit garg", "Lucy Christopher", "Michael Dahl", "R.D Sharma", "Preeti Agarwal"]
    f4 = ["Computer Science", "Litereature-Fiction", "Litereature-Fiction", "Maths", "Hindi"]
    f5 = ["BZN127YTER120", "QYD947JND492", "PTK385NIFC863", "GSV530JFSO932", "HWQ938FNPS348"]
    f6 = ["Reader's Zone","Scholastic","Chicken House","Dhanpat Rai","Arihant"]
    f7 = [3, 6, 4, 5, 2]

    rec = len(f1)
    for i in range(0, rec):
        mycursor.execute("insert into BookInfo values(%s,%s,%s,%s,%s,%s,%s);",
                    (f1[i], f2[i], f3[i], f4[i], f5[i], f6[i], f7[i]))
    dbcon.commit()