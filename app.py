from collections import OrderedDict
import datetime
import csv
import os
import sys
import re

from peewee import *

db = SqliteDatabase('inventory.db')

class Product(Model):
    product_id = AutoField(primary_key = True)
    product_name = TextField(unique = True)
    product_quantity = IntegerField(default = 0)
    product_price = IntegerField()
    date_updated = DateTimeField()
    class Meta:
        database = db

def initialize():
    """Creates the database and table"""
    db.connect()
    db.create_tables([Product], safe=True)
    with open('inventory.csv', newline='') as inventory_csv_file:
        inventory_reader = csv.DictReader(inventory_csv_file, delimiter=',')
        product_dicts = list(inventory_reader)
        for product in product_dicts:
            try:
                Product.insert(
                    product_name = product['product_name'],
                    product_price = price_to_cents(product['product_price']),
                    product_quantity = clean_quantity(product['product_quantity']),
                    date_updated = clean_date(product['date_updated'])
                ).execute()
            except IntegrityError:
                duplicate_record = Product.get(product_name=product['product_name'])
                if duplicate_record.date_updated <= clean_date(product['date_updated']):
                    duplicate_record.product_price = price_to_cents(product['product_price'])
                    duplicate_record.product_quantity = clean_quantity(product['product_quantity'])
                    duplicate_record.date_updated = clean_date(product['date_updated'])
                    duplicate_record.save()

def new_row(new_product):
    try:
        Product.insert(
            product_name = new_product['product_name'],
            product_price = price_to_cents(new_product['product_price']),
            product_quantity = clean_quantity(new_product['product_quantity']),
            date_updated = clean_date(new_product['date_updated'])
        ).execute()
    except IntegrityError:
        duplicate_record = Product.get(product_name=new_product['product_name'])
        if duplicate_record.date_updated <= clean_date(new_product['date_updated']):
            duplicate_record.product_price = price_to_cents(new_product['product_price'])
            duplicate_record.product_quantity = clean_quantity(new_product['product_quantity'])
            duplicate_record.date_updated = clean_date(new_product['date_updated'])
            duplicate_record.save()

def clear_terminal():
    """Clears the terminal for a new entry"""
    os.system('cls' if os.name == 'nt' else 'clear')
    
def price_to_cents(product):
    price_no_sign = product.replace('$', '')
    price_now_cents = int(float(price_no_sign)*100)
    return price_now_cents

def clean_quantity(product):
    return int(product)

def clean_date(product):
    return datetime.datetime.strptime(product, '%m/%d/%Y')
    
def view_order():
    """View the order"""
    id_number = None
    while True:
        try:
            id_number = input("Please enter a product ID number between numbers 1-{}: ".format(len(Product)))
            while id_number.isalpha() and id_number != 'q':
                id_number = input("\nThat's not a valid entry, please select an ID with a number between 1 and {}, or enter 'q' to return to the Main Menu: ".format(len(Product)))
            id_number = int(id_number)
            product = Product.get(id_number)
            clear_terminal()
            print(f"ID: {product.product_id}")
            print(f"Name: {product.product_name}")
            print(f"Quantity: {product.product_quantity}")
            print(f"Price: ${format(product.product_price / 100, '.2f')}") #Converting Float to Dollars and Cents - found this in StackOverflow
            print(f"Date Updated: {product.date_updated}\n")
            more_products = input("Would you like to view another product? [yN] ").lower()
            if more_products == "n":
                break
            else:
                clear_terminal()
        except DoesNotExist:
            clear_terminal()
            print("Product ID does not exist. Product ID ranges between 1 and {}.".format(len(Product)))
        except ValueError:
            break

def add_product():
    """Add a product"""
    print("Enter your entry")
    while True:
        try:
            new_product = OrderedDict()
            new_product['product_name'] = input("Please Input Product Name: ")
            new_product['product_quantity'] = int(input("Please Input Product Quantity (numbers only): "))
            new_product['product_price'] = input("Please Input Product Price ($X.XX): ")
            new_product['date_updated'] = datetime.datetime.now().strftime('%m/%d/%Y')
            price_to_cents(new_product['product_price'])
            clean_quantity(new_product['product_quantity'])
            clean_date(new_product['date_updated'])
            if input("Save Entry? [Yn] ").lower() == 'y':
                new_row(new_product)
                clear_terminal()
                print("Saved Successfully!")
                another_entry = input("Would you like to add another product? [Y/N] ")
                if another_entry == 'y':
                    clear_terminal()
                    continue
                else:
                    break
            else:
                break
        except ValueError:
            print("Invalid entry. My system doesn't like that...")

def backup():
    """Backup the database"""
    #snagged all of this from  CSV File Reading and Writing in docs.python.org
    with open('back_up.csv', 'w', newline='') as backup_csvfile:
        fieldnames = ['product_name', 'product_price','product_quantity', 'date_updated']
        back_up_writer = csv.DictWriter(backup_csvfile, fieldnames=fieldnames)
        back_up_writer.writeheader()
        all_products = Product.select()
        for product in all_products:
            back_up_writer.writerow({
                'product_name': product.product_name,
                'product_price': product.product_price,
                'product_quantity': product.product_quantity,
                'date_updated': product.date_updated
                })
        print("Data has been backed up successfully!\n")
        input("Press enter to return to the main menu")
            
menu = OrderedDict([
    ('v', view_order),
    ('a', add_product),
    ('b', backup),
])

def menu_loop():
    """Show the Menu"""
    choice = None
    while choice != 'q':
        clear_terminal()
        print("Enter an option from below OR Enter 'q' to quit.")
        for key, value in menu.items():
            print("{}) {}".format(key, value.__doc__))
        choice = input("Action: ").lower()
        if choice in menu:
            clear_terminal()
            menu[choice]()
        while choice not in menu and choice != 'q':
            choice = input("That's not a valid choice. please try again: ")
            if choice in menu:
                clear_terminal()
                menu[choice]()

if __name__ == '__main__':
    initialize()
    menu_loop()
    
