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

                    
        #print(product_dicts)

def price_to_cents(product):
    price_no_sign = product.replace('$', '')
    price_now_cents = int(float(price_no_sign)*100)
    return price_now_cents

def clean_quantity(product):
    return int(product)

def clean_date(product):
    return datetime.datetime.strptime(product, '%m/%d/%Y')

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
        print("Enter 'q' to quit.")
        for key, value in menu.items:
            print("{}) {}".format(key, value.__doc__))
        choice = input("Action: ").lower().srtip()
        if choice in menu:
            clear_terminal()
            menu[choice]()
    

def view_order():
    """View the order"""
    pass
        

def add_product():
    """Add a product"""
    pass

def backup():
    """Backup the database"""
    pass

def clear_terminal():
    """Clears the terminal for a new entry"""
    os.system('cls' if os.name == 'nt' else 'clear')
    pass

if __name__ == '__main__':
    error_list = []
    initialize()
    print(error_list)
    menu_loop()
    




    # price_match = re.match("^\D\d*.\d{2}\Z", product)
    #if price_match:
     #   price_no_sign = re.sub("\D", '', price_match)
      #  price_in_cents = int(float(price_no_sign) * 100)
       # return price_in_cents