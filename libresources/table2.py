import mysql.connector as datasrc
import csv
import datetime

dbcon = datasrc.connect(host='localhost',
                        user='root',
                        password='root',
                        database='library_management')

mycursor = dbcon.cursor()

def Table2Check():
    mycursor.execute('use library_management;')
    with open("startuptest.csv", mode="r") as cfile:
        read_data = list(csv.reader(cfile))
        try:
            if read_data[1][1] == 'Y':
                print("Tables Found")
                cfile.close()
        except IndexError:
            cfile.close()
            with open("startuptest.csv", mode="a+", newline='') as cfile:
                mycursor.execute("DROP table IF Exists borrower_management")
                mycursor.execute('''create table borrower_management(BID varchar(6) PRIMARY KEY,
                                                                        BookID varchar(4),
                                                                        StudentID varchar(4),                                                                                                                                                
                                                                        StudentFirstName varchar(30),                                                                        
                                                                        Borrow_Date date,
                                                                        Compulsory_Return_Date date,
                                                                        Actual_Return_Date date DEFAULT NULL,
                                                                        Book_Returned varchar(1));''')
                write_data = csv.writer(cfile, delimiter=",")
                write_data.writerow(['Table Created?', 'Y'])
                print("BookBorrowerManagement Table Created")
                table2values()
                cfile.close()


def table2values():
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
    for i in range(0, rec - 1):
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