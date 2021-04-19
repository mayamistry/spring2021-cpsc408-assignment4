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

    #command line prompt stuff
    fileName = input("Enter the name of the csv file you would like to create: ")
    numRecords = int(input("Enter the number of records you would like to create: "))

    csv_file = open(fileName, "w")
    writer = csv.writer(csv_file)
    writer.writerow(["CoffeeShopName", "PhoneNumber", "AverageDriveTimeFromChapman", "WiFi", "IndoorSeating", "Outlets", "Music", "FoodName", "FoodRating", "FoodPrice", "EmployeeName", "EmployeeRating", "ReviewDescription", "DrinkName", "DrinkRating", "DrinkPrice"])

    foods = ["Donut", "Bagel and cream cheese", "Cookie", "Avocado Toast", "Scone", "Breakfast Burrito", "Croissant", "Breakfast Sandwich", "Blueberry Muffin", "Chocolate Chip Muffin", "Chocolate Croissant"]
    drinks = ["Chai Latte", "Cold Brew", "Iced Latte", "Hot Latte", "Iced Tea", "Cappucino", "Flat White", "Black Coffee", "Americano", "Hot Chocolate", "Iced Coffee", "Matcha Latte"]

    for x in range(0, numRecords):
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
            shopRefID = mycursor.lastrowid
            mycursor.execute("INSERT INTO DrinkTable(DrinkName, DrinkRating, Price) VALUES (%s, %s, %s);", (row["DrinkName"], row["DrinkRating"], row["DrinkPrice"]))
            db.commit()
            drinkRefID = mycursor.lastrowid
            mycursor.execute("INSERT INTO EmployeeTable(EmployeeName, EmployeeRating, ReviewDescription) VALUES (%s, %s, %s);",
                             (row["EmployeeName"], row["EmployeeRating"], row["ReviewDescription"]))
            db.commit()
            employeeRefID = mycursor.lastrowid
            mycursor.execute("INSERT INTO FoodTable(FoodName, FoodRating, Price) VALUES (%s, %s, %s);",
                             (row["FoodName"], row["FoodRating"], row["FoodPrice"]))
            db.commit()
            foodRefID = mycursor.lastrowid
            mycursor.execute("INSERT INTO StudySpotsTable(ShopID, WiFi, IndoorSeating, Outlets, Music) VALUES (%s, %s, %s, %s, %s);",
                             (shopRefID, row["WiFi"], row["IndoorSeating"], row["Outlets"], row["Music"]))
            db.commit()
            mycursor.execute("INSERT INTO CoffeeShopServesFood(FoodID, ShopID) VALUES (%s, %s);", (foodRefID, shopRefID))
            db.commit()
            mycursor.execute("INSERT INTO CoffeeShopServesDrink(DrinkID, ShopID) VALUES (%s, %s);",
                             (drinkRefID, shopRefID))
            db.commit()
            mycursor.execute("INSERT INTO EmployeeWorksAt(EmployeeID, ShopID) VALUES (%s, %s);",
                             (employeeRefID, shopRefID))
            db.commit()
            print("import successful")
