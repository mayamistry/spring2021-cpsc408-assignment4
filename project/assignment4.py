import mysql.connector
import random as rand
from faker import Faker
import csv

#contains all the info necessary to establish connection
db = mysql.connector.connect(
    host = "35.236.58.10",
    user = "myappuser",
    password = "foobar",
    database = "CoffeeShopDB"
)

def genData():
    #need to create an instance of faker
    fake = Faker()
    #generate data and then right to a file

    csv_file = open("mydata.csv", "w")
    writer = csv.writer(csv_file)
    writer.writerow(["CoffeeShopName", "PhoneNumber", "AverageDriveTimeFromChapman", "WiFi", "IndoorSeating", "Outlets", "Music", "FoodName", "FoodRating", "FoodPrice", "EmployeeName", "EmployeeRating", "ReviewDescription", "DrinkName", "DrinkRating", "DrinkPrice"])

    foods = ["Donut", "Bagel and cream cheese", "Cookie", "Avocado Toast", "Scone", "Breakfast Burrito", "Croissant", "Breakfast Sandwich", "Blueberry Muffin", "Chocolate Chip Muffin", "Chocolate Croissant"]
    drinks = ["Chai Latte", "Cold Brew", "Iced Latte", "Hot Latte", "Iced Tea", "Cappucino", "Flat White", "Black Coffee", "Americano", "Hot Chocolate", "Iced Coffee", "Matcha Latte"]

    for x in range(0, 30):
        foodIndex = rand.randint(0,10)
        drinkIndex = rand.randint(0,11)
        writer.writerow([fake.company(), fake.phone_number(), fake.random_int(0, 45), fake.random_int(0, 1), fake.random_int(0, 1), fake.random_int(0, 1), fake.random_int(0, 1), foods[foodIndex], fake.random_int(1,10), fake.random_int(3,30), fake.name(), fake.random_int(1,10), fake.paragraph(nb_sentences=2), drinks[drinkIndex], fake.random_int(1,10), fake.random_int(2,30)])


#allows you to execute mySQL statements
def importData():
    mycursor = db.cursor()
    with open("./mydata.csv") as csvfile:
       reader = csv.DictReader(csvfile)

       for row in reader:
            print("importing information..")
            mycursor.execute("INSERT INTO CoffeeShopTable(CoffeeShopName, PhoneNumber, AverageDriveTimeFromChapman) VALUES (%s, %s, %s);", (row["CoffeeShopName"], row["PhoneNumber"], row["AverageDriveTimeFromChapman"]))
            db.commit()
            #studentId = mycursor.lastrowid
            #mycursor.execute("INSERT INTO StudentAddress(StudentId, Street, City, ZipCode) VALUES (%s, %s, %s, %s);", (studentId, row["Street"], row["City"], row["Zip"]))
            #db.commit()
            print("import successful")



#INITAL PART - SELECT
# mycursor.execute("SELECT * FROM StudentTable;")
# data = mycursor.fetchall()
#
# for d in data:
#     print(d[1])
#     print(d[4])

#SECOND PART - INSERT
# #%s is how you do parameter binding in mySQL to avoid SQL Injection
# mycursor.execute("INSERT INTO StudentTable(FirstName, LastName, Major, GPA) VALUES (%s, %s, %s, %s);", ('bar','foo','MATH','3.9'))
# #commit this change to the database
# db.commit()
#
# #rene will go over this later --> gives the id of the last record created and this is
# #important because you can use this as foreign key in other tables when more tables get involved
# studentId = mycursor.lastrowid
#
# print('created new student: ', studentId)

#THIRD PART - UPDATE
# mycursor.execute("UPDATE StudentTable SET Major = %s"
#                  "WHERE StudentId = %s;", ('MUSIC', 4))

#db.commit()
#print("Successful!")


#importData()