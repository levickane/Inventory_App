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
        inventory_reader = csv.DictReader(inventory_csv_file)
        product_dicts = list(inventory_reader)
        for product in product_dicts:
            Product.create(
                product_name = clean_name(product['product_name']),
                product_price = price_to_cents(product['product_price']),
                product_quantity = clean_quantity(product['product_quantity']),
                date_updated = clean_date(product['date_updated'])
            )
            print(product_dicts)

def clean_name(product):
    return re.match("\"?\w+\s-\s\w+\,?\s?\w*?\"?", product)

def price_to_cents(product):
    price_no_sign = product.replace('$', '')
    price_now_cents = int(float(price_no_sign)*100)
    return price_now_cents

def clean_quantity(product):
    return int(product)

def clean_date(product):
    return datetime.datetime.strptime(product, '%m/%d/%Y')

def add_product():
    pass

def clear_terminal():
    """Clears the terminal for a new entry"""
    os.system('cls' if os.name == 'nt' else 'clear')

def menu_loop():
    pass

def backup():
    pass


if __name__ == '__main__':
    initialize()
    
    




    # price_match = re.match("^\D\d*.\d{2}\Z", product)
    #if price_match:
     #   price_no_sign = re.sub("\D", '', price_match)
      #  price_in_cents = int(float(price_no_sign) * 100)
       # return price_in_cents