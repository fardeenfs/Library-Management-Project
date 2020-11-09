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
                                                                        BookID varchar(6) REFERENCES BookInfo(BookID) ,
                                                                        StudentID varchar(10),                                                                                                                                                
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
    file = open("testvalues1.csv")
    fileread = csv.reader(file, delimiter=",")
    x = []
    for line in fileread:
        x.append(line)
    f1, f2, f3, f4, f5, f7, f8, cleared = x
    rec = len(f1)
    f7rec = 0
    for i in range(0, rec):
        if str(i) not in cleared:
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
    file.close()

    file = open("testvalues2.csv")
    fileread = csv.reader(file, delimiter=",")
    x = []
    for line in fileread:
        x.append(line)
    f1, f2, f3, f4, f5, f6, f7 = x
    rec = len(f1)
    for i in range(0, rec):
        mycursor.execute("insert into BookInfo values(%s,%s,%s,%s,%s,%s,%s);",
                         (f1[i], f2[i], f3[i], f4[i], f5[i], f6[i], f7[i]))
    dbcon.commit()
    file.close()
